""" __init__ for routes """

from flask import Blueprint
api = Blueprint('api', __name__)

from routes.api_crud_task import api_crud_task  # pylint: disable=wrong-import-position
from routes.api_search_task import api_search_task  # pylint: disable=wrong-import-position
