""" __init__ for routes """

from flask import Blueprint

doc = Blueprint("doc", __name__)
api = Blueprint("api", __name__)
auth = Blueprint("auth", __name__)

# DOC
from routes.render_readme import render_readme  # pylint: disable=wrong-import-position

# API
from routes.api_crud_task import (
    APITask,
)  # pylint: disable=wrong-import-position
from routes.api_search_task import (
    api_search_task,
)  # pylint: disable=wrong-import-position

# Auth
from routes.api_authorization import (
    api_user_create,
    api_user_login,
)  # pylint: disable=wrong-import-position
