""" This program will ingest mocked tasks into the database via the /task API """
import datetime
import json
import random
import requests
import lorem
from models.task_model import TaskStatus

USER_1 = {'name': 'user_1', 'email': 'user_1@mock', 'password': 'M0cK'}
USER_2 = {'name': 'user_2', 'email': 'user_2@mock', 'password': 'M0cK'}


def create_user():
    """ Create ingest user """
    requests.post('http://127.0.0.1:5000/api/user/create', json=USER_1, timeout=1)
    requests.post('http://127.0.0.1:5000/api/user/create', json=USER_2, timeout=1)


def get_token(user):
    """ Get token from server """
    response = requests.post('http://127.0.0.1:5000/api/user/login', json=user, timeout=1).json()
    return response.get('token')


def ingest_tasks(token=None):
    """ Create a bunch of mocked tasks """

    # Create Authorization header
    headers = {'Authorization': token}

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
        response = requests.post('http://127.0.0.1:5000/api/task', headers=headers, json=payload, timeout=3600)

        # Print response status code
        if response.status_code == 200:
            print(f'\r{i + 1}/10000', end='')
        else:
            print(response.status_code)


def ingest_tasks_user(token, titles):
    """ Create tasks """

    # Create Authorization header
    headers = {'Authorization': token}

    for title in titles:
        description = lorem.sentence()  # A paragraph of descriptive text
        status = random.choice(list(TaskStatus)).value  # A random task status
        due_date = (
                datetime.datetime.now() + datetime.timedelta(weeks=1) +
                datetime.timedelta(days=random.randint(0, 365))
        ).isoformat()  # A random date between next week and a year from now

        # Create the payload
        payload = {'title': title, 'description': description, 'status': status, 'due_date': due_date}

        # Send the payload across the wire
        requests.post('http://127.0.0.1:5000/api/task', headers=headers, json=payload, timeout=3600)


def get_tasks(token):
    """ Get tasks """

    # Create Authorization header
    headers = {'Authorization': token}

    # Get tasks for user
    response = requests.get('http://127.0.0.1:5000/api/task', headers=headers, timeout=3600).json()
    print(json.dumps(response))


def search_tasks(token):
    """ Search a task """

    # Create Authorization header
    headers = {'Authorization': token}

    # Search task
    response = requests.get(
        'http://127.0.0.1:5000/api/task/search?title=user_1',
        headers=headers,
        timeout=3600).json()
    print(json.dumps(response))


if __name__ == "__main__":
    create_user()
    user_token_1 = get_token(USER_1)
    ingest_tasks_user(user_token_1, ['user_1 title 1', 'user_1 title 2'])

    user_token_2 = get_token(USER_2)
    ingest_tasks_user(user_token_2, ['user_2 title 1', 'user_2 title 2'])

    print('user 1\n\n')
    get_tasks(user_token_1)

    print('user 2\n\n')
    get_tasks(user_token_2)

    print('search tasks\n\n')
    search_tasks(user_token_1)

    # Create a whole-lot of tasks
    ingest_tasks(user_token_1)
