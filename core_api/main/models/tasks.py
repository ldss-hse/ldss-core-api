from sqlalchemy import Column, Integer, String

from core_api.extensions.database import Base


class TasksModel(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return f'<Task {self.name!r}>'
