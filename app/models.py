
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy import Enum as PgEnum 
from sqlalchemy.orm import relationship
from app.database import Base, engine 
import enum

class TaskStatus(str, enum.Enum):
    todo = "To Do"
    in_progress = "In Progress"
    done = "Done"

class TaskPriority(str, enum.Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class User(Base): 
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(PgEnum(TaskPriority, native_enum=False), default=TaskPriority.medium)
    status = Column(PgEnum(TaskStatus, native_enum=False), default=TaskStatus.todo)
    start_date = Column(Date)
    end_date = Column(Date)

    user_id = Column(Integer, ForeignKey("users.id"))  
    owner = relationship("User", back_populates="tasks")

    assignees = relationship(
        "User",
        secondary="task_assignees",  
        backref="assigned_tasks"
    )

class TaskAssignee(Base):
    __tablename__ = "task_assignees"
    
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

Base.metadata.create_all(bind=engine)