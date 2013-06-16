import os
import unittest
from datetime import datetime

from config import basedir
from app import app, db
from app.models import User


class TestUserModel(unittest.TestCase):
    def sedtUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + os.path.join(basedir, 'database\test.db')
        self.app = app.test_client()
        db.create_all()

    def teadrDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User("Test", "test@example.com", "password")
        avatar = u.avatar(1)
        expected = \
            "http://www.gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
        assert avatar[0:len(expected)] == expected

    def test_avatar_size(self):
        u = User("Test", "test@example.com", "password")
        avatar = u.avatar(5)
        expected = \
            "55502f40dc8b7c769880b10874abc9d0?d=mm&s=5"
        assert avatar[-len(expected):] == expected

    def test_created_at(self):
        u = User("Test", "test@example.com", "password")
        expected = datetime.utcnow()
        time = u.created_at
        assert (time - expected).total_seconds() < 1

    def test_no_posts(self):
        u = User("Test", "test@example.com", "password")
        expected = 0
        number_posts = u.posts.count()
        assert number_posts == expected

    def test_password(self):
        u = User("Test", "test@example.com", "password")
        expected = \
            "sha1"
        algorithm = u.password[:4]
        assert algorithm == expected
