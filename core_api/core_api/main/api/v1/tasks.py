"""
A module for REST API to create tasks
"""

import time

from flask import request
from flask_pydantic_spec import Request, Response

from core_api import PYDANTIC_VALIDATOR
from core_api.async_tasks.decision_maker.run_jar import run_decision_maker
from core_api.async_tasks.demo import add
from core_api.main.models.tasks import TasksModel
from core_api.extensions.database import get_database_session_for_flask

from . import V1_API_BLUEPRINT
from .schemas.decision_making_task import TaskDescription, TaskResult, DMTaskCreateRequestBodyModel, \
    DMTaskCreateResponseMessage
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


@V1_API_BLUEPRINT.route('/make-decision', methods=['POST'])
@PYDANTIC_VALIDATOR.validate(body=Request(DMTaskCreateRequestBodyModel),
                             resp=Response(HTTP_200=DMTaskCreateResponseMessage,
                                           HTTP_403=None),
                             tags=['api'])
def make_decision():
    """
    Endpoint to tackle creation of tasks
    :return: status of task creation
    """
    task: TasksModel = TasksModel(name='Decision Making task')

    # pylint: disable=no-member
    get_database_session_for_flask().add(task)
    get_database_session_for_flask().commit()

    decision_making_result = run_decision_maker(task_id=task.id)

    print(f'Task {task.id} has completed')

    return {
        'taskID': task.id,
        'taskResult': decision_making_result
    }
