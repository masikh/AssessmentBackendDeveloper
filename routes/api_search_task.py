""" search route for Task """
from datetime import datetime
from http import HTTPStatus
from flask import request, make_response, jsonify
from routes import api
from models import Task, TaskStatus
from generic_helpers.levenshtein import search_by_levenshtein
from generic_helpers.is_valid_enum import is_valid_enum
from generic_helpers.pagination import set_paginated_response
from generic_helpers.authenticator import authenticated
from flask_application import memoize


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


@memoize
# pylint: disable=too-many-arguments
def handle_search_request(
        user_token,  # pylint: disable=unused-argument
        query=None,
        status=None,
        after=None,
        before=None,
        sort_order=None):
    """ Memoized handler for search request

        Method supports searching, filtering and sorting
    """

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

    # set sort_order
    reverse_order = bool(sort_order == 'descending')

    # return sorted result
    return sorted(tasks_list, key=sort_by_due_date, reverse=reverse_order)


@api.route('/api/task/search', methods=['GET'])
@authenticated
def api_search_task():
    """ Search through the tasks by title """

    # Get the value of the query parameter
    query = request.args.get('title', default=None)

    # Get pagination parameters
    page = request.args.get('page', default='1')
    page_size = request.args.get('page_size', default='20')

    # Some filtering query parameters. It's possible to filter on status and date (after AND before)
    # If Filtering on due_date request it's mandatory to provide both 'after' and 'before'
    status = request.args.get('status', default=None)
    after = request.args.get('after', default=None)
    before = request.args.get('before', default=None)

    # Sorting parameter, default is descending
    sort_order = request.args.get('sort_order', default='descending')

    # Build memoization key
    # Create a list of non-None values and Concatenate the non-None values into a string
    # we also use the users authorization token to distinguish between users
    token = request.headers.get('Authorization')
    non_none_values = [token, query, status, after, before, sort_order]
    memoize_key = '+'.join(str(value) for value in non_none_values if value is not None)

    # Guard clauses

    # Check that the pagination parameters are digits
    if not page.isdigit() or not page_size.isdigit():
        # Return a comprehensive 400 response
        return response_bad_request("Invalid page or page_size. Please provide valid numeric values.")

    page = int(page)
    page_size = int(page_size)

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

    # Because we make use of a memoization decorator,
    # we moved all code to a decorated handle_search_request method
    tasks_list = handle_search_request(
        memoize_key,
        query=query,
        status=status,
        after=after,
        before=before,
        sort_order=sort_order
    )

    # Set paginated response
    paginated_response = set_paginated_response(tasks_list, page=page, page_size=page_size)

    # Build 200 response
    response = make_response(paginated_response)
    response.status_code = HTTPStatus.OK
    return paginated_response
