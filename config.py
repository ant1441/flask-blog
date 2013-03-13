import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = r'\x91a\xd3gE\xa6}\xb8O\x9fn@\x83+\xed\xa3Y+\x7f\x1b\x0b\xba\x84\xf5'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database', 'blog.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
