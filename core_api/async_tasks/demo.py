import os
from contextlib import closing
from time import sleep

from huey import SqliteHuey
from sqlalchemy.orm import declarative_base

from core_api.extensions.database import get_db_for_asynchronous_task
#
from sqlalchemy import Column, Integer, String

import core_api.extensions.database as db


huey = SqliteHuey(filename='./db/huey.db')
db.Base = declarative_base()

@huey.task(context=True)
def add(a, b, task=None):
    db_session = get_db_for_asynchronous_task()
    try:
        db.Base.query
    except AttributeError:
        db.Base.query = db_session.query_property()
    finally:
        from core_api.main.models import TasksModel

    with closing(db_session) as session:
        accuracy_job = session.query(TasksModel).get(1)
        print(accuracy_job)
        print('In task!!!')
        print(f'kill me please by kill -9 {os.getpid()}')
        print(f'B is {b}')
        sleep(2)
        accuracy_job: TasksModel = session.query(TasksModel).get(1)
        if accuracy_job.is_cancelled:
            print('Task is cancelled!!!')
            return -1
        print('Task is hard!!!')
        print(f'After: B is {b}')
        sleep(30)
        print('Task is very hard!!!')
        sleep(30)
        print('Task is very very hard!!!')
        print(dir(task))
        print(task)
        return a
