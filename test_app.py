import unittest
from unittest import mock
import responses
import requests
import re

from app import db, models
from app.app import app
from config import config
from mock_github import issues_json, events_json

from flask.ext.testing import TestCase

app.config.from_object(config['testing'])

class AppTestCase(TestCase):

    bad_url = re.compile(".*?/doesnot/exist/")

    def create_app(self):
        app.config.from_object(config['testing'])
        return app

    def setUp(self):

        def requests_get_stub(*args, **kwargs):
            response = self.client.get.return_value
            if '/doesnot/exist/' in args[0]:
                response.status_code = 404
                return response
            if '/events/' in args[0]:
                response.json.return_value = events_json
            else:
                response.json.return_value = issues_json
            response.ok = True
            response.status_code = 200
            return response

        self.client.get = mock.MagicMock(side_effect=requests_get_stub)

        db.init_app(app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_nonexistent_repo(self):
        resp = self.client.get('/doesnot/exist/')
        assert resp.status_code == 404

    def test_real_repo(self):
        url = '/api/real/repo/'
        resp = self.client.get(url)
        assert 'title' in resp.json()[0]

if __name__ == '__main__':
    unittest.main()
