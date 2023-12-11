""" Unit test for /api/user/create """
import unittest
from flask import Flask, json
from flask_bcrypt import Bcrypt
from routes import auth
from models.users_model import User, Group
from database import db


class AuthTestCase(unittest.TestCase):
    """ Tests for /api/user/create """
    def setUp(self):
        """ Setup the test environment """

        # Create a test Flask application
        self.app = Flask(__name__)
        self.app.register_blueprint(auth)

        # Set Secret key (needed for creating hashes)
        self.app.config['SECRET_KEY'] = 'unittest'

        # Use an in-memory SQLite database for testing
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Set up the Flask test client
        self.client = self.app.test_client()

        # Initialize the test database
        db.init_app(self.app)
        with self.app.app_context():
            # Create table(s)
            db.create_all()

            # Create the group 'users'
            group = Group(name='users')
            db.session.add(group)
            db.session.commit()

        # Encrypt a password using bcrypt
        bcrypt = Bcrypt()
        self.password_hash = bcrypt.generate_password_hash('test_password').decode('utf-8')

    def tearDown(self):
        """ Clean up any test data or resources """

        # Clean up the test database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user_successful(self):
        """ Test if a user can be successfully created and is added to the group 'users' """

        # Make sure the test runs within the app context
        with self.app.app_context():
            # Send a POST request with valid user data
            response = self.client.post(
                '/api/user/create',
                json={'email': 'test@example.com', 'name': 'Test User', 'password': 'test_password'}
            )

            # Assert the response status code and content
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data), {'email': 'test@example.com', 'name': 'Test User'})

            # Retrieve the new user and the group 'users' from the database
            user = User.query.filter_by(email='test@example.com').first()
            group = Group.query.filter_by(name='users').first()

            # Assert that the new user and group are added to the database
            self.assertIsNotNone(user)
            self.assertIsNotNone(group)
            self.assertIn(user, group.users)

    def test_create_user_existing_email(self):
        """ Test is creation of a user fails if the email address is already in the database """

        # Create a test user in the database
        with self.app.app_context():
            test_user = User(email='test@example.com', name='Test User', password=self.password_hash)
            db.session.add(test_user)
            db.session.commit()

        # Send a POST request with the existing email
        response = self.client.post(
            '/api/user/create',
            json={'email': 'test@example.com', 'name': 'Test User', 'password': 'test_password'}
        )

        # Assert the response status code and content
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {'error': 'email already taken'})

    def test_create_user_missing_data(self):
        """ Test if any data for a new user is missing fails the creation of a new user """

        # Send a POST request with missing user data
        response = self.client.post('/api/user/create', json={})

        # Assert the response status code and content
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {'error': 'email, name and password cannot be null'})


if __name__ == '__main__':
    unittest.main()
