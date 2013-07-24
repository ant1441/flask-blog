import time
from sqlalchemy.exc import IntegrityError, OperationalError
from flask.ext.login import (
        login_user, logout_user, current_user, login_required)
from flask import (
        render_template, flash, redirect, url_for, g, request, abort)
from werkzeug.security import check_password_hash
from blog import app, lm, db
from blog.forms import postBlogForm, loginForm
from blog.models import User, Post


@app.before_request
def before_request():
    # For page generation timing
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (
        time.time() - g.request_start_time)


# begin general views
@app.route('/')
def index():
    try:
        posts = Post.query.order_by(Post.created_at.desc()).all()
    except OperationalError:
        app.logger.critical("Database file: %s",
                            app.config['SQLALCHEMY_DATABASE_URI'],
                            exc_info=True)
        raise
    return render_template("index.html",
                           title="Home",
                           posts=posts)


@app.route('/new_post/', methods=['GET', 'POST'])
@login_required
def new_post():
    """
    Create a new post.

    If :GET: present the form to submit a new post.
    If :POST:, if valid, submit the post and redirect to home.
    """
    form = postBlogForm()
    if form.validate_on_submit():
        app.logger.info("User %s submitted post %s",
                        current_user,
                        form.title.data)
        db.session.add(
            Post(title=form.title.data,
                 slug=form.slug.data,
                 content=form.text.data,
                 user=current_user,
                 code=form.code.data,
                 ))
        try:
            db.session.commit()
        except IntegrityError as exc:
            if exc.message.endswith("not unique"):
                app.logger.error("Post '%s' was not unique in field '%s'",
                                 form.title.data,
                                 exc.message
                                 .split(" ", 2)[-1].rsplit(" ", 3)[0])
            else:
                app.logger.critical("Unknown Integrity Error with post '%s'",
                                    form.title.data,
                                    exc_info=True)
            db.session.rollback()
            flash("Integrity Error!", 'error')
            return render_template("make_post.html",
                                   title="Post Blog",
                                   form=form)
        except:
            app.logger.critical("Exception on %s [%s]",
                                'page',
                                'method',
                                exc_info=True)
            db.session.rollback()
            abort(500)
        flash("{} submitted {}.".format(
            current_user.username,
            form.title.data), 'success')
        return redirect(url_for('index'))
    return render_template("make_post.html",
                           title="Post Blog",
                           form=form)


@app.route('/post/<int:post_id>')
@app.route('/post/<slug>')
def post(post_id=None, slug=None):
    if slug:
        if post_id:
            abort(500)
        post = Post.query.filter_by(slug=slug).first_or_404()
    elif post_id:
        post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template("post_page.html",
                           post=post)


# begin login related views and functions
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


def try_login(user, password):
    if check_password_hash(user.password, password):
        return True
    return False


# url routing
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user.data).first()
        if user:
            if try_login(user, str(form.password.data)):
                flash('Logged in successfully!', 'success')
                app.logger.info("User %s logged in", user)
                login_user(user, remember=form.remember_me.data)
                return redirect(request.args.get("next") or url_for("index"))
            else:
                app.logger.warn("Log in attempt to '%s' from IP %s",
                                user,
                                request.remote_addr)
        else:
            app.logger.warn("Log in attempt to '%s' from IP %s",
                            form.user.data,
                            request.remote_addr)
            flash('User not found!', 'error')
    return render_template('login.html',
                           title="Log In",
                           form=form)


@app.route('/logout/')
def logout():
    logout_user()
    #flash("Successfully logged out!")
    return redirect(url_for('index'))
