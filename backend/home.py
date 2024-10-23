
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.contacts import Contact,ContactResponse  # Adjust the import based on your project structure
from models.notes import Note
from models.tasks import Task
from datetime import timedelta,date  
from typing import List
from loguru import logger
from models.home import HomeResponse
from models.tasks import TaskResponse
from models.notes import NoteResponse

def get_home_db(db: Session) -> HomeResponse:
    db_contact : List[ContactResponse] = db.query(Contact).order_by(Contact.last_activity_time.desc()).limit(3).all()
    db_notes : List[NoteResponse] = db.query(Note).limit(3).all()
    today = date.today()
    db_task = db.query(Task).filter(Task.due_date>= today).limit(3).all()
    task_response_list = []
    for task in db_task:
        task_response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            contact=task.contact.name if task.contact else "",  # Handle case where contact might be None
            completed=task.completed,
            created_time=task.created_time,
            due_date= task.due_date
        )
        task_response_list.append(task_response)


    return HomeResponse(
        contacts=db_contact,
        notes=db_notes,
        tasks=task_response_list)