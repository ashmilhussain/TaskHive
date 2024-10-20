from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.contacts import Contact,ContactCreate,ContactResponse  # Adjust the import based on your project structure
from datetime import datetime  # Ensure timezone is imported
from typing import List
from loguru import logger

def add_contact_db(contact: ContactCreate, db: Session) -> ContactResponse:  # Change return type to ContactResponse
    db_contact = Contact(**contact.dict())  # Create an instance of the SQLAlchemy model
    db.add(db_contact)  # Add the SQLAlchemy model instance
    db.commit()
    db.refresh(db_contact)
    
    return ContactResponse(id=db_contact.id, name=db_contact.name, email=db_contact.email,mobile=db_contact.mobile,organization=db_contact.organization,created_time=db_contact.created_time,last_activity_time=db_contact.last_activity_time)  # Adjust fields as necessary

def update_contact_db(contact_id: int, updated_contact: ContactCreate, db: Session) -> ContactResponse:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    for key, value in updated_contact.dict().items():
        if value is not None:
            setattr(db_contact, key, value)
    db_contact.last_activity_time = datetime.utcnow()  # Update last activity time
    db.commit()
    db.refresh(db_contact)
    return ContactResponse(id=db_contact.id, name=db_contact.name, email=db_contact.email,mobile=db_contact.mobile,organization=db_contact.organization,created_time=db_contact.created_time,last_activity_time=db_contact.last_activity_time)  # Adjust fields as necessary

def delete_contact_db(contact_id: int, db: Session):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(db_contact)
    db.commit()
    return {"message": "Contact deleted"}

def list_contacts_db(db: Session) -> List[ContactResponse]:
    return db.query(Contact).all()

def get_contact_db(contact_id: int, db: Session) -> ContactResponse:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return ContactResponse(**db_contact.dict())