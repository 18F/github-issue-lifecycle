import json
import os
from functools import wraps

import requests
from flask import Flask, Response, make_response, render_template, request
import flask_restful
from sassutils.wsgi import SassMiddleware

from . import charts, models, utils

app = Flask(__name__)
api = flask_restful.Api(app)
scss_manifest = {app.name: ('static/_scss', 'static/css')}
# Middleware
app.wsgi_app = SassMiddleware(app.wsgi_app, scss_manifest)

servers = {"production": os.environ.get('PROD'),
           "staging": os.environ.get('STAGING')}


# htpasswd configuration c/o http://flask.pocoo.org/snippets/8/
def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == os.environ['HTUSER'] and password == os.environ[
        'HTAUTH']


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@requires_auth
@app.route("/<owner>/<repo>/")
def index(owner, repo):
    data_age = request.args.get('data_age') or app.config[
        'REFRESH_THRESHHOLD_SECONDS']
    try:
        repo = models.Repo.get_fresh(owner_name=owner,
                                     repo_name=repo,
                                     refresh_threshhold_seconds=int(data_age))
        repo.set_milestone_color_map()
        chart = charts.lifecycles(repo.json_summary_flattened())
        return render_template("index.html", data={'chart': chart})
    except FileNotFoundError as e:
        return render_template("err.html",
                               data={'owner': owner,
                                     'repo': repo,
                                     'err': e}), 404


@app.route("/manage/")
@requires_auth
def manage():
    error = None
    if request.args.get('rebuild'):
        server = request.args.get('rebuild')
        url = servers[server]
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = {"ref": "refs/heads/%s" % server}
        requests.post(url, data=json.dumps(payload), headers=headers)
    else:
        error = "No server to rebuild"
    return render_template("manage.html", error=error)


@api.representation('application/json')
def output_json(data, code, headers=None):
    "Serializes dates in ISO8601 format"
    resp = make_response(
        json.dumps(data,
                   cls=utils.ISO8601JSONEncoder,
                   indent=2),
        code)
    resp.headers.extend(headers or {})
    return resp


class Api(flask_restful.Resource):
    def get(self, owner=None, repo=None):
        """Return JSON representation of lifecycle info from repo `owner.repo`."""

        data_age = request.args.get('data_age') or app.config[
            'REFRESH_THRESHHOLD_SECONDS']
        if not owner or not repo:
            return {'Usage': '/api/<owner>/<repo>/'}
        try:
            repo = models.Repo.get_fresh(
                owner_name=owner,
                repo_name=repo,
                refresh_threshhold_seconds=int(data_age))
        except FileNotFoundError as e:
            raise flask_restful.NotFound(e)
        return repo.json_summary()


api.add_resource(Api, '/api/<owner>/<repo>/')

# TODO: legend on chart
# TODO: tests
