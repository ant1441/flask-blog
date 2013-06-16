import logging
import logging.config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.admin import Admin

logging_cfg_file = None

# import logging configuration
if logging_cfg_file:
    logging.config.fileConfig(logging_cfg_file)
else:
    logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
admin = Admin(app, name='Blog')

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

from app import views, models, error_views, admin_views
