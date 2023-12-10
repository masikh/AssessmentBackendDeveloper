""" API for user creation and authentication """

from http import HTTPStatus
from flask import redirect, url_for, request, make_response, jsonify
from flask_bcrypt import Bcrypt
from models.users_model import User
from database import db
from routes import auth


def response_bad_request(error='Bad request'):
    """ Generic 400 response """

    # Build a 400 response
    response = make_response(jsonify({'error': error}))
    response.status_code = HTTPStatus.BAD_REQUEST
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
        response_bad_request('email, name and password cannot be null')

    # Check if a user with this email is know, return a comprehensive message to the end-user
    user = User.query.filter_by(email=email).first()
    if user:
        response_bad_request('email already taken')

    # Encrypt the password using bcrypt, no clear text password in the database
    bcrypt = Bcrypt()
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # create a new user with the hashed password
    new_user = User(email=email, name=name, password=password_hash)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))
