""" Authentication class """
from functools import wraps
from http import HTTPStatus

# from itsdangerous import (
#    TimedJSONWebSignatureSerializer as Serializer,
#    BadSignature,
#    SignatureExpired,
# )
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from itsdangerous.exc import BadTimeSignature, BadSignature, BadPayload
from flask import current_app, request, make_response, jsonify
from flask_bcrypt import Bcrypt
from models.users_model import User


class Authenticator:
    """Generate and verify session token

    This class hold methods for generating a token (after password validation)
    and verification of a token (valid, expired, signature)
    """

    def __init__(self, user_obj=None, password=None):
        self.user_obj = user_obj
        self.password = password

    def is_valid_password(self):
        """Password-validator"""

        # Check if the password provided matches with our password
        bcrypt = Bcrypt()
        valid = bcrypt.check_password_hash(self.user_obj.password, self.password)
        return valid

    def generate_token(self):
        """Generate authentication token valid for 20 minutes"""

        # Check if the password is valid
        if not self.is_valid_password():
            raise ValueError("Invalid password")

        # Create new token and get the dump the json object into token
        serializer = Serializer(current_app.config["SECRET_KEY"])
        token = serializer.dumps({"id": self.user_obj.id})

        # return the token
        return token

    @staticmethod
    def verify_token(token):
        """Verify token"""

        # Create an instance of Serializer for token validation
        serializer = Serializer(current_app.config["SECRET_KEY"])
        try:
            serializer.loads(token)
        except (BadTimeSignature, BadSignature, BadPayload):
            return (
                False  # valid token (but expired), invalid token or generic exception
            )
        return True

    @staticmethod
    def get_user_from_token(token):
        """Extract user ID from token"""

        # Setup serializer
        serializer = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token)
            user_id = data.get("id")
            if user_id is None:
                return None
            user = User.query.get(user_id)
            return user
        except (BadTimeSignature, BadSignature, BadPayload):
            return None  # Invalid token or token expired


def authenticated(func):
    """Simple decorator for checking if a valid Authorization header is set"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the token from the request heade
        token = request.headers.get("Authorization")

        # Check if authorization header is set
        if not token:
            # Build a 400 response
            response = make_response(jsonify({"error": "Authorization header missing"}))
            response.status_code = HTTPStatus.BAD_REQUEST
            return response

        # Verify the token using the Authenticator class
        if not Authenticator.verify_token(token):
            # Build a 400 response
            response = make_response(jsonify({"error": "Forbidden"}))
            response.status_code = HTTPStatus.FORBIDDEN
            return response
        # If the token is valid, proceed with the original function

        return func(*args, **kwargs)

    return wrapper
