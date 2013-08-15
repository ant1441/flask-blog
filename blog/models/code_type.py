from blog import db


class CodeType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    # relationships
    posts = db.relationship('Post', backref='code_type', lazy='dynamic')

    def __init__(self,
                 name=None):
        self.name = name

    def __repr__(self):
        return "CodeType('{}')".format(self.name)

    def __unicode__(self):
        return unicode(self.name)
