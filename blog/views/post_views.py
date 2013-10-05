from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from flask.ext.login import current_user, login_required
from flask import (
    render_template, flash, redirect, url_for, abort)
from blog import app, db
from blog.forms import PostBlogForm
from blog.models import Post
from blog.utilities import to_json
from blog.views import log
from blog.db_layer import PostLogic


@app.route('/new_post/', methods=['GET', 'POST'])
@login_required
def new_post():
    """
    Create a new post.

    If :GET: present the form to submit a new post.
    If :POST:, if valid, submit the post and redirect to home.
    """
    form = PostBlogForm()
    if form.validate_on_submit():
        log.info("User %s submitted post %s",
                 current_user,
                 form.title.data)
        log.debug("CodeType: %s", form.code_type.data)
        if form.code_type.data is None:
            code = False
        else:
            code = True
        post = Post(title=form.title.data,
                    slug=form.slug.data,
                    content=form.text.data,
                    user=current_user,
                    code=code,
                    code_type=form.code_type.data,)
        db.session.add(post)
        try:
            db.session.commit()
        except IntegrityError as exc:
            if exc.message.endswith("not unique"):
                log.error("Post '%s' was not unique in field '%s'",
                          form.title.data,
                          exc.message
                          .split(" ", 2)[-1].rsplit(" ", 3)[0])
            else:
                log.critical("Unknown Integrity Error with post '%s'",
                             form.title.data,
                             exc_info=True)
            db.session.rollback()
            flash("Integrity Error!", 'error')
            return render_template("post/make_post.html",
                                   title="Post Blog",
                                   form=form)
        except:
            log.critical("Exception on %s [%s]",
                         'page',
                         'method',
                         exc_info=True)
            db.session.rollback()
            abort(500)
        flash("{} submitted {}.".format(
            current_user.username,
            form.title.data), 'success')
        return redirect(url_for('index'))
    return render_template("post/make_post.html",
                           title="Post Blog",
                           form=form)


def get_post(post_id=None, slug=None):
    if slug:
        if post_id:
            abort(500)
        return (PostLogic.query
                .filter_by(slug=slug)
                .filter(PostLogic.visible)
                .one())
    elif post_id:
        return (PostLogic.query
                .filter_by(id=post_id)
                .filter(PostLogic.visible)
                .one())


@app.route('/post/<int:post_id>/')
@app.route('/post/<slug>/')
def post(post_id=None, slug=None):
    try:
        _post = get_post(post_id, slug)
    except NoResultFound:
        abort(404)
    log.debug("post: %s", _post)
    return render_template("post/post_page.html",
                           post=_post)


@app.route('/post/<int:post_id>.json')
@app.route('/post/<slug>.json')
def json_post(post_id=None, slug=None):
    try:
        _post = get_post(post_id, slug)
    except NoResultFound:
        abort(404)
    _post = to_json(_post)
    log.debug("post: %s", _post)
    return _post
