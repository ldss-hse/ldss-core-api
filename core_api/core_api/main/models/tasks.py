"""
A module with ORM model for tasks
"""
from sqlalchemy import Column, Integer, String, Boolean

from core_api.extensions.database import BASE


class TasksModel(BASE):
    """
    ORM Class for working with tasks
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    is_cancelled = Column(Boolean(), default=False)

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return f'<Task {self.name!r}>'
