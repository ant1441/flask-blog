from datetime import datetime
from blog import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    slug = db.Column(db.String(64), index=True, unique=True)
    content = db.Column(db.Text, index=True)
    code = db.Column(db.Boolean)
    hidden = db.Column(db.Boolean)
    updated_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)

    # relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    category = db.relationship('Category', backref='posts', lazy='dynamic')

    def __init__(self,
                 title,
                 content,
                 user,
                 category_id=None,
                 code=False,
                 hidden=False):
        self.title = title
        self.content = content
        self.category_id = category_id
        self.user_id = user.id
        self.created_at = datetime.utcnow()
        self.code = code
        self.hidden = hidden

    def date(self, format_="%d %b %y"):
        return datetime.strftime(self.created_at, format_)

    def __repr__(self):
        format_ = "<Post {0}: '{1}'>"
        if self.id is not None:
            return format_.format(self.id, self.title)
        return format_.format("'No id set'", self.title)
