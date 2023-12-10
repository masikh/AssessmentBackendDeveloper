""" This file holds the model for a user """
from database import db  # Import the db instance from the main application file


# pylint: disable=too-few-public-methods
class User(db.Model):
    """ User model """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  # primary key for user
    email = db.Column(db.String(100), unique=True)  # unique email for a user
    password = db.Column(db.String(100))  # password for the user (100 char max)
    name = db.Column(db.String(1000))  # name for the user (1000 char max)
