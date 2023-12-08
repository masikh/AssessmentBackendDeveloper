""" CRUD routes for Task """
from http import HTTPStatus
from flask import request, make_response
from routes import api


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

    if request.method == 'GET':
        # Handle the get method. If there's no task id, we return all available tasks else we return the specific task
        if task_id is None:
            # Handle GET request without task_id, thus return all available tasks
            return api_crud_task_get_all()

        # Handle GET request with task_id
        return api_crud_task_get(task_id)

    if request.method == 'POST':
        # Handle POST request
        return api_crud_task_post()

    if request.method == 'PATCH':
        # Handle PATCH request
        return api_crud_task_patch(task_id)

    if request.method == 'DELETE':
        # Handle DELETE request
        return api_crud_task_delete(task_id)

    # Method is not supported
    response = make_response({'error': 'Method not supported'})
    response.status_code = HTTPStatus.METHOD_NOT_ALLOWED
    return response


def api_crud_task_get_all():
    """ Logic for handling GET request without task_id """
    response = make_response({'result': 'Hello World'})
    response.status_code = HTTPStatus.OK
    return response


def api_crud_task_get(task_id):
    """ Logic for handling GET request with task_id """
    response = make_response({'task_id': task_id})
    response.status_code = HTTPStatus.OK
    return response


def api_crud_task_post():
    """ Logic for handling POST request """
    data = request.get_json()
    response = make_response(data)
    response.status_code = HTTPStatus.OK
    return response


def api_crud_task_patch(task_id):
    """ Logic for handling PATCH request """
    data = request.get_json()
    data['task_id'] = task_id
    response = make_response(data)
    response.status_code = HTTPStatus.OK
    return response


def api_crud_task_delete(task_id):
    """ Logic for handling DELETE request """
    response = make_response({'task_id': task_id})
    response.status_code = HTTPStatus.OK
    return response
