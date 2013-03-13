from flask.ext.wtf import Form, TextField, TextAreaField, SelectField, BooleanField, PasswordField
from flask.ext.wtf import Required, length
from models import User

class postBlogForm(Form):
    author = TextField('author', validators = [length(max=5)])
    title = TextField('title', validators = [Required(), length(max=128)])
    text = TextAreaField('text', validators = [Required()])
    slug = TextField('slug', validators = [length(max=64)])
    code = BooleanField('code')
    codeType = SelectField("codeType", choices=[('none', 'None'), ('html', 'HTML'), ('python','Python')])

class loginForm(Form):
    user = TextField('user', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
