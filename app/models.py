from hashlib import md5
from datetime import datetime
from flask.ext.login import make_secure_token
from werkzeug.security import generate_password_hash
from app import db

ROLE_USER = 1
ROLE_ADMIN = 0

SALT_LENGTH = 16


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.LargeBinary(144))
    email = db.Column(db.String(128), index=True, unique=True)
    role = db.Column(db.Integer, default=ROLE_USER)
    first_name = db.Column(db.String(128), index=True)
    last_name = db.Column(db.String(128), index=True)
    about_me = db.Column(db.Text, index=True)
    created_at = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)
    active = db.Column(db.Boolean)

    # relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(
            password,
            salt_length=SALT_LENGTH)
        del password
        if self.created_at is None:
            self.created_at = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
        return self.active

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
            self.id,
            self.username,
            self.password,
            self.role)
        return secure_token

    def __repr__(self):
        return "<User %d: '%s'>" % (self.id, self.username)

    def __unicode__(self):
        return self.username


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
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.code = code
        self.hidden = hidden

    def date(self, format_="%d %b %y", english=False):
        return datetime.strftime(self.created_at, format_)

    def __repr__(self):
        return "<Post %d: '%s'>" % (self.id, self.title)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    created_at = db.Column(db.DateTime)
    hidden = db.Column(db.Boolean)

    # relationshipts
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, name, hidden=False):
        self.name = name
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.hidden = hidden

    def __repr__(self):
        return "<Category %d: '%s'>" % (self.id, self.name)
