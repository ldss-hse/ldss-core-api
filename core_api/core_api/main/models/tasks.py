"""
A module with ORM model for tasks
"""
from sqlalchemy import Column, Integer, String, Boolean, Text

from core_api.extensions.database import BASE


class TasksModel(BASE):
    """
    ORM Class for working with tasks
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    is_cancelled = Column(Boolean(), default=False)
    task_description=Column(Text(), default='')

    def __init__(self, name=None, task_description=''):
        self.name = name
        self.task_description = task_description

    def __repr__(self):
        return f'<Task {self.name!r}>'
