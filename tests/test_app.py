import unittest
from unittest import mock

import requests
from flask.ext.testing import TestCase

from app import db, models
from app.app import app
from config import config
from .mock_github import requests_get_stub

app.config.from_object(config['testing'])


class AppTestCase(TestCase):
    def create_app(self):
        app.config.from_object(config['testing'])
        return app

    def setUp(self):
        requests.get = mock.MagicMock(side_effect=requests_get_stub)
        db.init_app(app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_repo_retrieved(self):
        url = '/api/real/repo/'
        resp = self.client.get(url)
        assert resp.json['owner'] == 'real'
        assert resp.json['name'] == 'repo'
        assert len(resp.json['issues']) == 2

    def test_repo_includes_spans(self):
        resp = self.client.get('/api/real/repo/')
        assert 'spans' in resp.json['issues'][0]
        assert 'milestones' in resp.json['issues'][0]['spans'][0]

    def test_repo_persisted(self):
        owner = '18f'
        name = 'fictionalrepo1'
        assert not models.Repo.query.filter_by(owner=owner, name=name).first()
        resp = self.client.get('/api/{}/{}/'.format(owner, name))
        repo = models.Repo.query.filter_by(owner=owner, name=name).first()
        assert repo
        assert len(repo.issues) == 2

    def test_cached_data_used(self):
        owner = '18f'
        name = 'fictionalrepo2'
        resp = self.client.get('/api/{}/{}/'.format(owner, name))
        calls_before = requests.get.call_count
        resp = self.client.get('/api/{}/{}/?data_age=3600'.format(owner, name))
        assert requests.get.call_count == calls_before

    def test_cached_data_not_used(self):
        owner = '18f'
        name = 'fictionalrepo2'
        resp = self.client.get('/api/{}/{}/'.format(owner, name))
        calls_before = requests.get.call_count
        resp = self.client.get('/api/{}/{}/?data_age=0'.format(owner, name))
        assert requests.get.call_count > calls_before

    def test_nonexistent_repo(self):
        resp = self.client.get('/api/doesnot/exist/')
        assert resp.status_code == 404

    def test_chart_served(self):
        owner = '18f'
        name = 'fictionalrepo2'
        resp = self.client.get('/{}/{}/'.format(owner, name))
        assert resp.status_code == 200
        assert 'text/html; charset=utf-8' in resp.headers.values()
        assert b'Bokeh' in resp.data


if __name__ == '__main__':
    unittest.main()
