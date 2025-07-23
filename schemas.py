from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Optional, Annotated
from datetime import datetime
from enum import Enum

# class TaskStatus(Enum):
#     pending = "pending"
#     in_progress = "in_progress"
#     copleted = "completed"
#     cancelled = "cancelled"

# class TaskStatusUpdate(BaseModel):
#     status: TaskStatus

class UserCreate(BaseModel):
    username: Annotated[str, StringConstraints(min_length=5, max_length=30)]
    email: EmailStr
    full_name: Optional[str] = None
    password: Annotated[str, StringConstraints(min_length=6)]

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'username': 'wallnet',
                'email': 'leviackerman@gmail.com',
                'password': 'wallnet123',
                'full_name': 'levii ackerman'
            }
        }

class UserLogin(BaseModel):
    email_or_username: str
    password: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'email_or_username': 'wallnet or leviackerman@dev.com',
                'password': 'wallnet123'
            }
        }

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'id': '1',
                'username': 'wallnet',
                'email': 'leviacckerman@dev.com',
                'full_name': 'levii ackerman',
                'is_active': True,
                'created_time': '2025-07-17'
            }
        }

class UserInDB(UserRead):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str]

    class Config:
        from_attributes = True
        json_schema_extra = {
            'exmaple':  {
                'username': 'wallnet1',
                'email': 'leviackerman@dev.com',
                'full_name': 'Levii ackerman',
                'password': 'wallnet123'
            }
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: datetime
    # status: TaskStatus
    is_done: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'title': 'reading book',
                'description': 'for iq',
                'deadline': '2025-07-20',
                'is_done': False
            }
        }

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    # status: Optional[TaskStatus]
    is_done: Optional[bool] = None

class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    deadline: datetime
    # status: TaskStatus
    is_done: bool
    craeted_time: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'id': 1,
                'title': 'reading book',
                'description': 'for iq',
                'deadline': '2025-07-19',
                'is_done': False,
                'created_time': '2025-07-18'
            }
        }

class FriendCreate(BaseModel):
    friend_id: int

class FriendRespone(BaseModel):
    id: int
    user_id: int
    friend_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'user_id': 1,
                'friend_id': 1
            }
        }

class GroupCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'name': 'google dashboard project'
            }
        }

class GroupRead(BaseModel):
    id: int
    name: str
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True

class GroupMemberAdd(BaseModel):
    user_id: int

class GroupMemberRemove(BaseModel):
    user_id: int
    group_id: int

class GroupTaskAdd(BaseModel):
    title: str
    description: Optional[str]
    deadline: datetime

class GroupTaskRead(BaseModel):
    id: int
    title: str
    description: str
    deadline: datetime
    is_done: bool
    created_at: datetime
    group_id: int
    
    class Config:
        from_attributes = True

class GroupTaskAssignmentCreate(BaseModel):
    user_id: int
    task_id: int

class GroupTaskAssigmentRead(BaseModel):
    id: int
    is_completed: bool
    assigned_at: datetime
    user_id: int
    task_id: int

    class Config:
        from_attributes = True
