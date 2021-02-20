# Create a REST API in Flask

## Introduction

This is a somewhat simple example as we don't have much data in our application other than users profiles.

This activity will create a REST API based on the profile information (note: you wouldn't want to share people's
profiles in this way, it is the only table we have in our database currently!).

We will create the following routes:

- HTTP GET /api/profiles/{userid} returns the profile for a user
- HTTP GET /api/profiles returns the profiles of all users
- HTTP POST /api/profiles adds a new user profile

In this API we aren't allowing 'update' and 'delete' so I have omitted those methods.

All routes return JSON.

## Modify models.py to serialise the data

Add code to the profiles table that returns the object data in an easily serializable format. Serialization will turn an
entry into a string format that can be passed around via HTTP.

Add a property to the Profile class to serialise the data we want to provide. I have omitted the photo.

```python
class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    photo = db.Column(db.Text)
    bio = db.Column(db.Text)
    area = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.user_id,
            'username': self.username,
            'bio': self.bio,
            'area': self.area
        }
```

## Create an api package with a routes.py

1. Create a new python package for the api in the project structure.
2. Create routes.py
3. Define a blueprint for the api in routes.py
4. Add the blueprint to the create_app function

## Create the first REST route

Let's add the first route for the GET /api/profiles route.

You need to:

- query the database to return all profiles
- return a response with the profiles in JSON format

The Flask app will return json data rather than rendering a view for the api. To do this we will use a Flask function
called make_response:

```
make_response(body, HTTP status, headers)
```

The data for ‘body’ can be of type str, bytes, dict, or tuple. The body is the serialised results of the query.

The HTTP status code is 200 OK.

The header is 'Content-Type: application/json'.

Flask provides a decorator that can be used after every request. Since we need to add the header type to all our routes
then we could create a method to set the header for every request like this:

```python
@api_bp.after_request
def add_header(response):
    response.headers['Content-Type'] = 'application/json'
    return response
```

However, since Flask.jsonify returns an object and sets the content type to application/json then this after_request is
unnecessary. It is included only to show you that it exists as you may wish to use it if you areen't using
Flask.jsonify.

```python
from flask import Blueprint, jsonify, make_response

from my_app.models import Profile

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/profiles', methods=['GET'])
def get_profiles():
    profiles = Profile.query.all()
    json = jsonify(profiles=[p.serialize for p in profiles])
    return make_response(json, 200)
```

## Download and install postman (or use online)

As the API does not render a view then to see whether our API is returning data we can test it using Postman.

[Download postman](https://www.postman.com/downloads/)

[Create an account and use postman online API](https://www.postman.com/product/api-client/)

Use postman to test the route: GET  http://127.0.0.1:5000/api/profiles

You should get 2 profiles returned as JSON.

## Create the other routes

HTTP GET /api/profiles/{userid} returns the profile for a user

HTTP POST /api/profiles adds a new user profile

```python
@api_bp.route('/profiles/<int:userid>', methods=['GET'])
def get_profile(userid):
    profile = Profile.query.filter_by(id=userid).first_or_404()
    json = jsonify(profile=profile.serialize)
    return make_response(json, 200)


def post_profile():
    """
    Creates a new profile.
    User must be an existing user.
    Username is required and must be unique.
    Area must be in the given list in the area table.
    TODO: Apply validation to the fields
    """
    user_id = request.args.get('userid', type=int)
    bio = request.args.get('bio', type=str)
    area = request.args.get('area', type=str)
    username = request.args.get('username', type=str)
    if username is None:
        headers = {"Content-Type": "application/json"}
        json = jsonify({'message': 'Please provide a username'})
        return make_response(json, 400, headers)
    profile = Profile(user_id=user_id, username=username, bio=bio, area=area)
    db.session.add(profile)
    db.session.commit()
    uri = f'http://127.0.0.1:5000/api/{user_id}'
    json = jsonify({'message': uri})
    headers = {"Content-Type": "application/json"}
    return make_response(json, 201, headers)
```

Use postman to test the routes.

Don't forget to change the request type to POST for the second route and pass values for the required parameters (
userid, username) and optionally for bio and area. Userids 3 and 4 do not have a profile so create a profile for one of these.

## Add custom error handlers

The errors should return json also so let's add some custom error handlers to the api blueprint in routes.py:

```python
@api_bp.errorhandler(404)
def not_found():
    error = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    response = jsonify(error)
    return make_response(response, 404)


@api_bp.errorhandler(401)
def not_authorised():
    error = {
        'status': 401,
        'message': 'You must provide username and password to access this resource',
    }
    response = jsonify(error)
    return make_response(response, 401)
```

## Add basic HTTP authorisation

There are numerous packages that provide methods for handling authorisation.

For this exercise we will use [Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/).

We will first create an auth object:

```python
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
```

We then need to provide an implementation for verify_password:

```python
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(email=username).first()
    if not user or not user.check_password(password):
        return False
    return user
```

We can then prevent api routes from being accessed without authorisation using the `@auth.login_required` decorator.

```python
@app.route('/profiles')
@auth.login_required
def get_profiles():
# etc
```

Finally we will provide a route to allow a user to register an account. This will be added to our existing User table
for speed.

```python
@api_bp.route('/users', methods=['POST', 'GET'])
def create_user():
    """
    Creates a new user.
    User table requires email address, password, firstname and lastname.
    Since we only need two fields for the api users I am adding dummy data to the other fields.
    TODO: Check that the username is a valid email address.
    """
    username = request.args.get('username')
    password = request.args.get('password')
    firstname = "None"
    lastname = "None"
    if username is None or password is None:
        json = jsonify({'message': 'Missing username or password'})
        return make_response(json, 400)
    if User.query.filter_by(email=username).first() is not None:
        json = jsonify({'message': 'Duplicate username'})
        return make_response(json, 400)
    user = User(email=username, firstname=firstname, lastname=lastname)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    json = jsonify({'userid': '{}'.format(user.id), 'username': '{}'.format(user.email)})
    return make_response(json, 201)
```

To check whether this is working use Postman and:

1. POST http://127.0.0.1:5000/users  with parameters username (fluffy@cloud.com) and password (sky)
2. GET http://127.0.0.1:5000/profiles  without username and password and you should get a 401 error
3. GET  http://127.0.0.1:5000/profiles  go to the Authorisation tab and enter the username and password used in step 1.
