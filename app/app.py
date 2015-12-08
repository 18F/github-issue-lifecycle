import json
import os
from datetime import timedelta
from functools import wraps

import requests
from flask import Flask, Response, make_response, render_template, request
from sassutils.wsgi import SassMiddleware
from waitress import serve

from . import charts, models

app = Flask(__name__)
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


def load_data(owner_name, repo_name):
    repo = models.Repo.get_fresh(owner_name=owner_name, repo_name=repo_name)
    repo.set_milestone_color_map()
    return {'chart': charts.lifecycles(repo)}


@requires_auth
@app.route("/<owner>/<repo>/")
def index(owner, repo):
    try:
        data = load_data(owner, repo)
    except FileNotFoundError as e:
        return render_template("err.html",
                               data={'owner': owner,
                                     'repo': repo,
                                     'err': e}), 404
    return render_template("index.html",
                           data=load_data(owner, repo),
                           error=error)


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
