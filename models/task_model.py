""" This file holds the model for a task and a helper function to check its types """
from datetime import datetime, timedelta
from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from database import db  # Import the db instance from the main application file


class TaskStatus(Enum):  # inheritance of the Enum class
    """
    Enum class for the status of a task.

    The reason to use an ENUM (instead of e.g. boolean: completed) for a task status
    is that it can be easily extended without mayor code changes (e.g. DISCARDED)
    """
    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"
    # DISCARDED = "discarded"


class Task(db.Model):
    """
    Simple model for a task. We use user authorization to allow to view your own tasks only

    Default values:

    title: 'new task'
    description: 'description'
    status: pending
    due_date: datetime object set to a week from now

    """
    __tablename__ = 'tasks'
    __permissions__ = {
        "owner": ['read', 'update', 'delete', 'revoke'],
        "group": [],
        "other": []
    }

    # Set annotations for class attributes (e.g. int, str etc...)
    # Also set defaults for each field
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String, default="New task")
    description: str = Column(String, default="Description")
    status: TaskStatus = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.PENDING)
    due_date: datetime = Column(db.DateTime, default=datetime.now() + timedelta(weeks=1))

    def serialize(self):
        """ serialize the task via a dict comprehension """

        # Note: using a dynamic dict comprehension here (tempting!) is more complicated due to
        # 'status' and 'due_date', which needs to be converted to a string before it can be sent
        # over the wire. Does the 'from sqlalchemy_serializer import SerializerMixin' provide any
        # solutions for cleaner abstraction?
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,  # Convert Enum to string value
            'due_date': self.due_date.isoformat()  # Convert datetime to string value
        }

    def deserialize(self, data: dict):
        """ Populate task attributes from dict (data) """

        # Note: using a dynamic dict comprehension here (tempting!) is more complicated due to
        # 'status' and 'due_date', which needs to be converted to an object before it can be sent
        # to the database. (see also: comments for serialize)
        self.title = data.get('title') if data.get('title') is not None else self.title
        self.description = data.get('description') if data.get('description') is not None else self.description
        self.status = TaskStatus(data.get('status')) if data.get('status') is not None else self.status
        self.due_date = datetime.fromisoformat(data.get('due_date')) if data.get('due_date') else self.due_date
        return self
