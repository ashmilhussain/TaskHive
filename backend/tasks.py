from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.tasks import Task,TaskCreate,TaskResponse  # Adjust the import based on your project structure
from typing import List

def add_task_to_db(task: TaskCreate, db: Session) -> TaskResponse:
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return TaskResponse(id=db_task.id, title=db_task.title, description=db_task.description, completed=db_task.completed, created_time=db_task.created_time)

def update_task_in_db(task_id: int, updated_task: TaskCreate, db: Session) -> TaskResponse:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for key, value in updated_task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return TaskResponse(**db_task.dict())

def delete_task_from_db(task_id: int, db: Session):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted"}

def list_tasks_from_db(db: Session) -> List[TaskResponse]:
    return db.query(Task).all()

def get_task_from_db(task_id: int, db: Session) -> TaskResponse:
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskResponse(**db_task.dict())