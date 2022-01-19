"""
Example of creating background tasks
"""

import os
from contextlib import closing
from time import sleep

from huey import SqliteHuey
from sqlalchemy.orm import declarative_base

from core_api.extensions.database import get_db_for_asynchronous_task

import core_api.extensions.database as db

huey = SqliteHuey(filename='./db/huey.db')
db.BASE = declarative_base()


@huey.task(context=True)
def add(task=None):
    """
    Example asynchronous task
    :param task: current task instance
    :return: result of task evaluation
    """
    db_session = get_db_for_asynchronous_task()

    # pylint: disable=import-outside-toplevel
    try:
        db.BASE.query
    except AttributeError:
        db.BASE.query = db_session.query_property()
    finally:
        from core_api.main.models import TasksModel
    # pylint: enable=import-outside-toplevel

    with closing(db_session) as session:
        task = session.query(TasksModel).get(1)
        print(task)
        print('In task!!!')
        print(f'kill me please by kill -9 {os.getpid()}')
        sleep(2)

        task: TasksModel = session.query(TasksModel).get(1)
        if task.is_cancelled:
            print('Task is cancelled!!!')
            return -1

        print('Task is hard!!!')
        sleep(30)

        print('Task is very hard!!!')
        sleep(30)

        print('Task is very very hard!!!')
        print(task)
        return 0
