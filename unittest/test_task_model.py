import unittest
from datetime import datetime, timedelta

from models.task_model import Task, TaskStatus, enforce_types


#
# Mocked classes
#


@enforce_types
class MockedClass:
    """ Create an arbitrary class with two attributes (annotated!).
        The class is decorated in order to test the decorator itself.
    """
    is_boolean: bool = False
    is_integer: int = 0


#
# Actual tests
#


class TestTask(unittest.TestCase):
    """ Various tests for the Task dataclass """

    def test_task_attributes_defaults(self):
        """ Check that the default values of a task are set """

        # Setup test data
        new_task = Task()

        # Assert test data
        self.assertEqual(new_task.title, 'New task')  # check default value is set
        self.assertEqual(new_task.description, 'Description')  # check default value is set
        self.assertEqual(new_task.status, TaskStatus.PENDING)  # check default value is set

        # Calculate the expected due date (one week from now)
        expected_due_date = datetime.now() + timedelta(weeks=1)

        # Check that the due_date is approximately equal to the expected_due_date.
        # Note: This test might (extremely unlikely) fail if the computer somehow takes
        # more than 10 seconds to complete this test.
        self.assertAlmostEqual(new_task.due_date, expected_due_date, delta=timedelta(seconds=10))

    def test_task_attributes_defaults_override(self):
        """ Check that the default values of a task are overriden """

        # Setup test data
        now = datetime.now()
        new_task = Task(
            title='mock title',
            description='mock description',
            status=TaskStatus.STARTED,
            due_date=now
        )

        # Assert test data
        self.assertEqual(new_task.title, 'mock title')  # check default value is overriden
        self.assertEqual(new_task.description, 'mock description')  # check default value is overriden
        self.assertEqual(new_task.status, TaskStatus.STARTED)  # check default value is overriden
        self.assertEqual(new_task.due_date, now)  # check default value is overriden

    def test_task_initialization_with_incorrect_types(self):
        """ Check that the types for the class instances are checked upon initialization """

        # Check if invalid types raises an exception
        with self.assertRaises(TypeError):
            # title must be of type str
            Task(title=123)

        with self.assertRaises(TypeError):
            # description must be of type str
            Task(description=123)

        with self.assertRaises(TypeError):
            # status must be an object of (enum) TaskStatus
            Task(status="InvalidState")

        with self.assertRaises(TypeError):
            # due_date must be a datetime object
            Task(due_date="InvalidDate")

    def test_task_modification_with_incorrect_types(self):
        """ Check that the types for the class instances are checked upon modification """

        # Setup test data
        new_task = Task()

        # Check if modification with an invalid type raises an exception
        with self.assertRaises(TypeError):
            # title must be of type str
            new_task.title = 123

        with self.assertRaises(TypeError):
            # description must be of type str
            new_task.description = 123

        with self.assertRaises(TypeError):
            # status must be an object of (enum) TaskStatus
            new_task.status = "InvalidState"

        with self.assertRaises(TypeError):
            # due_date must be a datetime object
            new_task.due_date = "InvalidDate"


class TestEnforceTypesDecorator(unittest.TestCase):
    """ Test for the enforce_types decorator. This decorator should work an any
        arbitrary class with annotated attributes
    """

    def test_correct_init(self):
        """Test correct initialization of MockedClass instance."""
        mocked_instance = MockedClass()
        self.assertIsInstance(mocked_instance, MockedClass)

    def test_incorrect_init(self):
        """Test incorrect initialization of MockedClass instance."""
        with self.assertRaises(TypeError):
            MockedClass(is_boolean="false")

    def test_correct_modification(self):
        """Test correct modification of MockedClass attributes."""
        mocked_instance = MockedClass()
        mocked_instance.is_boolean = True
        mocked_instance.is_integer = 1
        self.assertEqual(mocked_instance.is_boolean, True)
        self.assertEqual(mocked_instance.is_integer, 1)

    def test_incorrect_modification_1(self):
        """Test incorrect modification of MockedClass attributes."""
        mocked_instance = MockedClass()
        with self.assertRaises(TypeError):
            # attribute is_boolean must be a boolean
            mocked_instance.is_boolean = "false"

    def test_incorrect_modification_2(self):
        """Test incorrect modification of MockedClass attributes."""
        mocked_instance = MockedClass()
        with self.assertRaises(TypeError):
            # attribute is_integer must be an integer
            mocked_instance.is_integer = "0"
