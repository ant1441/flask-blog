import sys
import os
import logging
import logging.config
import yaml

__version__ = '0.4-2'

CONFIG = "config.yaml"


try:
    with open(CONFIG) as config:
        GLOBAL_CONFIG = yaml.load(config)
    # import logging configuration
    logging.config.dictConfig(GLOBAL_CONFIG['logging'])
except IOError:
    with open("/var/local/blog/config.yaml") as config:
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

log = logging.getLogger(__name__)

from blog.views import (
    views, login_views, error_views, admin_views, post_views)
from blog.models import Category, Post, User, CodeType

from blog.utilities import parse
app.jinja_env.filters['parse'] = parse
