from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from enum import Enum
from typing import Optional, List


class TaskStatus(str, Enum):
    todo = "To Do"
    in_progress = "In Progress"
    done = "Done"

class TaskPriority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

# USER SCHEMAS
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

# TASK SCHEMAS
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.medium
    status: TaskStatus = TaskStatus.todo
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class TaskCreate(TaskBase):
    assignee_ids: Optional[List[int]] = [] 

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    priority: Optional[TaskPriority]
    status: Optional[TaskStatus]
    start_date: Optional[date]
    end_date: Optional[date]
    assignee_ids: Optional[List[int]] = None  

# class TaskResponse(TaskBase):
#     id: int
#     user_id: Optional[int] = None  
#     assignees: List[UserResponse] = []

#     class Config:
#         orm_mode = True

class TaskResponse(TaskBase):
    id: int
    user_id: Optional[int] = None  
    assignees: List[UserResponse] = []

    class Config:
        from_attributes = True
