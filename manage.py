import os
from datetime import date, timedelta
from os import environ, path, stat

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager
from waitress import serve

from app import db, models
from app.app import app
from config import config

config_name = os.getenv('FLASK_CONFIG') or 'default'
app.logger.info('Using FLASK_CONFIG {0} from environment'.format(config_name))
app.config.from_object(config[config_name])
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

app.debug = (environ.get('ENV') == 'local')


@manager.command
def deploy():
    port = int(environ.get("VCAP_APP_PORT") or app.config['PORT'])
    serve(app, port=port)


@manager.command
def cleandata():
    "Deletes *all* stored data"
    for tbl in reversed(db.metadata.sorted_tables):
        db.engine.execute(tbl.delete())


@manager.command
def update(owner_name, repo_name):
    models.Repo.get_fresh(owner_name=owner_name,
                          repo_name=repo_name,
                          refresh_threshhold_seconds=0)


if __name__ == "__main__":
    manager.run()
