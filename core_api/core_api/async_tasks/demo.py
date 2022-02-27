"""
Example of creating background tasks
"""

import os
from contextlib import closing
from pathlib import Path
from time import sleep
import toml

from huey import SqliteHuey
from sqlalchemy.orm import declarative_base

from core_api.extensions.database import get_db_for_asynchronous_task

import core_api.extensions.database as db

config_path = Path(__file__).parent.parent / 'settings.toml'
dev_config = toml.load(config_path)
huey_db_path = Path(__file__).parent.parent / dev_config['development']['DATABASE_DIR'] / 'huey.db'

print(f'DB Name: {huey_db_path}')

huey = SqliteHuey(filename=str(huey_db_path))
db.BASE = declarative_base()


@huey.task(context=True)
def add(task=None, task_id=None):
    """
    Example asynchronous task
    :param task_id: current task DB ID
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
        task = session.query(TasksModel).get(task_id)
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
