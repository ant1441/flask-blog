from datetime import datetime
from hashlib import md5
from flask.ext.login import make_secure_token
from werkzeug.security import generate_password_hash
from blog import db

ROLE_USER = 1
ROLE_ADMIN = 0
SALT_LENGTH = 16


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(74))
    email = db.Column(db.String(128), index=True)
    role = db.Column(db.Integer, default=ROLE_USER)
    first_name = db.Column(db.String(128), index=True)
    last_name = db.Column(db.String(128), index=True)
    about_me = db.Column(db.Text, index=True)
    created_at = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    #active = db.Column(db.Boolean)

    # relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = generate_password_hash(
            password,
            salt_length=SALT_LENGTH)
        del password
        self.active = True
        self.created_at = datetime.utcnow()
        self.last_modified = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
        #return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        hexDigest = md5(self.email).hexdigest()
        size = str(size)

        return 'http://www.gravatar.com/avatar/{0}?d=mm&s={1}'.format(
            hexDigest, size)

    def get_auth_token(self):
        secure_token = make_secure_token(
            str(self.id),
            self.username,
            self.password,
            str(self.role))
        return secure_token

    def __repr__(self):
        format_ = "<User {0}: '{1}'>"
        if self.id is not None:
            return format_.format(self.id, self.username)
        return format_.format("'No id set'", self.username)

    def __unicode__(self):
        return self.username
