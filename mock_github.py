import re

import requests

events_url_pattern = re.compile(r'issues/(\d+)/events')


def requests_get_stub(*args, **kwargs):
    response = requests.get.return_value

    if '/doesnot/exist/' in args[0]:
        response.status_code = 404
        response.ok = False
        response.text = 'Repo not found'
        return response

    events_for_issue_num = events_url_pattern.search(args[0])
    if events_for_issue_num:
        issue_num = int(events_for_issue_num.group(1))
        response.json.return_value = events_json[issue_num]
    else:
        response.json.return_value = issues_json
    response.ok = True
    response.status_code = 200
    return response


issues_json = [
    {'assignee':
     {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
      'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
      'followers_url': 'https://api.github.com/users/quepol/followers',
      'following_url':
      'https://api.github.com/users/quepol/following{/other_user}',
      'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
      'gravatar_id': '',
      'html_url': 'https://github.com/quepol',
      'id': 1841120,
      'login': 'quepol',
      'organizations_url': 'https://api.github.com/users/quepol/orgs',
      'received_events_url':
      'https://api.github.com/users/quepol/received_events',
      'repos_url': 'https://api.github.com/users/quepol/repos',
      'site_admin': False,
      'starred_url':
      'https://api.github.com/users/quepol/starred{/owner}{/repo}',
      'subscriptions_url': 'https://api.github.com/users/quepol/subscriptions',
      'type': 'User',
      'url': 'https://api.github.com/users/quepol'},
     'body': '# 29 minutes\r\n'
          '*From: Aaron Snow*\r\n'
          '\r\n'
          'I want to relate a great little thing that happened here at [18th '
          'and F](http://gsa.gov/) yesterday.\r\n',
     'closed_at': '2014-03-26T04:01:54Z',
     'comments': 3,
     'comments_url':
     'https://api.github.com/repos/18F/blog-drafts/issues/4/comments',
     'created_at': '2014-03-25T07:07:18Z',
     'events_url':
     'https://api.github.com/repos/18F/blog-drafts/issues/4/events',
     'html_url': 'https://github.com/18F/blog-drafts/issues/4',
     'id': 30101124,
     'labels': [
         {'color': 'bfe5bf',
          'name': 'how we work',
          'url':
          'https://api.github.com/repos/18F/blog-drafts/labels/how%20we%20work'
          }
     ],
     'labels_url':
     'https://api.github.com/repos/18F/blog-drafts/issues/4/labels{/name}',
     'locked': False,
     'milestone':
     {'closed_at': None,
      'closed_issues': 140,
      'created_at': '2014-03-25T06:52:47Z',
      'creator':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'description': 'posts that have been written, edited, and '
                               'approved for posting',
      'due_on': None,
      'html_url': 'https://github.com/18F/blog-drafts/milestones/approved',
      'id': 608934,
      'labels_url':
      'https://api.github.com/repos/18F/blog-drafts/milestones/2/labels',
      'number': 2,
      'open_issues': 0,
      'state': 'open',
      'title': 'approved',
      'updated_at': '2015-12-09T16:48:40Z',
      'url': 'https://api.github.com/repos/18F/blog-drafts/milestones/2'},
     'number': 4,
     'state': 'closed',
     'title': 'Story about FBOpen and m.gsa.gov',
     'updated_at': '2014-03-29T05:21:10Z',
     'url': 'https://api.github.com/repos/18F/blog-drafts/issues/4',
     'user':
     {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
      'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
      'followers_url': 'https://api.github.com/users/quepol/followers',
      'following_url':
      'https://api.github.com/users/quepol/following{/other_user}',
      'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
      'gravatar_id': '',
      'html_url': 'https://github.com/quepol',
      'id': 1841120,
      'login': 'quepol',
      'organizations_url': 'https://api.github.com/users/quepol/orgs',
      'received_events_url':
      'https://api.github.com/users/quepol/received_events',
      'repos_url': 'https://api.github.com/users/quepol/repos',
      'site_admin': False,
      'starred_url':
      'https://api.github.com/users/quepol/starred{/owner}{/repo}',
      'subscriptions_url': 'https://api.github.com/users/quepol/subscriptions',
      'type': 'User',
      'url': 'https://api.github.com/users/quepol'}},
    {'assignee':
     {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
      'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
      'followers_url': 'https://api.github.com/users/quepol/followers',
      'following_url':
      'https://api.github.com/users/quepol/following{/other_user}',
      'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
      'gravatar_id': '',
      'html_url': 'https://github.com/quepol',
      'id': 1841120,
      'login': 'quepol',
      'organizations_url': 'https://api.github.com/users/quepol/orgs',
      'received_events_url':
      'https://api.github.com/users/quepol/received_events',
      'repos_url': 'https://api.github.com/users/quepol/repos',
      'site_admin': False,
      'starred_url':
      'https://api.github.com/users/quepol/starred{/owner}{/repo}',
      'subscriptions_url': 'https://api.github.com/users/quepol/subscriptions',
      'type': 'User',
      'url': 'https://api.github.com/users/quepol'},
     'body':
     'Blog post about the Github AMA this week. Got questions about 18F '
          'and the PIF program? Come ask us!',
     'closed_at': '2014-04-01T20:00:44Z',
     'comments': 2,
     'comments_url':
     'https://api.github.com/repos/18F/blog-drafts/issues/17/comments',
     'created_at': '2014-04-01T18:43:14Z',
     'events_url':
     'https://api.github.com/repos/18F/blog-drafts/issues/17/events',
     'html_url': 'https://github.com/18F/blog-drafts/issues/17',
     'id': 30625911,
     'labels': [],
     'labels_url':
     'https://api.github.com/repos/18F/blog-drafts/issues/17/labels{/name}',
     'locked': False,
     'milestone':
     {'closed_at': None,
      'closed_issues': 140,
      'created_at': '2014-03-25T06:52:47Z',
      'creator':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'description': 'posts that have been written, edited, and '
                               'approved for posting',
      'due_on': None,
      'html_url': 'https://github.com/18F/blog-drafts/milestones/approved',
      'id': 608934,
      'labels_url':
      'https://api.github.com/repos/18F/blog-drafts/milestones/2/labels',
      'number': 2,
      'open_issues': 0,
      'state': 'open',
      'title': 'approved',
      'updated_at': '2015-12-09T16:48:40Z',
      'url': 'https://api.github.com/repos/18F/blog-drafts/milestones/2'},
     'number': 17,
     'state': 'closed',
     'title': 'Github AMA',
     'updated_at': '2014-04-01T20:00:44Z',
     'url': 'https://api.github.com/repos/18F/blog-drafts/issues/17',
     'user':
     {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
      'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
      'followers_url': 'https://api.github.com/users/quepol/followers',
      'following_url':
      'https://api.github.com/users/quepol/following{/other_user}',
      'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
      'gravatar_id': '',
      'html_url': 'https://github.com/quepol',
      'id': 1841120,
      'login': 'quepol',
      'organizations_url': 'https://api.github.com/users/quepol/orgs',
      'received_events_url':
      'https://api.github.com/users/quepol/received_events',
      'repos_url': 'https://api.github.com/users/quepol/repos',
      'site_admin': False,
      'starred_url':
      'https://api.github.com/users/quepol/starred{/owner}{/repo}',
      'subscriptions_url': 'https://api.github.com/users/quepol/subscriptions',
      'type': 'User',
      'url': 'https://api.github.com/users/quepol'}}
]

events_json = {
    4:
    [{'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-25T07:07:23Z',
      'event': 'milestoned',
      'id': 105106022,
      'milestone': {'title': 'posted'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/105106022'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-25T07:09:14Z',
      'event': 'labeled',
      'id': 105106349,
      'label': {'color': 'f7c6c7',
                'name': 'fbopen'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/105106349'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/565152?v=3',
       'events_url': 'https://api.github.com/users/aaronsnow/events{/privacy}',
       'followers_url': 'https://api.github.com/users/aaronsnow/followers',
       'following_url':
       'https://api.github.com/users/aaronsnow/following{/other_user}',
       'gists_url': 'https://api.github.com/users/aaronsnow/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/aaronsnow',
       'id': 565152,
       'login': 'aaronsnow',
       'organizations_url': 'https://api.github.com/users/aaronsnow/orgs',
       'received_events_url':
       'https://api.github.com/users/aaronsnow/received_events',
       'repos_url': 'https://api.github.com/users/aaronsnow/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/aaronsnow/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/aaronsnow/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/aaronsnow'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-25T20:18:21Z',
      'event': 'closed',
      'id': 105389265,
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/105389265'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1328699?v=3',
       'events_url': 'https://api.github.com/users/amoose/events{/privacy}',
       'followers_url': 'https://api.github.com/users/amoose/followers',
       'following_url':
       'https://api.github.com/users/amoose/following{/other_user}',
       'gists_url': 'https://api.github.com/users/amoose/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/amoose',
       'id': 1328699,
       'login': 'amoose',
       'organizations_url': 'https://api.github.com/users/amoose/orgs',
       'received_events_url':
       'https://api.github.com/users/amoose/received_events',
       'repos_url': 'https://api.github.com/users/amoose/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/amoose/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/amoose/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/amoose'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-26T01:23:19Z',
      'event': 'reopened',
      'id': 105478781,
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/105478781'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'assignee':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-26T03:18:05Z',
      'event': 'assigned',
      'id': 105495794,
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/105495794'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-26T03:59:55Z',
      'event': 'milestoned',
      'id': 105501905,
      'milestone': {'title': 'posted'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/105501905'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-26T03:59:55Z',
      'event': 'demilestoned',
      'id': 105501906,
      'milestone': {'title': 'posted'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/105501906'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1328699?v=3',
       'events_url': 'https://api.github.com/users/amoose/events{/privacy}',
       'followers_url': 'https://api.github.com/users/amoose/followers',
       'following_url':
       'https://api.github.com/users/amoose/following{/other_user}',
       'gists_url': 'https://api.github.com/users/amoose/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/amoose',
       'id': 1328699,
       'login': 'amoose',
       'organizations_url': 'https://api.github.com/users/amoose/orgs',
       'received_events_url':
       'https://api.github.com/users/amoose/received_events',
       'repos_url': 'https://api.github.com/users/amoose/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/amoose/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/amoose/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/amoose'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-26T04:01:54Z',
      'event': 'mentioned',
      'id': 105502170,
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/105502170'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1328699?v=3',
       'events_url': 'https://api.github.com/users/amoose/events{/privacy}',
       'followers_url': 'https://api.github.com/users/amoose/followers',
       'following_url':
       'https://api.github.com/users/amoose/following{/other_user}',
       'gists_url': 'https://api.github.com/users/amoose/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/amoose',
       'id': 1328699,
       'login': 'amoose',
       'organizations_url': 'https://api.github.com/users/amoose/orgs',
       'received_events_url':
       'https://api.github.com/users/amoose/received_events',
       'repos_url': 'https://api.github.com/users/amoose/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/amoose/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/amoose/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/amoose'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-26T04:01:54Z',
      'event': 'subscribed',
      'id': 105502171,
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/105502171'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-26T04:01:54Z',
      'event': 'closed',
      'id': 105502172,
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/105502172'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-26T04:52:53Z',
      'event': 'labeled',
      'id': 105508695,
      'label': {'color': '009800',
                'name': 'how we work'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/105508695'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-29T05:19:07Z',
      'event': 'demilestoned',
      'id': 106705064,
      'milestone': {'title': 'posted'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/106705064'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-03-29T05:21:10Z',
      'event': 'milestoned',
      'id': 106705168,
      'milestone': {'title': 'approved'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/106705168'}],
    17:
    [{'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-04-01T18:43:14Z',
      'event': 'milestoned',
      'id': 107595720,
      'milestone': {'title': 'idea'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/107595720'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'assignee':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-04-01T18:43:14Z',
      'event': 'assigned',
      'id': 107595721,
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/107595721'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-04-01T18:43:21Z',
      'event': 'milestoned',
      'id': 107595759,
      'milestone': {'title': 'draft'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/107595759'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-04-01T18:43:21Z',
      'event': 'demilestoned',
      'id': 107595760,
      'milestone': {'title': 'idea'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/107595760'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-04-01T20:00:27Z',
      'event': 'milestoned',
      'id': 107628074,
      'milestone': {'title': 'approved'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/107628074'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-04-01T20:00:27Z',
      'event': 'demilestoned',
      'id': 107628075,
      'milestone': {'title': 'draft'},
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/107628075'},
     {'actor':
      {'avatar_url': 'https://avatars.githubusercontent.com/u/1841120?v=3',
       'events_url': 'https://api.github.com/users/quepol/events{/privacy}',
       'followers_url': 'https://api.github.com/users/quepol/followers',
       'following_url':
       'https://api.github.com/users/quepol/following{/other_user}',
       'gists_url': 'https://api.github.com/users/quepol/gists{/gist_id}',
       'gravatar_id': '',
       'html_url': 'https://github.com/quepol',
       'id': 1841120,
       'login': 'quepol',
       'organizations_url': 'https://api.github.com/users/quepol/orgs',
       'received_events_url':
       'https://api.github.com/users/quepol/received_events',
       'repos_url': 'https://api.github.com/users/quepol/repos',
       'site_admin': False,
       'starred_url':
       'https://api.github.com/users/quepol/starred{/owner}{/repo}',
       'subscriptions_url':
       'https://api.github.com/users/quepol/subscriptions',
       'type': 'User',
       'url': 'https://api.github.com/users/quepol'},
      'commit_id': None,
      'commit_url': None,
      'created_at': '2014-04-01T20:00:44Z',
      'event': 'closed',
      'id': 107628198,
      'url':
      'https://api.github.com/repos/18F/blog-drafts/issues/events/107628198'}]
}
