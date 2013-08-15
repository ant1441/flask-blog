from sqlalchemy.exc import IntegrityError
from flask.ext.login import current_user, login_required
from flask import (
    render_template, flash, redirect, url_for, abort)
from blog import app, db
from blog.forms import PostBlogForm
from blog.models import Post
from blog.views import log


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
            return render_template("make_post.html",
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
