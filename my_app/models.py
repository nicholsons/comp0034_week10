from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from my_app import db


class User(UserMixin, db.Model):
    # Uncomment the following line and remove all the field definitions if you want to experiment with
    # reflection
    # __table__ = db.Model.metadata.tables['user']
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    profiles = db.relationship('Profile', backref='user', lazy=True)

    def __repr__(self):
        return f"{self.id} {self.firstname} {self.lastname} {self.email} {self.password}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    photo = db.Column(db.Text)
    bio = db.Column(db.Text)
    area = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Area(db.Model):
    __tablename__ = 'area'
    code = db.Column(db.Text, nullable=False, primary_key=True)
    area = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.area
