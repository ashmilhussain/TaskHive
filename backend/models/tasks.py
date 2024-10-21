from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime,timezone
from pydantic import BaseModel
from models.base import Base
from typing import Optional
from datetime import date
from models.contacts import Contact
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)  # Auto-incremented
    title = Column(String, index=True)
    description = Column(String, index=True)
    type = Column(String, index=True)  # Optional field
    contact_id = Column(Integer, ForeignKey('contacts.id'))  # Define foreign key
    contact = relationship("Contact", back_populates="tasks")
    due_date = Column(DateTime, default=datetime.now(timezone.utc))  # Optional field
    completed = Column(Boolean, default=False)  # Task completion status
    created_time = Column(DateTime, default=datetime.now(timezone.utc))  # Automatically set to current time

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like SQLAlchemy Column

    # Pydantic model for creating a task
class TaskCreate(BaseModel):
    title: str
    description: str
    type: str = "general"  # Optional field
    contact: Optional[str]  # Reference to Contacts
    due_date: Optional[date] = None  # Optional field
    completed: bool = False  # Default to not completed
    
    class Config:
        orm_mode = True  # Enable ORM mode to read data as dictionaries


    # Pydantic model for creating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None  # Optional field
    description: Optional[str] = None  # Optional field
    type: Optional[str] = None  # Optional field
    contact_id: Optional[int] = None  # Reference to Contacts
    due_date: Optional[date] = None  # Optional field
    completed: bool = False  # Default to not completed

    class Config:
        orm_mode = True  # Enable ORM mode to read data as dictionaries

# Pydantic model for response
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    contact : str
    completed: bool
    created_time: datetime
        
    class Config:
        orm_mode = True  # Enable ORM mode to read data as dictionaries