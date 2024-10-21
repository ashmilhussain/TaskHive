from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime,timezone
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import relationship

from models.base import Base

# SQLAlchemy model
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)  # Auto-incremented
    name = Column(String, index=True)
    mobile = Column(String, index=True)
    email = Column(String, index=True)
    organization = Column(String, index=True)
    created_time = Column(DateTime, default=datetime.now(timezone.utc))  # Automatically set to current time
    last_activity_time = Column(DateTime, default=datetime.now(timezone.utc))  # Automatically set to current time

    tasks = relationship("Task", back_populates="contact")  # Ensure this line is present

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types like SQLAlchemy Column

# Pydantic model
class ContactCreate(BaseModel):
    name: str
    mobile: Optional[str] = None  # Optional field
    email: Optional[str] = None  # Optional field
    organization: Optional[str] = None  # Optional field

    class Config:
        orm_mode = True  # Enable ORM mode to read data as dictionaries

# Pydantic model
class ContactUpdate(BaseModel):
    name:  Optional[str] = None  # Optional field
    mobile: Optional[str] = None  # Optional field
    email: Optional[str] = None  # Optional field
    organization: Optional[str] = None  # Optional field

    class Config:
        orm_mode = True  # Enable ORM mode to read data as dictionaries

class ContactResponse(BaseModel):
    id: int
    name: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    organization: Optional[str] = None
    created_time: datetime
    last_activity_time: datetime

    class Config:
        orm_mode = True  # Enable ORM mode to read data as dictionaries