import json
import os

import flask_restful
from flask import Flask, make_response, render_template, request

from . import charts, models, utils

app = Flask(__name__)
api = flask_restful.Api(app)

servers = {"production": os.environ.get('PROD'),
           "staging": os.environ.get('STAGING')}


@app.route("/")
def usage():
    return "Usage: /repo_owner_name/repo_name/"


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
