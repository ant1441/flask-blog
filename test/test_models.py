import unittest
from nose.tools import raises
from datetime import datetime
import tempfile

import blog
from blog import app, db
from blog.models import User, Post, Category


class TestModels(unittest.TestCase):
    def test_constants(self):
        assert blog.models.ROLE_USER == 1
        assert blog.models.ROLE_ADMIN == 0


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
        expected = r"<User 'No id set': 'Test'>"
        expected_type = str
        representation = repr(self.u)
        assert expected == representation
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
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        db.create_all()
        test_user = User("TestUser", "test@example.com", "password")
        db.session.add(test_user)
        test_post = Post("Post Title", "Post Content", test_user)
        db.session.add(test_post)
        db.session.commit()

    def test_user_count(self):
        expected = 1
        assert User.query.count() == expected, "Wrong number of users found"

    def test_user_details_email(self):
        expected = "test@example.com"
        user = User.query.filter_by(email="test@example.com").first()
        assert user.email == expected

    def test_user_details_username(self):
        expected = "TestUser"
        user = User.query.filter_by(email="test@example.com").first()
        assert user.username == expected

    def test_user_repr(self):
        expected = "<User 1: 'TestUser'>"
        user = User.query.one()
        assert repr(user) == expected, "DB User repr invalid"

    def test_user_auth_token(self):
        expected_length = 40
        expected_type = unicode
        user = User.query.one()
        with app.app_context():
            token = user.get_auth_token()
        assert len(token) == expected_length, \
            "Auth token invalid length. Was {0}. Expected {1}".format(
                len(token),
                expected_length)
        assert type(token) == expected_type, \
            "User auth token invalid type. Was {0}. Expected {1}".format(
                type(token),
                expected_type)

    def test_post_count(self):
        expected = 1
        assert Post.query.count() == expected

    def tearDown(self):
        db.session.remove()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()


class TestPostModelNoDb(unittest.TestCase):
    def setUp(self):
        self.u = User("Test User", "test@example.com", "password")
        self.c = Category("Test Category")
        self.p = Post("Test Post Title",
                      "Test Post Content",
                      self.u,
                      self.c,
                      code=True,
                      hidden=True)

    def test_date(self):
        expected_type = str
        expected_before = datetime.now()
        date = self.p.date()
        datetime_date = datetime.strptime(date, "%d %b %y")
        assert type(date) == expected_type, \
            "Date type incorrect. Was {0}. Expected {1}".format(
                type(date),
                expected_type)
        assert datetime_date < expected_before, "Date not before now"

    def test_repr(self):
        expected = "<Post 'No id set': 'Test Post Title'>"
        repr_ = repr(self.p)
        assert repr_ == expected


class TestPostModelWithDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        db.create_all()
        test_user = User("Test User", "test@example.com", "password")
        db.session.add(test_user)
        test_category = Category("Test Category")
        db.session.add(test_category)
        test_post = Post(
            "Post Title",
            "Post Content",
            test_user,
            test_category)
        db.session.add(test_post)
        db.session.commit()

    def test_post_db_repr(self):
        expected = "<Post 1: 'Post Title'>"
        post_repr = repr(Post.query.one())
        assert post_repr == expected

    def tearDown(self):
        db.session.remove()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()


class TestCategoryModelNoDb(unittest.TestCase):
    def setUp(self):
        self.c = Category("Test Category")

    def test_repr(self):
        expected = "<Category 'No id set': 'Test Category'>"
        category_repr = repr(self.c)
        assert category_repr == expected


class TestCategoryModelWithDb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        db.create_all()
        test_category = Category("Test Category")
        db.session.add(test_category)
        db.session.commit()

    def test_category_db_repr(self):
        expected = "<Category 1: 'Test Category'>"
        category_repr = repr(Category.query.one())
        assert category_repr == expected

    def tearDown(self):
        db.session.remove()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
