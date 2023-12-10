""" __init__ file"""
from flask import Flask, g, request
from flask_authorize import Authorize
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from models.users_model import User
from generic_helpers.memoize import Memoize


# Create the Flask app
app = Flask('__name__')


def my_current_user():
    """ Return current user to check authorization against """

    # Extract the token from the 'Authorization' header
    token  = request.headers.get('Authorization')

    # Bailout if there is no Authorization header
    if token is None:
        return None

    # Verify and extract user from the token
    user = extract_user_from_token(token)
    return user

def extract_user_from_token(token):
    """
    Extract user from the token.
    """
    serializer = Serializer(app.config['SECRET_KEY'])
    try:
        data = serializer.loads(token)
        user_id = data.get('id')
        # Assuming you have a User model with an 'id' field
        user = User.query.get(user_id)
        return user
    except (SignatureExpired, BadSignature):
        return None

# Initialize authorize decorator, using the declarative method for setting up the extension
authorize = Authorize(current_user=my_current_user)
authorize.init_app(app)

# Initialize memoization
memoize = Memoize(ttl=300, max_items=300)
