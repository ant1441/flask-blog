from datetime import datetime
from blog import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    created_at = db.Column(db.DateTime)
    hidden = db.Column(db.Boolean)

    # relationships
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, name, hidden=False):
        self.name = name
        self.created_at = datetime.utcnow()
        self.hidden = hidden

    def __repr__(self):
        format_ = "<Category {0}: '{1}'>"
        if self.id is not None:
            return format_.format(self.id, self.name)
        return format_.format("'No id set'", self.name)
