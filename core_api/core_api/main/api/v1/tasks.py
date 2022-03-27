"""
A module for REST API to create tasks
"""

import time

from flask import request
from flask_pydantic_spec import Request, Response

from core_api import PYDANTIC_VALIDATOR
from core_api.async_tasks.demo import add
from core_api.main.models.tasks import TasksModel
from core_api.extensions.database import get_database_session_for_flask

from . import V1_API_BLUEPRINT
from .schemas.task_create_request import TaskCreateRequestBodyModel, TaskCreateResponseMessage


@V1_API_BLUEPRINT.route('/tasks', methods=['GET'])
def get():
    """
    Endpoint to get list of all tasks
    :return: list of tasks
    """
    return {
        'tasks': [
            {
                'this is': 'tasks get'
            }
        ]
    }


@V1_API_BLUEPRINT.route('/tasks', methods=['POST'])
@PYDANTIC_VALIDATOR.validate(body=Request(TaskCreateRequestBodyModel),
                             resp=Response(HTTP_200=TaskCreateResponseMessage,
                                           HTTP_403=None),
                             tags=['api'])
def post():
    """
    Endpoint to tackle creation of tasks
    :return: status of task creation
    """
    task: TasksModel = TasksModel(name=request.context.body.name)

    # pylint: disable=no-member
    get_database_session_for_flask().add(task)
    get_database_session_for_flask().commit()

    response = {
        'taskID': task.id
    }

    add(task_id=task.id)

    time.sleep(0.1)

    print('Cancelled the task')
    task.is_cancelled = True
    get_database_session_for_flask().commit()

    return response
