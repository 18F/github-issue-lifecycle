from collections import OrderedDict
from datetime import date, datetime, timedelta
import itertools
import os

import requests
from requests.auth import HTTPBasicAuth

from . import db
from .app import app
from .utils import to_py_datetime

GH_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
BEGINNING_OF_TIME = '1970-01-01T00:00:00Z'
BEGINNING_DATETIME = datetime.strptime(BEGINNING_OF_TIME, GH_DATE_FORMAT)


def authorization():
    try:
        auth = HTTPBasicAuth(os.environ['GITHUB_USER'],
                             os.environ['GITHUB_AUTH'])
        return auth
    except KeyError:
        app.logger.warning(
            'Environment variables GITHUB_USER and GITHUB_AUTH not set')
        app.logger.warning('Skipping authentication...')
        return None


class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    synched_at = db.Column(db.DateTime(),
                           nullable=False,
                           default=BEGINNING_DATETIME)
    issues = db.relationship('Issue',
                             cascade='all, delete-orphan',
                             order_by='Issue.created_at',
                             backref='repo')

    ISSUES_PAGE_SIZE = 100

    @classmethod
    def get_fresh(cls, owner_name, repo_name, refresh_threshhold_seconds=None):
        """For a repo ``repo_name`` owned by ``owner_name``:

        1. Fetches or creates the Repo model instance
        2. Refreshes the data from Github if necessary"""

        if refresh_threshhold_seconds is None:
            refresh_threshhold_seconds = app.config[
                'REFRESH_THRESHHOLD_SECONDS']
        (owner_name, repo_name) = (owner_name.lower(), repo_name.lower())
        repo = (cls.query.filter_by(owner=owner_name,
                                    name=repo_name).first() or
                cls(owner=owner_name,
                    name=repo_name,
                    synched_at=BEGINNING_DATETIME))
        if (datetime.now() - repo.synched_at) > timedelta(
                seconds=int(refresh_threshhold_seconds)):
            repo.fetch_issues()
        db.session.add(repo)
        db.session.commit()
        repo.set_milestone_color_map() 
        return repo

    def url(self):
        return 'https://api.github.com/repos/{}/{}/'.format(self.owner,
                                                            self.name)

    @classmethod
    def _latest_update(cls, items, field_name='updated_at'):
        "Returns latest `field_name` in `items`"
        updates = [datetime.strptime(
            i.get(field_name, BEGINNING_OF_TIME), GH_DATE_FORMAT)
                   for i in items]
        return max(updates).strftime(GH_DATE_FORMAT)

    def raw_issue_data(self):
        params = {
            'since': self.synched_at.strftime(GH_DATE_FORMAT),
            'per_page': self.ISSUES_PAGE_SIZE,
            'sort': 'updated',
            'direction': 'asc',
            'state': 'all'  # include closed issues
        }

        auth = authorization()
        issues = requests.get(self.url() + 'issues', params=params, auth=auth)
        if issues.ok:
            result = {}
            new_issues = [i for i in issues.json()
                          if i['number'] not in result]
            while new_issues:
                result.update({i['number']: i for i in new_issues})
                # Github seems to be ignoring `sort` parameter, have to
                # check all results, alas
                params['since'] = self._latest_update(new_issues)
                issues = requests.get(self.url() + 'issues',
                                      params=params,
                                      auth=authorization())
                new_issues = [i
                              for i in issues.json()
                              if i['number'] not in result]
            return result.values()
        else:
            err_msg = 'Could not fetch issues for repo {}/{}: {}'.format(
                self.owner, self.name, issues.text)
            if not auth:
                err_msg += '\nNOTE: Environment variables GITHUB_USER and GITHUB_AUTH not set'
            raise FileNotFoundError(err_msg)

    def fetch_issues(self):
        """Refresh the database's store of issues for this repo from github."""
        for issue_data in self.raw_issue_data():
            issue = Issue.query.filter_by(
                number=issue_data.get('number')).first()
            if issue:
                db.session.delete(issue)
            db.session.commit()
            issue = Issue.from_raw(issue_data)
            issue.repo = self
            issue.fetch_events()
        self.synched_at = datetime.now()
        db.session.commit()

    def json_summary(self):
        result = dict(name=self.name,
                      owner=self.owner,
                      issues=[iss.json_summary() for iss in self.issues])
        return result

    def json_summary_flattened(self):
        spans = list(self.spans())
        result = dict(spans=spans,
                      stones=(self.stones()),
                      colors=[self.milestone_colors[s['span']['milestones'][
                          -1]] for s in spans], )
        return result

    def spans(self):
        for (idx, iss) in enumerate(self.issues):
            lifecycle = iss.lifecycle()
            for span in lifecycle['spans']:
                yield {'issue': iss,
                       'index': idx,
                       'span': span,
                       'final': lifecycle['final']}

    def stones(self):
        for (idx, iss) in enumerate(self.issues):
            lifecycle = iss.lifecycle()
            for stone in lifecycle['points']:
                yield {'issue': iss, 'index': idx, 'stone': stone}

    def milestones(self):
        "List of milestones in all issues, in rough order of first appearance"
        nested = [[e.milestone for e in i.events] for i in self.issues]
        all_milestones = list(OrderedDict.fromkeys(
            itertools.chain.from_iterable(nested)))
        if None in all_milestones:
            all_milestones.remove(None)
        return all_milestones

    _PALLETTE = ('greenyellow', 'cornflowerblue',
        'hotpink', 'indigo', 'fuschia',
        'green', 'lightskyblue', 'firebrick', 'gray', 'lightcoral',
        'darkslategray', 'darkorange', 'darkolivegreen',
        'cyan', 'chocolate', 'blueviolet', 'burlywood', 'aquamarine', )

    def set_milestone_color_map(self):
        "Decide a color to correspond to each type of milestone used in the repo"
        colors = itertools.cycle(self._PALLETTE) # reuse colors if too many milestones
        self.milestone_colors = {}
        for milestone in self.milestones():
            self.milestone_colors[milestone] = colors.__next__()
        self.milestone_colors.update({'opened': 'gold',
                                      'reopened': 'gold',
                                      'closed': 'black'})


labels_issues = db.Table(
    'labels_issues',
    db.Column('label_id', db.Integer, db.ForeignKey('label.id')),
    db.Column('issue_id', db.Integer, db.ForeignKey('issue.id')))


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer(), db.ForeignKey(Repo.id))
    number = db.Column(db.Integer)
    title = db.Column(db.String())
    body = db.Column(db.String())
    state = db.Column(db.String())
    creator_login = db.Column(db.String(),
                              db.ForeignKey('person.login'),
                              nullable=False)
    assignee_login = db.Column(db.String(),
                               db.ForeignKey('person.login'),
                               nullable=True)
    comments = db.Column(db.String())
    locked = db.Column(db.Boolean)
    url = db.Column(db.String(), nullable=True)
    events_url = db.Column(db.String(), nullable=True)
    labels_url = db.Column(db.String(), nullable=True)
    comments_url = db.Column(db.String(), nullable=True)
    html_url = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime(), default=date.today)
    updated_at = db.Column(db.DateTime(), default=date.today)
    closed_at = db.Column(db.DateTime(), nullable=True)
    labels = db.relationship('Label',
                             secondary=labels_issues,
                             backref=db.backref('issues',
                                                lazy='dynamic'))
    events = db.relationship('Event',
                             cascade='all, delete-orphan',
                             order_by='Event.created_at',
                             backref='issue')

    @classmethod
    def from_raw(cls, issue_data):
        insertable = {
            'id': issue_data.get('id'),
            'number': issue_data.get('number'),
            'title': issue_data.get('title'),
            'state': issue_data.get('state'),
            'body': issue_data.get('body'),
            'locked': issue_data.get('locked'),
            'url': issue_data.get('url'),
            'labels_url': issue_data.get('labels_url'),
            'html_url': issue_data.get('html_url'),
            'events_url': issue_data.get('events_url'),
            'updated_at': to_py_datetime(issue_data['updated_at']),
            'created_at': to_py_datetime(issue_data['created_at']),
            'closed_at': to_py_datetime(issue_data['closed_at']),
        }
        creator = Person.from_raw(issue_data['user'])
        insertable['creator_login'] = creator.login
        if issue_data.get('assignee'):
            assignee = Person.from_raw(issue_data['assignee'])
            insertable['assignee_login'] = assignee.login
        issue = cls(**insertable)
        for label_data in issue_data['labels']:
            issue.labels.append(Label.get_or_create(label_data))
        db.session.add(issue)
        return issue

    def fetch_events(self):
        response = requests.get('{}?per_page=100'.format(self.events_url),
                                auth=authorization())
        if self.number in (4, 17):
            from pprint import pprint
            with open('events{}.json'.format(self.number), 'w') as outfile:
                pprint(response.json(), outfile)
        # todo: if > 100 events?
        if response.ok:
            for raw_event in response.json():
                self.events.append(Event.from_raw(raw_event))

    def json_summary(self):

        lifecycle = self.lifecycle()

        return {
            'number': self.number,
            'title': self.title,
            'html_url': self.html_url,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'closed_at': self.closed_at,
            'spans': lifecycle['spans'],
            'points': lifecycle['points'],
        }

    def lifecycle(self):
        """Description of the events of this issue's lifecycle.

        Returns dict with:
        final: Last milestone marked
        points: (name, date) of milestones and open/close events
        spans: ([statuses], start date, end date) describing each time period
            in the issue's lifecycle.
        [statuses] is the list of milestones in effect.  The last in the list
            will generally be the one of interest.
        """
        statuses = ['opened', ]
        result = {'spans': [], 'final': 'opened', 'points': []}
        start_date = self.created_at
        for event in self.events:
            if event.event in ('milestoned', 'demilestoned', 'closed',
                               'reopened'):
                if event.milestone and event.milestone in statuses:
                    continue
                result['spans'].append({'milestones': statuses[:],
                                        'start': start_date,
                                        'end': event.created_at})
                if event.event == 'demilestoned':
                    try:
                        statuses.remove(event.milestone)
                    except ValueError:
                        pass  # sometimes they demilestone a nonexistent milestone!
                elif event.event == 'milestoned':
                    statuses.append(event.milestone)
                elif event.event in ('closed', 'reopened'):
                    statuses.append(event.event)
                result['points'].append({'status': statuses[-1],
                                         'at': event.created_at})
                start_date = event.created_at
        if self.closed_at:
            if statuses[-1] != 'closed':
                if self.closed_at > start_date:
                    result['spans'].append({'milestones': statuses[:],
                                            'start': start_date,
                                            'end': self.closed_at})
                result['points'].append({'status': 'closed',
                                         'at': self.closed_at})
        else:
            result['spans'].append({'milestones': statuses[:],
                                    'start': start_date,
                                    'end': datetime.now()})
        result['final'] = [s for s in statuses
                           if s not in ('closed', 'reopened')][-1]
        return result


class Person(db.Model):
    login = db.Column(db.String(), primary_key=True)
    url = db.Column(db.String(), nullable=True)
    created = db.relationship('Issue',
                              foreign_keys=[Issue.creator_login, ],
                              backref='author')
    assigned = db.relationship('Issue',
                               foreign_keys=[Issue.assignee_login, ],
                               backref='assignee')

    @classmethod
    def from_raw(cls, raw_data):
        person = cls.query.filter_by(login=raw_data['login']).first()
        if person:
            person.url = raw_data.get('url')
        else:
            person = cls(login=raw_data['login'], url=raw_data.get('url'))
        db.session.add(person)
        db.session.flush()  # TODO: ugh, all this flushing
        return person


class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    url = db.Column(db.String())
    color = db.Column(db.String(), nullable=True)

    @classmethod
    def get_or_create(cls, label_data):
        label = cls.query.filter_by(name=label_data['name']).first() \
                or cls(**label_data)
        return label


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    commit_id = db.Column(db.String())
    url = db.Column(db.String())
    actor = db.Column(db.String())
    event = db.Column(db.String())
    milestone = db.Column(db.String())
    created_at = db.Column(db.DateTime())
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))

    @classmethod
    def from_raw(cls, event_data):
        "Given dict of event data fetched from GitHub API, return instance"
        insertable = dict(
            id=event_data['id'],
            commit_id=event_data['commit_id'],
            url=event_data['url'],
            actor=event_data['actor'].get('login') if event_data[
                'actor'] else None,
            milestone=event_data.get('milestone') and event_data['milestone'][
                'title'],
            event=event_data['event'],
            created_at=to_py_datetime(event_data.get('created_at')), )
        return cls(**insertable)
