from flask.ext.wtf import (
    Form, TextField, TextAreaField, BooleanField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.ext.wtf import Required, length

from blog.forms.utilities import code_types


class PostBlogForm(Form):
    author = TextField('author', validators=[length(max=5)])
    title = TextField('title', validators=[Required(), length(max=128)])
    text = TextAreaField('text', validators=[Required()])
    slug = TextField('slug', validators=[length(max=64)])
    code = BooleanField('code')
    code_type = QuerySelectField(
        "codeType",
        query_factory=code_types,
        allow_blank=True,
        blank_text="False")
