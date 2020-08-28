"""Flask config class."""
import pathlib


class Config(object):
    """Set Flask base configuration"""
    SECRET_KEY = 'dfdQbTOExternjy5xmCNaA'  # Replace with your own secret key! This should not be visible to others.
    DATA_PATH = pathlib.Path(__file__).parent.parent.joinpath("data")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(DATA_PATH.joinpath('example.sqlite'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST = pathlib.Path(__file__).parent.joinpath("static").joinpath("photos")


class ProdConfig(Config):
    ENV = 'production' # Warning: this is not the recommended method but should suffice for our app
    DEBUG = False
    TESTING = False


class TestConfig(Config):
    ENV = 'testing'
    DEBUG = False
    TESTING = True
    #  To allow forms to be submitted from the tests without the CSRF token
    WTF_CSRF_CHECK_DEFAULT = False
    WTF_CSRF_ENABLED = False


class DevConfig(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
