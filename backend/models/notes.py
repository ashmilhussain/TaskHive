from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime,timezone
from pydantic import BaseModel
from models.base import Base
from typing import Optional
from datetime import date

class Note(Base):  # Changed class name from Task to Note
    __tablename__ = "notes"  # Changed table name from tasks to notes

    id = Column(Integer, primary_key=True, index=True)  # Auto-incremented
    title = Column(String, index=True)
    description = Column(String, index=True)
    type = Column(String, index=True)  # Optional field
    contact = Column(String, index=True)  # Optional field, now attached to notes
    due_date = Column(DateTime, default=datetime.now(timezone.utc))  # Optional field
    completed = Column(Boolean, default=False)  # Task completion status
    created_time = Column(DateTime, default=datetime.now(timezone.utc))  # Automatically set to current time

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like SQLAlchemy Column

    # Pydantic model for creating a note
class NoteCreate(BaseModel):  # Changed class name from TaskCreate to NoteCreate
    title: str
    description: str
    type: str = "general"  # Optional field
    contact: Optional[str] = None  # Optional field, now attached to notes
    due_date: Optional[date] = None  # Optional field
    completed: bool = False  # Default to not completed
    
    class Config:
        orm_mode = True  # Enable ORM mode to read data as dictionaries


    # Pydantic model for updating a note
class NoteUpdate(BaseModel):  # Changed class name from TaskUpdate to NoteUpdate
    title: Optional[str] = None  # Optional field
    description: Optional[str] = None  # Optional field
    type: Optional[str] = None  # Optional field
    contact: Optional[str] = None  # Optional field, now attached to notes
    due_date: Optional[date] = None  # Optional field
    completed: bool = False  # Default to not completed

    class Config:
        orm_mode = True  # Enable ORM mode to read data as dictionaries

# Pydantic model for response
class NoteResponse(BaseModel):  # Changed class name from TaskResponse to NoteResponse
    id: int
    title: str
    description: str
    completed: bool
    created_time: datetime
        
    class Config:
        orm_mode = True  # Enable ORM mode to read data as dictionaries
