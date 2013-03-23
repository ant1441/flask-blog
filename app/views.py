from flask import render_template, flash, redirect, url_for, g, request, abort, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqlamodel import ModelView
from app import app, lm, db, admin
from forms import postBlogForm, loginForm
from models import User, Post, Category
from hashlib import md5
import time
import datetime

@app.before_request
def before_request():
    # For page generation timing
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


# begin general views
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template("index.html",
            title="Home",
            posts=posts)

@app.route('/new_post/', methods=['GET', 'POST'])
@login_required
def newPost():
    form = postBlogForm()
    if form.validate_on_submit():
        flash("Posting from author %s." % form.author.data or current_user.username)
        db.session.add(
                Post(title=form.title.data,
                    content=form.text.data,
                    user=current_user,
                    code=form.code.data,
                    ))
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("make_post.html",
                            title="Post Blog",
                            form=form)

#@app.route('/post/', defaults={'post_id': int(Post.query.order_by(Post.created_at).limit(1).id)})
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.filter_by(id = post_id).first_or_404()
    return render_template("post_page.html",
                            post=post)


# begin login related views and functions
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

def try_login(user, password):
    if password == user.password:
        return True
    return False

# url routing
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user.data).first()
        if user:
            if try_login(user, md5(form.password.data).hexdigest()):
                flash('Logged in successfully!')
                login_user(user, remember=form.remember_me.data)
                return redirect(request.args.get("next") or url_for("index"))
        else:
            flash('User not found!')
    return render_template('login.html',
            title="Log In",
            form = form)

@app.route('/logout/')
def logout():
    logout_user()
    #flash("Successfully logged out!")
    return redirect(url_for('index'))

# begin administration views

class DatabaseAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated()

class UserAdmin(ModelView):
    column_exclude_list = ['about_me']
    column_sortable_list = ('username', 'email', 'role', 'created_at', 'first_name', 'last_name', 'last_modified', 'active')
    column_searchable_list = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, session):
        super(UserAdmin, self).__init__(User, session)

class PostAdmin(ModelView):
    column_sortable_list = ('title', ('author', User.username), 'created_on')

    def __init__(self, session):
        super(PostAdmin, self).__init__(Post, session)

class CategoryAdmin(ModelView):

    def __init__(self, session):
        super(CategoryAdmin, self).__init__(Category, session)

admin.add_view(UserAdmin(db.session))
admin.add_view(PostAdmin(db.session))
admin.add_view(CategoryAdmin(db.session))

# begin error handling views

@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning("404 Error: %s", request.path)
    return render_template("404.html"), 404
