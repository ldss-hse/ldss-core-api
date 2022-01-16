from flask import Blueprint
from flask_restful import Api

V1_API_BLUEPRINT = Blueprint('tasks_api', __name__)

tasks_api = Api(V1_API_BLUEPRINT)

# pylint: disable=wrong-import-position
from . import tasks
