from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required
from flask.ext.wtf import Form


class LoginForm(Form):
    user = TextField('user', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)
