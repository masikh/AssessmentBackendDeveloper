""" search route for Task """
from http import HTTPStatus
from flask import request, make_response, jsonify
from routes import api
from models import Task
from generic_helpers.levenshtein import search_by_levenshtein


def response_bad_request():
    """ Generic 400 response """

    # Build a 400 response
    response = make_response(jsonify({'error': 'Bad request'}))
    response.status_code = HTTPStatus.BAD_REQUEST
    return response


@api.route('/api/task/search', methods=['GET'])
def api_search_task():
    """ Search through the tasks by title """

    # Get the value of the 'title' query parameter
    query = request.args.get('query', default=None)

    # Return Bad request is the query is None
    if query is None:
        return response_bad_request()

    # Search
    results = search_by_levenshtein(query, model=Task, field_name='title')

    # Convert tasks to a list of dictionaries
    tasks_list = [task_tuple[0].serialize() for task_tuple in results]

    # Build 200 response
    response = make_response(tasks_list)
    response.status_code = HTTPStatus.OK
    return response
