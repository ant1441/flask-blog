from sqlalchemy.exc import OperationalError
from flask import render_template
from blog import app
from blog.models import Post
from blog.views import log


# begin general views
@app.route('/')
def index():
    try:
        posts = Post.query.order_by(Post.created_at.desc()).all()
    except OperationalError:
        log.critical("Database file: %s",
                     app.config['SQLALCHEMY_DATABASE_URI'],
                     exc_info=True)
        raise
    return render_template("index.html",
                           title="Home",
                           posts=posts)
