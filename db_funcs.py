from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config
from app import db

def init_db():
    db.create_all()

def test_data():
    from app import models
    admin = models.User("Admin", "admin@example.com", "pass")
    me = models.User("Adam", "adam@example.com", "futurama")
    guest = models.User("Guest", "guest@example.com", "guestpass")
    db.session.add(admin)
    db.session.add(me)
    db.session.add(guest)
    db.session.commit()
    testCat = models.Category("Test")
    db.session.add(testCat)
    db.session.commit()
    post = models.Post("Test Post!", "This is a test post.", models.User.query.first(), models.Category.query.first())
    db.session.add(post)
    db.session.commit()
