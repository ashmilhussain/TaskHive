from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime,timezone
from pydantic import BaseModel
from models.base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)  # Auto-incremented
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)  # Task completion status
    created_time = Column(DateTime, default=datetime.now(timezone.utc))  # Automatically set to current time

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like SQLAlchemy Column

    # Pydantic model for creating a task
class TaskCreate(BaseModel):
    title: str
    description: str
    completed: bool = False  # Default to not completed

    class Config:
        orm_mode = True  # Enable ORM mode to read data as dictionaries

# Pydantic model for response
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    created_time: datetime
        
    class Config:
        orm_mode = True  # Enable ORM mode to read data as dictionaries