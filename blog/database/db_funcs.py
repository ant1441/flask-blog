from blog import db
from blog.models import User, Post, Category


def init_db():
    db.create_all()


def test_data():
    admin = User("Admin", "admin@example.com", "pass")
    me = User("Adam", "adam@example.com", "password")
    guest = User("Guest", "guest@example.com", "guestpass")
    db.session.add(admin)
    db.session.add(me)
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

if __name__ == "__main__":
    init_db()
    test_data()
