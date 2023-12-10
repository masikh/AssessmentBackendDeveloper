""" Authentication class """
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import current_app
from flask_bcrypt import Bcrypt


class Authenticator:
    """ Generate and verify session token

        This class hold methods for generating a token (after password validation)
        and verification of a token (valid, expired, signature)
    """
    def __init__(self, user_obj=None, password=None):
        self.user_obj = user_obj
        self.password = password

    def is_valid_password(self):
        """ Password-validator """

        # Check if the password provided matches with our password
        bcrypt = Bcrypt()
        valid = bcrypt.check_password_hash(self.user_obj.password, self.password)
        return valid

    def generate_token(self, expiration=1200):
        """ Generate authentication token valid for 20 minutes """

        # Check if the password is valid
        if not self.is_valid_password():
            raise ValueError('Invalid password')

        # Create new token and get the dump the json object into token
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        token = serializer.dumps({'id': self.user_obj.id})

        # return the token
        return token.decode('utf-8')

    @staticmethod
    def verify_token(token):
        """ Verify token """

        # Create an instance of Serializer for token validation
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:

            serializer.loads(token)
        except (SignatureExpired, BadSignature):
            return False  # valid token (but expired), invalid token or generic exception
        return True
