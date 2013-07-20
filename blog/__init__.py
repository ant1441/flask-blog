import os
from os.path import join
import logging
import logging.config
import yaml
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.admin import Admin
from blog.config import basedir

CONFIG = os.getenv("LOG_CFG", "config.yaml")
with open(join(basedir, CONFIG)) as config:
    GLOBAL_CONFIG = yaml.load(config)
# import logging configuration
try:
    logging.config.dictConfig(GLOBAL_CONFIG['logging'])
except (IOError,NameError):
    print "ERROR"
    logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
app.logger.info("from app")
app.config.from_object('blog.config.{}'.format(GLOBAL_CONFIG['environment']))
db = SQLAlchemy(app)
admin = Admin(app, name='Blog')

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

if __name__ == "blog":
    # If these are imported by nose, the coverage gets all buggered up.
    from blog import views, error_views, admin_views  # flake8: noqa
    from blog.models import *
