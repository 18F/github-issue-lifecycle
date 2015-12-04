from datetime import date, datetime
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

        issues = requests.get(self.url() + 'issues',
                              params=params,
                              auth=authorization())
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

    def fetch_issues(self):
        for issue_data in self.raw_issue_data():
            issue = Issue.query.filter_by(
                number=issue_data.get('number')).first()
            if issue:
                db.session.delete(issue)
            db.session.commit()
            issue = Issue.from_raw(issue_data)
            issue.repo = self
            issue.fetch_events()


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
        response = requests.get('{}issues/{}/events?per_page=100'.format(
            self.repo.url(), self.number),
                                auth=authorization())
        # todo: if > 100 events?
        if response.ok:
            for raw_event in response.json():
                self.events.append(Event.from_raw(raw_event))

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
                result['spans'].append((statuses[:], start_date,
                                        event.created_at))
                if event.event == 'demilestoned':
                    statuses.remove(event.milestone)
                elif event.event == 'milestoned':
                    statuses.append(event.milestone)
                elif event.event in ('closed', 'reopened'):
                    statuses.append(event.event)
                result['points'].append((statuses[-1], event.created_at))
                start_date = event.created_at
        if self.closed_at:
            if statuses[-1] != 'closed':
                if self.closed_at > start_date:
                    result['spans'].append((statuses[:], start_date,
                                            event.created_at))
                result['points'].append(('closed', self.closed_at))
        else:
            result['spans'].append((statuses[:], start_date, datetime.now()))
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
