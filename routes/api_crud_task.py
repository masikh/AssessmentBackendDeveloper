""" CRUD routes for Task """
from http import HTTPStatus
from flask import request, make_response, jsonify
from werkzeug.exceptions import InternalServerError
from routes import api
from models import Task
from database import db


def response_ok(task):
    """ Generic 200 response """

    # Serialize data
    response_dict = task.serialize()

    # Build response
    response = make_response(jsonify(response_dict))
    response.status_code = HTTPStatus.OK

    return response


def response_not_found():
    """ Generic 404 response """

    # Build response
    response = make_response(jsonify({'error': 'Task not found'}))
    response.status_code = HTTPStatus.NOT_FOUND
    return response


def response_bad_request():
    """ Generic 404 response """

    # Build response
    response = make_response(jsonify({'error': 'Bad request'}))
    response.status_code = HTTPStatus.BAD_REQUEST
    return response


@api.errorhandler(InternalServerError)
def handle_internal_server_error(error):
    """ Custom internal server error handler """

    response = make_response(jsonify({'error': str(error)}))
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response


@api.route('/api/task', defaults={'task_id': None}, methods=['GET', 'POST', 'PATCH', 'DELETE'])
@api.route('/api/task/<int:task_id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def api_crud_task(task_id):
    """ CRUD API for tasks, depending on the HTTP-method and argument a handler is chosen

        GET: (with task_id) -> api_crud_task_get(task_id)
        GET: (without task_id) -> api_crud_task_get_all()
        POST: api_crud_task_post()
        PATCH: api_crud_task_patch(task_id)
        DELETE: api_crud_task_patch(task_id)
        *: returns a HTTPStatus.METHOD_NOT_ALLOWED with a error message

        For authorization has been omitted for this assessment, authentication well be implemented

        TODO: authentication (authorization will not be implemented for this assessment)
              pagination
              search
              filter
              apidocs
    """

    # Guard clause: If request method is POST we don't expect a task_id. If task_id is not None
    # We'll return a 'BAD_REQUEST'. For all other allowed methods a task_id is allowed.
    if request.method == 'POST' and task_id is not None:
        return response_bad_request()

    # Warning -> fully NULL primary key identity cannot load any object. This condition may
    # raise an error in a future release. error in: task = Task.query.get(task_id)
    if request.method in ['PATCH', 'DELETE'] and task_id is None:
        return response_bad_request()

    if request.method == 'GET':
        # Handle the get method. If there's no task id, we return all available tasks else we return the specific task
        if task_id is None:
            # Handle GET request without task_id, thus return all available tasks
            return api_crud_task_get_all()

        # Handle GET request with task_id
        return api_crud_task_get(task_id)

    if request.method == 'POST':
        # Handle POST request. Although it technically makes no difference if there is a task_id
        # or not. It's not clean and hence a bad_request
        if task_id is not None:
            return response_bad_request()
        return api_crud_task_post()

    if request.method == 'PATCH':
        # Handle PATCH request. If not task_id is provided we consider it a bad request
        if task_id is None:
            return response_bad_request()
        return api_crud_task_patch(task_id)

    if request.method == 'DELETE':
        # Handle DELETE request
        if task_id is None:
            return response_bad_request()
        return api_crud_task_delete(task_id)

    # Method is not supported
    response = make_response({'error': 'Method not supported'})
    response.status_code = HTTPStatus.METHOD_NOT_ALLOWED
    return response


def api_crud_task_get_all():
    """ Logic for handling GET request without task_id """

    # Get all tasks from database
    tasks = Task.query.all()

    # Convert tasks to a list of dictionaries
    tasks_list = [task.serialize() for task in tasks]

    # Build 200 response
    response = make_response(tasks_list)
    response.status_code = HTTPStatus.OK
    return response


def api_crud_task_get(task_id):
    """ Logic for handling GET request with task_id """

    # Get task from database
    task = Task.query.get(task_id)

    # Guard clause, bailout if task doesn't exist
    if task is None:
        response = make_response(jsonify({'error': 'Task not found'}))
        response.status_code = HTTPStatus.NOT_FOUND
        return response

    return response_ok(task)


def api_crud_task_post():
    """ Logic for handling POST request """

    # Get POST data from request
    data = request.get_json()

    # Create a new task instance. If the data is malformed an internal server error
    # will occur and shall be processed by the @api.errorhandler(InternalServerError)
    new_task = Task()
    new_task.deserialize(data)

    # Add the new task to the session and commit to the database
    db.session.add(new_task)
    db.session.commit()

    return response_ok(new_task)


def api_crud_task_patch(task_id):
    """ Logic for handling PATCH request """

    # Get task from database
    task = Task.query.get(task_id)

    # Guard clause, bailout if task doesn't exist
    if task is None:
        response =  make_response(jsonify({'error': 'Task not found'}))
        response.status_code = HTTPStatus.NOT_FOUND
        return response

    # Get PATCH data from request
    data = request.get_json()

    # Create a new task instance. If the data is malformed an internal server error
    # will occur and shall be processed by the @api.errorhandler(InternalServerError)
    task = task.deserialize(data)

    # Add the new task to the session and commit to the database
    db.session.add(task)
    db.session.commit()

    return response_ok(task)


def api_crud_task_delete(task_id):
    """ Logic for handling DELETE request """
    task = Task.query.get(task_id)

    if task:
        # Delete the task from database
        db.session.delete(task)
        db.session.commit()

        # Build 200 response
        response = make_response('DELETED')
        response.status_code = HTTPStatus.OK
        return response

    return response_not_found()
