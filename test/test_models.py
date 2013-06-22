from os.path import join
import unittest
from nose.tools import raises
from datetime import datetime
import tempfile
import re

import blog
from blog import app, db
from blog.models import User
from blog.database import db_funcs
from config import basedir


class TestUserModelNoDb(unittest.TestCase):
    def setUp(self):
        self.u = User("Test", "test@example.com", "password")

    def test_avatar(self):
        avatar = self.u.avatar(1)
        expected = \
            "http://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
        assert avatar.startswith(expected)

    def test_avatar_size(self):
        avatar = self.u.avatar(5)
        expected = \
            "55502f40dc8b7c769880b10874abc9d0?d=mm&s=5"
        assert avatar.endswith(expected)

    def test_avatar_largersize(self):
        avatar = self.u.avatar(10)
        expected = \
            "55502f40dc8b7c769880b10874abc9d0?d=mm&s=10"
        assert avatar.endswith(expected)

    def test_created_at(self):
        expected = datetime.utcnow()
        time = self.u.created_at
        assert (time - expected).total_seconds() < 1

    def test_no_posts(self):
        expected = 0
        number_posts = self.u.posts.count()
        assert number_posts == expected

    def test_password_algorithm(self):
        expected = "sha1"
        algorithm = self.u.password[:4]
        assert algorithm == expected

    def test_password_length(self):
        expected = 62
        length = len(self.u.password)
        assert length == expected

    def test_active(self):
        expected = True
        active = self.u.is_active()
        assert active == expected

    def test_anonymous(self):
        expected = False
        anonymous = self.u.is_anonymous()
        assert anonymous == expected

    def test_authenticated(self):
        expected = True
        authenticated = self.u.is_authenticated()
        assert authenticated == expected

    def test_repr(self):
        expected = r"<User .*?: '.*'>"
        expected_type = str
        representation = repr(self.u)
        assert re.match(expected, representation)
        assert type(representation) == expected_type

    def test_unicode(self):
        expected = u"Test"
        expected_type = unicode
        unicode_repr = unicode(self.u)
        assert unicode_repr == expected
        assert type(unicode_repr) == expected_type


class TestUserModelDb(unittest.TestCase):
    def setUp(self):
        self.db_fd, blog.app.config['DATABASE'] = tempfile.mkstemp()
        self.u = User("Test", "test@example.com", "password")
        #self.admin = User.query.get(1)
        db.session.add(self.u)

    def test_id_type(self):
        expected = unicode
        uid = self.u.get_id()
        assert type(uid) == expected

    @raises(RuntimeError)
    def test_auth_token(self):
        expected = "something"
        auth_token = self.u.get_auth_token()
        assert auth_token == expected

    #def tedst_repr(self):
        #expected = r"<User /d*?: '.*'>"
        #expected_type = str
        #representation = repr(self.admin)
        #assert False, representation
        #assert re.match(expected, representation)
        #assert type(representation) == expected_type

    def tearDown(self):
        db.session.rollback()


class TestUserModelWithDb(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(
            join(basedir, 'test.db'))
        print app.config['SQLALCHEMY_DATABASE_URI']
        self.app = app.test_client()
        db.create_all()

    def test_voodoo(self):
        assert db is not None

    def tearDown(self):
        db.session.remove()
        db.drop_all()
