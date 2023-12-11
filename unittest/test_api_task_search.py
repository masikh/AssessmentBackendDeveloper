""" Unit test for /api/task/search """
import unittest
from datetime import datetime
from flask import Flask
from flask_bcrypt import Bcrypt
from routes import api
from models.users_model import User
from models.task_model import Task, TaskStatus
from database import db
from generic_helpers.authenticator import Authenticator


class AuthTestCase(unittest.TestCase):
    """Tests for /api/task/search"""

    def setUp(self):
        """Setup the test environment"""

        # Create a test Flask application
        self.app = Flask(__name__)
        self.app.register_blueprint(api)

        # Use an in-memory SQLite database for testing
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # Set Secret key (needed for creating hashes)
        self.app.config["SECRET_KEY"] = "unittest"

        # Set up the Flask test client
        self.client = self.app.test_client()

        # Initialize the test database and create a test user
        db.init_app(self.app)
        with self.app.app_context():
            # Create table(s)
            db.create_all()

            # Encrypt a password using bcrypt
            bcrypt = Bcrypt()
            password_hash = bcrypt.generate_password_hash("test_password").decode(
                "utf-8"
            )

            # Create the user object with the hashed password
            self.test_user = User(email="test@example.com", password=password_hash)

            # Commit the user to the database
            db.session.add(self.test_user)
            db.session.commit()

            # Create authentication token
            authenticator = Authenticator(
                user_obj=self.test_user, password="test_password"
            )
            self.token = authenticator.generate_token()

            # Create some tasks in the database
            task1 = Task(
                title="Task 1",
                description="Description 1",
                status=TaskStatus.PENDING,
                due_date=datetime.strptime("2023-01-01", "%Y-%m-%d").replace(
                    hour=12, minute=0, second=0, microsecond=0
                ),
            )
            task2 = Task(
                title="Task 2",
                description="Description 2",
                status=TaskStatus.STARTED,
                due_date=datetime.strptime("2023-01-02", "%Y-%m-%d").replace(
                    hour=12, minute=0, second=0, microsecond=0
                ),
            )
            task3 = Task(
                title="Task 3",
                description="Description 3",
                status=TaskStatus.COMPLETED,
                due_date=datetime.strptime("2023-01-03", "%Y-%m-%d").replace(
                    hour=12, minute=0, second=0, microsecond=0
                ),
            )

            db.session.add_all([task1, task2, task3])
            db.session.commit()

    def tearDown(self):
        """Clean up any test data or resources"""

        # Clean up the test database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_search_pending(self):
        """Test if the search result returns the single pending task"""

        # Send a request to search tasks
        response = self.client.get(
            "/api/task/search",
            headers={"Authorization": self.token},
            query_string={"page": 1, "page_size": 3, "status": "pending"},
        )

        # Our expected result in the response data
        expected_result = {
            "current_page": 1,
            "last_page": 1,
            "result": [
                {
                    "description": "Description 1",
                    "due_date": "2023-01-01T12:00:00",
                    "id": 1,
                    "status": "pending",
                    "title": "Task 1",
                }
            ],
        }

        # Assert the response status code and response_data
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, expected_result)

    def test_search_paginated(self):
        """Test if the search result returns the second result page"""

        # Send a request to search tasks
        response = self.client.get(
            "/api/task/search",
            headers={"Authorization": self.token},
            query_string={"page": 2, "page_size": 1},
        )

        # Our expected result in the response data
        expected_result = {
            "current_page": 2,
            "last_page": 3,
            "result": [
                {
                    "description": "Description 2",
                    "due_date": "2023-01-02T12:00:00",
                    "id": 2,
                    "status": "started",
                    "title": "Task 2",
                }
            ],
        }

        # Assert the response status code and response_data
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, expected_result)

    def test_search_partial_text(self):
        """Test searching for partial text matching"""

        # Send a request to search tasks
        response = self.client.get(
            "/api/task/search",
            headers={"Authorization": self.token},
            query_string={"page": 1, "page_size": 3, "title": "k 2"},
        )

        # Our expected result in the response data
        expected_result = {
            "current_page": 1,
            "last_page": 1,
            "result": [
                {
                    "description": "Description 2",
                    "due_date": "2023-01-02T12:00:00",
                    "id": 2,
                    "status": "started",
                    "title": "Task 2",
                }
            ],
        }

        # Assert the response status code and response_data
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, expected_result)

    def test_search_date_range(self):
        """Test searching tasks on date range"""

        # Send a request to search tasks
        response = self.client.get(
            "/api/task/search",
            headers={"Authorization": self.token},
            query_string={
                "page": 1,
                "page_size": 3,
                "after": "2022-12-31",
                "before": "2023-01-03",
            },
        )

        # Our expected result in the response data
        expected_result = {
            "current_page": 1,
            "last_page": 1,
            "result": [
                {
                    "description": "Description 2",
                    "due_date": "2023-01-02T12:00:00",
                    "id": 2,
                    "status": "started",
                    "title": "Task 2",
                },
                {
                    "description": "Description 1",
                    "due_date": "2023-01-01T12:00:00",
                    "id": 1,
                    "status": "pending",
                    "title": "Task 1",
                },
            ],
        }

        # Assert the response status code and response_data
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, expected_result)

    def test_search_reverse_sorting(self):
        """Test searching tasks and sort on ascending date"""

        # Send a request to search tasks
        response = self.client.get(
            "/api/task/search",
            headers={"Authorization": self.token},
            query_string={"page": 1, "page_size": 3, "sort_order": "ascending"},
        )

        # Our expected result in the response data
        expected_result = {
            "current_page": 1,
            "last_page": 1,
            "result": [
                {
                    "description": "Description 1",
                    "due_date": "2023-01-01T12:00:00",
                    "id": 1,
                    "status": "pending",
                    "title": "Task 1",
                },
                {
                    "description": "Description 2",
                    "due_date": "2023-01-02T12:00:00",
                    "id": 2,
                    "status": "started",
                    "title": "Task 2",
                },
                {
                    "description": "Description 3",
                    "due_date": "2023-01-03T12:00:00",
                    "id": 3,
                    "status": "completed",
                    "title": "Task 3",
                },
            ],
        }

        # Assert the response status code and response_data
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json, expected_result)
