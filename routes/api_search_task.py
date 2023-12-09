""" search route for Task """
from datetime import datetime
from http import HTTPStatus
from flask import request, make_response, jsonify
from routes import api
from models import Task, TaskStatus
from generic_helpers.levenshtein import search_by_levenshtein
from generic_helpers.is_valid_enum import is_valid_enum


def response_bad_request(error):
    """ Dynamic 400 response """

    # Build a 400 response
    response = make_response(jsonify({'error': str(error)}))
    response.status_code = HTTPStatus.BAD_REQUEST
    return response


def set_and_check_date_filter_prerequisites(after, before):
    """ Check if both after and before are set"""

    # Check if both 'after' and 'before' are provided
    if after is not None and before is not None:
        # Convert 'after' and 'before' to datetime objects
        try:
            after_date = datetime.strptime(after, "%Y-%m-%d")
            before_date = datetime.strptime(before, "%Y-%m-%d")
        except ValueError as exc:
            # We raise the Value error again, so we can catch it in the calling method
            raise ValueError("Invalid date format. Use e.g. %Y-%m-%d") from exc

        # Check if 'after' is in the past of 'before'
        if after_date > before_date:
            # We raise a Value error, so we can catch it in the calling method
            raise ValueError("'after' is in the past of 'before'")

        # Return a tuple of datetime objects
        return after_date, before_date

    # either "after" or "before" is missing
    # We raise a Value error, so we can catch it in the calling method
    raise ValueError("either 'after' or 'before' is missing")


@api.route('/api/task/search', methods=['GET'])
def api_search_task():
    """ Search through the tasks by title """

    # Get the value of the query parameter
    query = request.args.get('title', default=None)

    # Some filtering query parameters. It's possible to filter on status and date (after AND before)
    # If Filtering on due_date request it's mandatory to provide both 'after' and 'before'
    status = request.args.get('status', default=None)
    after = request.args.get('after', default=None)
    before = request.args.get('before', default=None)

    # Sorting parameter, default is descenting
    sort_order = request.args.get('sort_order', default='descending')

    # Guard clauses

    # check if the used status exist
    if not is_valid_enum(status, TaskStatus):
        # Dynamically build a list of statuses
        valid_statuses = str([f'{status.value}' for status in TaskStatus])

        # Return a comprehensive 400 response
        return response_bad_request(f'invalid statuses, use one of: {valid_statuses}')

    # check if the date stamps are correct (if any!)
    if after is not None or before is not None:
        try:
            # check_date_filter raises a ValueError if a check is failed,
            # in this manner the error message can be provided to the end user
            after, before = set_and_check_date_filter_prerequisites(after, before)
        except ValueError as error:
            # Return a comprehensive 400 response
            return response_bad_request(error)

    # Check if the sort_order is either ascending or descending
    if sort_order not in ['ascending', 'descending']:
        # Return a comprehensive 400 response
        return response_bad_request("invalid sort value, use one of: ['ascending', 'descending']")

    # Build a list of tasks
    if query is None:
        # Return all tasks from the database. Serialize during the list comprehension.
        tasks_list = [task.serialize() for task in Task.query.all()]
    else:
        # Search within the tasks from the database for a match based on the query
        results = search_by_levenshtein(query, model=Task, field_name='title')
        tasks_list = [task_tuple[0].serialize() for task_tuple in results]

    # Filter results on status
    if status:
        # Build new tasks list were status matches the queried status
        tasks_list = [x for x in tasks_list if x['status'] == status]

    # Filter results on due_date
    if after and before:
        # Build new task were the tasks its due_date is in between after and before
        tasks_list = [
            x for x in tasks_list
            if after < datetime.fromisoformat(x['due_date']) < before
        ]

    # Sort the remaining task_list
    def sort_by_due_date(item):
        return datetime.fromisoformat(item['due_date'])

    reverse_order = bool(sort_order == 'descending')
    tasks_list = sorted(tasks_list, key=sort_by_due_date, reverse=reverse_order)

    # Build 200 response
    response = make_response(tasks_list)
    response.status_code = HTTPStatus.OK
    return response
