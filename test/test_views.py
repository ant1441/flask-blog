import unittest
from blog import app, db


class TestSimpleViews(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()

    def test_index(self):
        index = self.app.get('/')
        print index
        print index.data
        assert False

class TestSimpleViewsWithDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
