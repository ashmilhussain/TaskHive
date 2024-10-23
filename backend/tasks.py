from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.tasks import Task,TaskCreate,TaskUpdate,TaskResponse  # Adjust the import based on your project structure
from typing import List
from models.contacts import Contact  # Adjust the import based on your project structure
from loguru import logger

def add_task_to_db(task: TaskCreate, db: Session) -> TaskResponse:
    contact = db.query(Contact).filter(Contact.name == task.contact).first()  # Find contact by name
    logger.info(f"Log for contact {Contact.name} {task.contact} {contact}")
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")  # Handle case where contact is not found
    taskdict = task.dict()
    taskdict.pop('contact', None)
    db_task = Task(**taskdict, contact_id=contact.id,contact=contact)  # Use contact ID for the task
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return TaskResponse(id=db_task.id, title=db_task.title, description=db_task.description,contact=contact.name, completed=db_task.completed, created_time=db_task.created_time)

def update_task_in_db(task_id: int, updated_task: TaskCreate, db: Session) -> TaskResponse:
    db_task = db.query(TaskUpdate).filter(TaskUpdate.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in updated_task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return TaskResponse(id=db_task.id, title=db_task.title, description=db_task.description, completed=db_task.completed, created_time=db_task.created_time)

def delete_task_from_db(task_id: int, db: Session):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}

def list_tasks_from_db(db: Session) -> List[TaskResponse]:
    tasks = db.query(Task).all()  # Fetch all tasks
    task_response_list = []
    for task in tasks:
        task_response = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            contact=task.contact.name if task.contact else "",  # Handle case where contact might be None
            completed=task.completed,
            created_time=task.created_time
        )
        task_response_list.append(task_response)  # Append the task_response to the list
    # ... existing code to process task_response ...
    # Loop through tasks to assign contact name
    return task_response_list

def get_task_from_db(task_id: int, db: Session) -> TaskResponse:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info(f"Contact {task_dict}")
    task_dict = db_task.dict()
    task_dict["contact"] = db_task.contact.name
    return TaskResponse(**task_dict)
