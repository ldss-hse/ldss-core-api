"""
Schemas for validation of task creation REST request
"""

from pydantic import BaseModel, Field


class TaskCreateRequestBodyModel(BaseModel):
    """
    A scheme for a REST request
    """
    name: str = Field(...,
                      title='Name of task',
                      description='Name of long running background task',
                      min_length=3)


class TaskCreateResponseMessage(BaseModel):
    """
    A scheme for a REST responce
    """
    taskID: int = Field(...,
                        title='ID of task',
                        description='UUID of a just submitted task',
                        gt=0
                        )
