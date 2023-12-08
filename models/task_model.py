from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


def enforce_types(cls):
    """ Decorator method. Its purpose is to enforce the types for class attributes
        used upon initialization and modification.
    """

    class Wrapper(cls):
        """ This wrapper class overrides the __init__ and __setattr__ of the wrapped
            class in order to check if the type of its attributes adhere to its annotation
        """

        def __init__(self, *args, **kwargs):
            """ Override the 'dunder' __init__ in order to check for correct types upon
                initialization.
            """
            super().__init__(*args, **kwargs)
            self._check_types()

        def __setattr__(self, name, value):
            """ Override the 'dunder' __setattr__ in order to check for correct types upon
                modification.
            """
            super().__setattr__(name, value)
            self._check_types()

        def _check_types(self):
            """ Check each class attribute using its annotation for correct types """

            # Get all attributes and its values of the class
            for attribute_name, attribute_type in self.__annotations__.items():
                # get the value for the attribute 'field_name'
                attribute_value = getattr(self, attribute_name)

                # if the field its value is not of the type (annotation) for this field, raise an exception
                if not isinstance(attribute_value, attribute_type):
                    raise TypeError(f"Invalid type for '{attribute_name}': {type(attribute_value).__name__}")

    # Return the wrapped class with the overridden 'dunders'.
    return Wrapper


class TaskStatus(Enum):
    """
    Enum class for the status of a task.

    The reason to use an ENUM (instead of e.g. boolean: completed) for a task status
    is that it can be easily extended without mayor code changes (e.g. DISCARDED)
    """
    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"
    # DISCARDED = "discarded"


@enforce_types
@dataclass
class Task:
    """
    This dataclass hold the simple structure for a class. It sets some default attribute values upon
    initialization (see below)

    Example usage:

    task_item = Task(
        title="Coding Assignment",
        description="Complete data structure"
    )
    print(task_item)

    Default values:

    title: 'new task'
    description: 'description'
    status: pending
    due_date: datetime object set to a week from now

    """

    # Set annotations for class attributes
    title: str = "New task"
    description: str = "Description"
    status: TaskStatus = TaskStatus.PENDING
    due_date: datetime = datetime.now() + timedelta(weeks=1)
