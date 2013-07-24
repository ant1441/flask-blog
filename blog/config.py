import os
from os.path import abspath, dirname, join

basedir = abspath(dirname(__file__))
databasedir = join(basedir, 'database')


class Config(object):
    SECRET_KEY = \
        r'\x7f\xd0\xedMT\xed\\\x92[\xdb~v\xb4\xdc\xd0\\3f\x11\xd7\x19\xcelh'


class Production(Config):
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_FILE",
        'sqlite:///' + join(databasedir,
                            'blog.db'))
    SQLALCHEMY_MIGRATE_REPO = join(basedir, 'db_repository')


class Development(Config):
    CSRF_ENABLED = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_FILE",
        'sqlite:///' + join(databasedir,
                            'development.db'))
    SQLALCHEMY_MIGRATE_REPO = join(basedir, 'db_repository')


class Testing(Config):
    CSRF_ENABLED = False
    TESTING = True
