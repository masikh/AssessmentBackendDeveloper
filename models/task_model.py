from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


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
