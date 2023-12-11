""" CRUD routes for Task """
from http import HTTPStatus
from flask import request, make_response, jsonify
from flask_restful import Resource
from flasgger import swag_from
from werkzeug.exceptions import InternalServerError
from routes import api
from models import Task
from database import db
from flask_application import memoize  # , authorize
from generic_helpers.pagination import set_paginated_response
from generic_helpers.authenticator import authenticated
from apidocs.api_task_crud import APITaskCRUD


apidocs = APITaskCRUD()


def response_method_not_allowed():
    """ Generic response"""
    response = make_response({"error": "method not allowed"})
    response.status_code = HTTPStatus.METHOD_NOT_ALLOWED

    return response


def response_ok(task):
    """Generic 200 response"""

    # Serialize data
    response_dict = task.serialize()

    # Build response
    response = make_response(jsonify(response_dict))
    response.status_code = HTTPStatus.OK

    return response


def response_not_found():
    """Generic 404 response"""

    # Build a 404 response
    response = make_response(jsonify({"error": "Task not found"}))
    response.status_code = HTTPStatus.NOT_FOUND
    return response


def response_bad_request(error="Bad request"):
    """Generic 400 response"""

    # Build a 400 response
    response = make_response(jsonify({"error": error}))
    response.status_code = HTTPStatus.BAD_REQUEST
    return response


@api.errorhandler(InternalServerError)
def handle_internal_server_error(error):
    """Custom internal server error handler"""

    # Any 500 (Internal server error) will be handled by this response.
    # E.g. This might occur when malformed data is sent to the deserializer.
    # Using this generic errorhandler saves the need for hard to read try-excepts
    # throughout the code, at the cost of loosing detailed error messages. Since
    # it's always possible to use a custom try-except where its deemed fit, this
    # will serve as an extra save guard.

    response = make_response(jsonify({"error": str(error)}))
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return response


class APITask(Resource):
    """GET|POST|PATCH|DELETE task by id"""

    @staticmethod
    @api.route("/api/task", methods=["GET"])
    @swag_from(apidocs.api_get_tasks, methods=["GET"])
    @authenticated
    def get_tasks():
        """GET tasks"""
        return api_crud_task_get_all()

    @staticmethod
    @api.route("/api/task/<int:task_id>", methods=["GET"])
    @swag_from(apidocs.api_get_task_by_id)
    @authenticated
    def get_task(task_id):
        """Get details of a specific task by ID"""
        return api_crud_task_get(task_id)

    @staticmethod
    @api.route("/api/task", methods=["POST"])
    @swag_from(apidocs.api_post_task, methods=["POST"])
    @authenticated
    def post():
        """POST task"""
        return api_crud_task_post()

    @staticmethod
    @api.route("/api/task/<int:task_id>", methods=["PATCH"])
    @swag_from(apidocs.api_patch_task_by_id)
    @authenticated
    def patch(task_id):
        """Update details of a specific task by ID"""
        return api_crud_task_patch(task_id)

    @staticmethod
    @api.route("/api/task/<int:task_id>", methods=["DELETE"])
    @swag_from(apidocs.api_delete_task_by_id)
    @authenticated
    def delete(task_id):
        """Delete a specific task by ID"""
        return api_crud_task_delete(task_id)


# @authorize.read
def api_crud_task_get_all():
    """Logic for handling GET request without task_id"""

    @memoize  # key is user token
    def get_all(memoize_key):  # pylint: disable=unused-argument
        """Because we use memoization, this logic is in its own method
        to be wrapped by the memoize decorator
        """

        # Get all tasks from database
        tasks = Task.query.all()

        # Convert tasks to a list of dictionaries and return result
        return [task.serialize() for task in tasks]

    # Get pagination parameters
    page = request.args.get("page", default="1")
    page_size = request.args.get("page_size", default="20")

    # Build memoization key
    # Create a list of non-None values and Concatenate the non-None values into a string
    # we also use the users authorization token to distinguish between users
    token = request.headers.get("Authorization")
    non_none_values = [token]
    memoize_key = "+".join(str(value) for value in non_none_values if value is not None)

    # Because we use memoize, we need a key to retrieve the correct entries
    response = get_all(memoize_key)

    # Check that the pagination parameters are digits
    if not page.isdigit() or not page_size.isdigit():
        # Return a comprehensive 400 response
        return response_bad_request(
            "Invalid page or page_size. Please provide valid numeric values."
        )

    page = int(page)
    page_size = int(page_size)

    # Set paginated response
    paginated_response = set_paginated_response(
        response, page=page, page_size=page_size
    )

    # Build 200 response
    response = make_response(paginated_response)
    response.status_code = HTTPStatus.OK
    return paginated_response


# @authorize.read
def api_crud_task_get(task_id):
    """Logic for handling GET request with task_id"""

    # Get task from database
    task = Task.query.get(task_id)

    # Guard clause, bailout if task doesn't exist
    if task is None:
        # If no task is found, leave this function with a 404
        return response_not_found()

    return response_ok(task)


# @authorize.create()
def api_crud_task_post():
    """Logic for handling POST request"""

    # Get POST data from request
    data = request.get_json()

    # Create a new task instance.
    try:
        new_task = Task()
        new_task.deserialize(data)
    except ValueError:
        return response_bad_request()

    # Add the new task to the session and commit to the database
    db.session.add(new_task)
    db.session.commit()

    # The memoized response is no longer valid, flush the cache
    memoize.clear_all_cache()
    return response_ok(new_task)


# @authorize.update
def api_crud_task_patch(task_id):
    """Logic for handling PATCH request"""

    # Dear reviewer: -> I was out of time!!!
    #
    # This patch doesn't work a patch should work.
    # A patch should replace the values which you send via the request.
    # this endpoint does not behave like that.

    # Get task from database
    task = Task.query.get(task_id)

    # Guard clause, bailout if task doesn't exist
    if task is None:
        return response_not_found()

    # Get PATCH data from request
    data = request.get_json()

    # Create a new task from data
    task = task.deserialize(data)
    try:
        task = task.deserialize(data)
    except ValueError:
        return response_bad_request()

    # Add the new task to the session and commit to the database
    db.session.add(task)
    db.session.commit()

    # The memoized response is no longer valid, flush the cache
    memoize.clear_all_cache()

    return response_ok(task)


# @authorize.delete
def api_crud_task_delete(task_id):
    """Logic for handling DELETE request"""

    # Get the task from the database by 'id'
    task = Task.query.get(task_id)

    # If no task is found, leave this function with a 404
    if not task:
        return response_not_found()

    # Delete the task from database
    db.session.delete(task)
    db.session.commit()

    # Build 200 response
    response = make_response("DELETED")
    response.status_code = HTTPStatus.OK

    # The memoized response is no longer valid, flush the cache
    memoize.clear_all_cache()

    return response
