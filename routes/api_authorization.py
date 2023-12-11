""" API for user creation and authentication """

from http import HTTPStatus
from flask import request, make_response, jsonify
from flask_bcrypt import Bcrypt
from models.users_model import User, Group
from database import db
from routes import auth
from generic_helpers.authenticator import Authenticator


def response_bad_request(error='Bad request'):
    """ Generic 400 response """

    # Build a 400 response
    response = make_response(jsonify({'error': error}))
    response.status_code = HTTPStatus.BAD_REQUEST
    return response


def response_forbidden(error='Forbidden'):
    """ Generic 403 response """

    # Build a 403 response
    response = make_response(jsonify({'error': error}))
    response.status_code = HTTPStatus.FORBIDDEN
    return response


@auth.route('/api/user/create', methods=['POST'])
def api_user_create():
    """ Create a new user """

    # Get post data from request
    data = request.get_json()

    # Unpack post data
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    # guard clause
    if None in [email, name, password]:
        return response_bad_request('email, name and password cannot be null')

    # Check if a user with this email is know, return a comprehensive message to the end-user
    user = User.query.filter_by(email=email).first()
    if user:
        return response_bad_request('email already taken')

    # Encrypt the password using bcrypt, no clear text password in the database
    bcrypt = Bcrypt()
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # create a new user with the hashed password
    new_user = User(email=email, name=name, password=password_hash)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # add the new user to the group 'users'. First get the group 'users'
    users_group = Group.query.filter_by(name='users').first()

    # Check for the existence of the group
    if not users_group:
        raise RuntimeError('Group users should always exist')

    # Add the new user to the 'users' group
    users_group.users.append(new_user)
    db.session.commit()

    # Build a 200 response
    response = make_response(jsonify({'email': email, 'name': name}))
    response.status_code = HTTPStatus.OK
    return response


@auth.route('/api/user/login', methods=['POST'])
def api_user_login():
    """ User login route, returns a token """

    # Get post data from request
    data = request.get_json()

    # Unpack post data
    email = data.get('email')
    password = data.get('password')

    # guard clauses

    # Check if email and password are provided
    if None in [email, password]:
        return response_bad_request('email and password cannot be null')

    # Check if the user exist
    user = User.query.filter_by(email=email).first()
    if user is None:
        return response_forbidden()

    # Check password for the user and create a token or return a forbidden
    authenticator = Authenticator(user_obj=user, password=password)
    try:
        # A value error is raised if the password doesn't match
        token = authenticator.generate_token()
    except ValueError as error:
        # Invalid password
        return response_forbidden(str(error))

    # Build a 200 response
    response = make_response(jsonify({'token': token}))
    response.status_code = HTTPStatus.OK
    return response
