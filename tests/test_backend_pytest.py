from my_app.models import User


def test_index_page_valid(client):
    """
    GIVEN a Flask application is running
    WHEN the '/' home page is requested (GET)
    THEN check the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200


def test_profile_not_allowed_when_user_not_logged_in(client):
    """
    GIVEN A user is not logged
    WHEN When they access the profile menu option
    THEN they should be redirected to the login page
    """
    response = client.get('/community/profile', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
    # assert response.location == '/login' # should work if redirect as redirect header contains location


def test_signup_succeeds(client):
    """
        GIVEN A user is not registered
        WHEN When they submit a valid registration form
        THEN they the should be redirected to a page with a custom welcome message and there should be an additional
        record in the user table in the database
        """
    count = User.query.count()
    response = client.post('/signup', data=dict(
        first_name='First',
        last_name='Last',
        email='email@address.com',
        password='password',
        password_repeat='password'
    ), follow_redirects=True)
    count2 = User.query.count()
    assert count2 - count == 1
    assert response.status_code == 200
    assert b'First' in response.data


def test_create_profile_not_allowed_when_user_not_logged_in(client):
    """
    GIVEN a Flask application
    WHEN the ‘/community/profile' page is requested (GET) when the user is not logged in
    THEN the user is redirected to the login page and the message ‘You must be logged in to view that page.’ is
    displayed
    """
    response = client.get('/community/profile', follow_redirects=True)
    assert b'You must be logged in to view that page' in response.data
    assert b'<title>Login</title>' in response.data


# Try and write tests for the following:

"""
GIVEN a User has been created
WHEN the user logs in with the wrong email address
THEN then an error message should be displayed on the login form ('No account found with that email address.')
"""

'''
GIVEN a User has been created
WHEN the user logs in with the wrong password
THEN then an error message should be displayed on the login form ('Incorrect password.')
'''

'''
GIVEN a User is logged in and selected Remember Me
WHEN they close the browser and re-open it within 60 seconds
THEN they should remain logged in
'''

'''
GIVEN a User is logged in and selected Remember Me
WHEN they close the browser and re-open after 60 seconds
THEN they should be required to login again to access any protected pages (such as community home)
'''

'''
GIVEN a User logged out
WHEN they access the navigation bar
THEN there should be an option to login in
'''
