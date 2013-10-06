from os.path import join
from blog import db
from blog.models import User, Post, Category


def init_db():
    db.create_all()


def test_data():
    admin = User("Admin", "admin@example.com", "pass")
    me = User("Adam", "adam@example.com", "password")
    guest = User("Guest", "guest@example.com", "guestpass")
    db.session.add(admin)
    db.session.commit()
    db.session.add(me)
    db.session.commit()
    db.session.add(guest)
    db.session.commit()
    testCat = Category("Test")
    db.session.add(testCat)
    try:
        with open(join(__file__, "lorem.txt")) as file:
            post = Post("Test Post!",
                        file.read(),
                        User.query.first(),
                        Category.query.first())
        db.session.add(post)
    finally:
        db.session.commit()


def create_user():
    username = raw_input("Username: ")
    email = raw_input("Email: ")
    password = raw_input("Password: ")
    user = User(username, email, password)
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    init_db()
    test_data()
