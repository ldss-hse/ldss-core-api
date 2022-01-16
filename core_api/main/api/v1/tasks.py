import json

from flask import request, jsonify
from flask_pydantic_spec import Request, Response
from flask_restful import Resource
from flask_pydantic import validate

from core_api import PYDANTIC_VALIDATOR
from core_api.main.models.tasks import TasksModel
from core_api.extensions.database import get_database_session_for_flask

from . import V1_API_BLUEPRINT
from .schemas.task_create_request import TaskCreateRequestBodyModel, TaskCreateResponseMessage


@V1_API_BLUEPRINT.route('/tasks', methods=['GET'])
def get():
    return {'this is': 'tasks get'}


@V1_API_BLUEPRINT.route('/tasks', methods=['POST'])
@PYDANTIC_VALIDATOR.validate(body=Request(TaskCreateRequestBodyModel), resp=Response(HTTP_200=TaskCreateResponseMessage, HTTP_403=None), tags=['api'])
def post():
    u = TasksModel(name=request.context.body.name)
    get_database_session_for_flask().add(u)
    get_database_session_for_flask().commit()

    response = {
        'taskID': u.id
    }
    return response
