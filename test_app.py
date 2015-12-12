import unittest
from unittest import mock

import requests
from flask.ext.testing import TestCase

from app import db, models
from app.app import app
from config import config
from mock_github import requests_get_stub

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

    def test_nonexistent_repo(self):
        resp = self.client.get('/api/doesnot/exist/')
        assert resp.status_code == 404


if __name__ == '__main__':
    unittest.main()
