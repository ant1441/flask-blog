from sqlalchemy.exc import OperationalError
from flask import render_template
from blog import app
from blog.views import log
from blog.db_layer import PostLogic


# begin general views
@app.route('/')
def index():
    try:
        posts = (PostLogic.query
                 .filter(PostLogic.visible)
                 .order_by(PostLogic.created_at.desc())
                 .all())
    except OperationalError:
        log.critical("Database file: %s",
                     app.config['SQLALCHEMY_DATABASE_URI'],
                     exc_info=True)
        raise
    return render_template("index.html",
                           title="Home",
                           posts=posts)


@app.route('/about')
def about():
    return "About Me"
