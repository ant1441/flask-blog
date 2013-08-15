from flask.ext.wtf import (
    Form, TextField, TextAreaField, SelectField, BooleanField)
from flask.ext.wtf import Required, length


class PostBlogForm(Form):
    author = TextField('author', validators=[length(max=5)])
    title = TextField('title', validators=[Required(), length(max=128)])
    text = TextAreaField('text', validators=[Required()])
    slug = TextField('slug', validators=[length(max=64)])
    code = BooleanField('code')
    codeType = SelectField(
        "codeType",
        choices=[
            ('none', 'None'),
            ('html', 'HTML'),
            ('python', 'Python')
        ])
