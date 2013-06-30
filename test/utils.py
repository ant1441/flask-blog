from os.path import join, exists
from blog import app, db
from blog.models import User, Post, Category


def init_db():
    db.create_all()


def test_database():
    database_location = app.config.get("SQLALCHEMY_DATABASE_URI")[10:]
    assert exists(join('..', 'blog', database_location)), \
        "Database doesn't exist"
    db.echo = True
    admin = User("Admin", "admin@example.co.uk", "pass")
    db.session.add(admin)
    db.session.commit()
    me = User("Adam", "adam@example.co.uk", "password")
    db.session.add(me)
    db.session.commit()
    guest = User("Guest", "guest@example.co.uk", "guestpass")
    db.session.add(guest)
    db.session.commit()
    testCat = Category("Test")
    db.session.add(testCat)
    db.session.commit()
    post = Post("Test Post!",
                "This is a test post.",
                User.query.first(),
                Category.query.first())
    db.session.add(post)
    db.session.commit()
