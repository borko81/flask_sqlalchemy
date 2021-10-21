import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'


class TestingConfig(Config):
    TESTING = True
