import os
import unittest

from config import basedir
from blog import app, db


class TestSimpleViews(unittest.TestCase):
    def sedtUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def teadrDown(self):
        db.session.remove()
        db.drop_all()

    def test_index(self):
        pass
