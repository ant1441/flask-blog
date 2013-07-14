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
    try:
        with open(join(basedir, logging_cfg_file)) as config:
            logging.config.dictConfig(yaml.load(config))
    except IOError:
        logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("blog")

app = Flask(__name__)
config_object = 'Production'
#config_object = 'Testing'
app.config.from_object('blog.config.{}'.format(config_object))
db = SQLAlchemy(app)
admin = Admin(app, name='Blog')

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'

if __name__ == "blog":
    # If these are imported by nose, the coverage gets all buggered up.
    from blog import views, models, error_views, admin_views  # flake8: noqa
