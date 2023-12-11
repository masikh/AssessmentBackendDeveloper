""" Unit test for /api/login """
import unittest
from unittest.mock import patch
from flask import Flask, json
from flask_bcrypt import Bcrypt
from routes import auth
from models.users_model import User
from database import db


class AuthTestCase(unittest.TestCase):
    """ Tests for /api/login """
    def setUp(self):
        """ Setup the test environment """

        # Create a test Flask application
        self.app = Flask(__name__)
        self.app.register_blueprint(auth)

        # Use an in-memory SQLite database for testing
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Set Secret key (needed for creating hashes)
        self.app.config['SECRET_KEY'] = 'unittest'

        # Set up the Flask test client
        self.client = self.app.test_client()

        # Initialize the test database and create a test user
        db.init_app(self.app)
        with self.app.app_context():
            # Create table(s)
            db.create_all()

            # Encrypt a password using bcrypt
            bcrypt = Bcrypt()
            password_hash = bcrypt.generate_password_hash('test_password').decode('utf-8')

            # Create the user object with the hashed password
            self.test_user = User(email='test@example.com', password=password_hash)

            # Commit the user to the database
            db.session.add(self.test_user)
            db.session.commit()

    def tearDown(self):
        """ Clean up any test data or resources """

        # Clean up the test database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('generic_helpers.authenticator.Authenticator.generate_token')
    def test_login_successful(self, mock_generate_token):
        """ Test if a token is generated on correct input """

        # Mock the generate_token method
        mock_generate_token.return_value = 'test_token'

        # Send a POST request with valid credentials
        response = self.client.post(
            '/api/user/login',
            json={'email': 'test@example.com', 'password': 'test_password'}
        )

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'token': 'test_token'})

    def test_login_missing_credentials(self):
        """ Test is a 400 is returned if credentials are missing """

        # Send a POST request with missing credentials
        response = self.client.post('/api/user/login', json={})

        # Assert the response status code and content
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {'error': 'email and password cannot be null'})

    def test_login_user_not_found(self):
        """ Test if access is denied with incorrect credentials (non-existing user in this case) """

        # Send a POST request with a non-existing user's credentials
        response = self.client.post(
            '/api/user/login',
            json={'email': 'nonexistent@example.com', 'password': 'test_password'}
        )

        # Assert the response status code and content
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.data), {'error': 'Forbidden'})

    def test_login_invalid_password(self):
        """ Test if access is denied with incorrect credentials (invalid password in this case) """

        # Mock the Authenticator to simulate invalid password
        with patch('generic_helpers.authenticator.Authenticator') as mock_authenticator:
            mock_authenticator.return_value.generate_token.side_effect = ValueError('Invalid password')

            # Send a POST request with valid credentials but invalid password
            response = self.client.post(
                '/api/user/login',
                json={'email': 'test@example.com', 'password': 'invalid_password'}
            )

            # Assert the response status code and content
            self.assertEqual(response.status_code, 403)
            self.assertEqual(json.loads(response.data), {'error': 'Invalid password'})


if __name__ == '__main__':
    unittest.main()
