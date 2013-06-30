from os.path import join
import logging
import logging.config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.admin import Admin
from blog.config import basedir

logging_cfg_file = "logging.cfg"

# import logging configuration
if logging_cfg_file:
    import yaml
    with open(join(basedir, logging_cfg_file)) as config:
        logging.config.dictConfig(yaml.load(config))
else:
    logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("blog")

app = Flask(__name__)
config_object = 'Testing'
app.config.from_object('blog.config.{}'.format(config_object))
db = SQLAlchemy(app)
admin = Admin(app, name='Blog')

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

from blog import views, models, error_views, admin_views
