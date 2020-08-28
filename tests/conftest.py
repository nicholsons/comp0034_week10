"""Fixtures for the tests"""

import pytest

from my_app import create_app, config, add_countries
from my_app import db as _db


@pytest.yield_fixture(scope='session')
def app(request):
    """ Returns a session wide Flask app """
    _app = create_app(config.TestConfig)
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='session')
def client(app):
    """ Exposes the Werkzeug test client for use in the tests. """
    return app.test_client()


@pytest.yield_fixture(scope='session')
def db(app):
    """
    Returns a session wide database using a Flask-SQLAlchemy database connection.
    Country list is added to the database.
    All tables are dropped at the end of the test.
    """
    _db.app = app
    _db.create_all()
    add_countries(app)

    yield _db

    _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db):
    """ Rolls back database changes at the end of each test """
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session_ = db.create_scoped_session(options=options)

    db.session = session_

    yield session_

    transaction.rollback()
    connection.close()
    session_.remove()


@pytest.fixture(scope='function')
def user(db):
    """ Creates a user without a profile. """
    from my_app.models import User
    user = User(firsname="Person", lastname='One', email='person1@people.com')
    user.set_password('password1')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def user_with_profile(db):
    """ Creates a user with a profile with a username and bio """
    from my_app.models import User, Profile
    user = User(firsname='Person', lastname='Two', email='person2@people.com')
    user.profile = Profile(username='person2',
                           bio="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam ac tempor metus. "
                               "Aenean mattis, tortor fringilla iaculis pharetra, dui justo imperdiet turpis, "
                               "at faucibus risus eros vitae dui. Nam finibus, nibh eu imperdiet feugiat, nisl lacus "
                               "porta tellus, a tincidunt nibh enim in urna. Aliquam commodo volutpat ligula at "
                               "tempor. In risus mauris, commodo id mi non, feugiat convallis ex. Nam non odio dolor. "
                               "Cras egestas mollis feugiat. Morbi ornare laoreet varius. Pellentesque fringilla "
                               "convallis risus, sit amet laoreet metus interdum et.")
    user.set_password('password2')
    db.session.add(user)
    db.session.commit()
    return user


# Helper functions (not fixtures) from https://flask.palletsprojects.com/en/1.1.x/testing/
def login(client, email, password):
    return client.post('/login/', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout/', follow_redirects=True)