from werkzeug.security import check_password_hash
from flask import render_template, flash, request, redirect, url_for
from flask.ext.login import (
    login_user, logout_user)
from blog import app, lm
from blog.forms import LoginForm
from blog.models import User
from blog.views import log


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
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user.data).first()
        if user:
            if try_login(user, str(form.password.data)):
                flash('Logged in successfully!', 'success')
                log.info("User %s logged in", user)
                login_user(user, remember=form.remember_me.data)
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash('Log in Error', 'danger')
                log.warn("Log in attempt to '%s' from IP %s",
                         user,
                         request.remote_addr)
                form.errors['password'] = [u"Incorrect Password"]
        else:
            log.warn("Log in attempt to '%s' from IP %s",
                     form.user.data,
                     request.remote_addr)
            flash('User not found!', 'danger')
            form.errors['user'] = [u"User not found"]
    return render_template('login.html',
                           title="Log In",
                           form=form)


@app.route('/logout/')
def logout():
    logout_user()
    #flash("Successfully logged out!")
    return redirect(url_for('index'))
