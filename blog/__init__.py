import sys
import os
import logging
import logging.config
import yaml

__version__ = "0.3"

CONFIG = os.getenv("LOG_CFG", "development.yaml")


try:
    with open(CONFIG) as config:
        GLOBAL_CONFIG = yaml.load(config)
# import logging configuration
    logging.config.dictConfig(GLOBAL_CONFIG['logging'])
except:
    sys.stderr.write("ERROR loading configuration\n")
    raise

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.admin import Admin


app = Flask(__name__)
app.config.update(**GLOBAL_CONFIG['flask'])
db = SQLAlchemy(app)
admin = Admin(app, name='Blog')

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

if __name__ == "blog":
    # If these are imported by nose, the coverage gets all buggered up.
    from blog import views, error_views, admin_views  # flake8: noqa
    from blog.models import *
