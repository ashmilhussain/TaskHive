from fastapi import FastAPI, Depends
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from utils.dbutils import DBUtils

from models.contacts import ContactCreate,ContactResponse  # Ensure correct imports
from models.tasks import TaskCreate, TaskResponse
from models.chat import ChatMessage
from contacts import add_contact_db,list_contacts_db,update_contact_db,delete_contact_db,get_contact_db

# Import the new functions from tasks.py
from tasks import add_task_to_db, update_task_in_db, delete_task_from_db, list_tasks_from_db, get_task_from_db
from starlette.requests import Request
from chains.init_chain import intent_chain
from sqlalchemy.orm import Session


app = FastAPI()

DB = DBUtils()
dbSession : Session = Depends(DB.get_db)

app.chain = intent_chain(DB)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/contacts", response_model=ContactResponse)
def add_contact(contact: ContactCreate,dbSession : Session = Depends(DB.get_db)):
    return add_contact_db(contact,dbSession)

@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, updated_contact: ContactCreate,dbSession : Session = Depends(DB.get_db)):
    return update_contact_db(contact_id, updated_contact, dbSession)

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    return delete_contact_db(contact_id, dbSession)

@app.get("/contacts", response_model=List[ContactResponse])
def list_contacts():
    return list_contacts_db()

@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    return get_contact_db(contact_id, dbSession)


# Endpoint to add a task
@app.post("/tasks", response_model=TaskResponse)
def add_task(task: TaskCreate):
    return add_task_to_db(task, dbSession)

# Endpoint to update a task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskCreate):
    return update_task_in_db(task_id, updated_task, dbSession)

# Endpoint to delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    return delete_task_from_db(task_id, dbSession)

# Endpoint to list tasks
@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks():
    return list_tasks_from_db(dbSession)

# Endpoint to get a specific task
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    return get_task_from_db(task_id, dbSession)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_response(chat_message: ChatMessage,request: Request):

    out = app.chain.invoke({
        "question": chat_message.message,
    })
    return out

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
