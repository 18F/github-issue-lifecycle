# github-issue-lifecycle
Serve data on lifecycle (open -> milestones -> close) of a repo's issues

<a href="https://travis-ci.org/18F/github-issue-lifecycle">
  <img src="https://travis-ci.org/18F/github-issue-lifecycle.svg?branch=master" alt="TravisCI" />
</a>

<a href="https://codecov.io/github/18F/github-issue-lifecycle?branch=master">
  <img src="https://codecov.io/github/18F/github-issue-lifecycle/coverage.svg?branch=master" alt="Code Coverage"/>
</a>

Summarizes the events in a Github repository's issues.
Output is available as

- An API (`/api/<owner>/repo/`), returning for each issue a list of `spans` -
time periods defined by the milestones in effect during that time

- A [Bokeh](http://bokeh.pydata.org/) graph (`/<owner>/<repo>/`)
illustrating each issue as a horizontal bar, with
a different color for each span.  The bars show milestone and assignee information
when hovered over, and are hyperlinked to the issues' pages at Github.

To run the development server:

1. Create and activate a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html)

1. Install [PostgreSQL](http://www.postgresql.org/)
(other SQLAlchemy-compatible databases are OK, too, if you modify `config.py`
appropriately)

1. Run `pip install -r requirements.txt`

1. `createdb github-issues-dev`

1. Run `python setup.py db upgrade` to create the database tables.

1. Run `python manage.py deploy`

1. Visit http://0.0.0.0:5000/<owner><repo>/

If you want to report on a private repository, set the environment
variables `GITHUB_USER` and `GITHUB_AUTH`.  This will also protect your
server for running up against Github's unauthenticated API usage
limits. 

The local server stores information queried from Github in a local
PostgreSQL database, so that it will save web traffic and load on
Github.  The server will rely entirely on locally stored data if its
last query to Github was more than `REFRESH_THRESHHOLD_SECONDS`
ago, a constant stored in `config.py` (default 1 hour).
