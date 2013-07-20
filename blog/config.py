from os.path import abspath, dirname, join

basedir = abspath(dirname(__file__))
databasedir = join(basedir, 'database')


class Config(object):
    SECRET_KEY = \
        r'\x91a\xd3gE\xa6}\xb8O\x9fn@\x83+\xed\xa3Y+\x7f\x1b\x0b\xba\x84\xf5'


class Production(Config):
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(
        databasedir,
        'blog.db')
    SQLALCHEMY_MIGRATE_REPO = join(basedir, 'db_repository')


class Development(Config):
    CSRF_ENABLED = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(
        databasedir,
        'development.db')
    SQLALCHEMY_MIGRATE_REPO = join(basedir, 'db_repository')


class Testing(Config):
    CSRF_ENABLED = False
    TESTING = True
