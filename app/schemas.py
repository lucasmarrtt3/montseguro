from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskCreate(TaskBase):
    title: str
    description: str
    completed: bool = False

class TaskUpdate(TaskBase):
    pass
