""" This program will ingest mocked tasks into the database via the /task API """
import datetime
import random
import requests
import lorem
from models.task_model import TaskStatus


def ingest_tasks():
    """ Create a bunch of mocked tasks """

    # Print warning message for end-user
    print('Creating 10000 mocked tasks in the database. This might take a while')

    # Create a thousand tasks for the next year
    for i in range(10000):
        # Create mocked attribute values for the new task at hand
        title = lorem.sentence()  # Single title
        description = lorem.paragraph()  # A paragraph of descriptive text
        status = random.choice(list(TaskStatus)).value  # A random task status
        due_date = (
                datetime.datetime.now() + datetime.timedelta(weeks=1) +
                datetime.timedelta(days=random.randint(0, 365))
        ).isoformat()  # A random date between next week and a year from now

        # Create the payload
        payload = {'title': title, 'description': description, 'status': status, 'due_date': due_date}

        # Send the payload across the wire
        response = requests.post('http://127.0.0.1:5000/api/task', json=payload, timeout=1)

        # Print response status code
        if response.status_code == 200:
            print(f'\r{i + 1}/10000', end='')
        else:
            print(response.status_code)


if __name__ == "__main__":
    ingest_tasks()
