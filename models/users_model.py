""" This file holds the model for a user and group

    We use an adaption of: https://flask-authorize.readthedocs.io/en/latest/
"""
from flask_authorize import RestrictionsMixin
from database import db


# Define the 'groups' table
# pylint: disable=too-few-public-methods
class Group(db.Model, RestrictionsMixin):
    """ Group model """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    restrictions = db.Column(db.String(255), default='')

    # Define the relationship with users
    users = db.relationship('User', secondary='user_group', back_populates='groups')

# Define the 'users' table
# pylint: disable=too-few-public-methods
class User(db.Model):
    """ User model """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    # Add user to a group
    groups = db.relationship('Group', secondary='user_group')


# Create relations between tables
user_group = db.Table(
    'user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)
