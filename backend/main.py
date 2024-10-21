from fastapi import FastAPI, Depends
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from utils.dbutils import DBUtils

from models.contacts import ContactCreate,ContactResponse  # Ensure correct imports
from models.tasks import TaskCreate, TaskResponse
from models.notes import NoteCreate, NoteResponse

from models.chat import ChatMessage

from contacts import add_contact_db,list_contacts_db,update_contact_db,delete_contact_db,get_contact_db
from tasks import add_task_to_db, update_task_in_db, delete_task_from_db, list_tasks_from_db, get_task_from_db
from notes import add_note_to_db, update_note_in_db, delete_note_from_db, list_notes_from_db, get_note_from_db

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
def delete_contact(contact_id: int,dbSession : Session = Depends(DB.get_db)):
    return delete_contact_db(contact_id, dbSession)

@app.get("/contacts", response_model=List[ContactResponse])
def list_contacts(dbSession : Session = Depends(DB.get_db)):
    return list_contacts_db(dbSession)

@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    return get_contact_db(contact_id, dbSession)


# Endpoint to add a task
@app.post("/tasks", response_model=TaskResponse)
def add_task(task: TaskCreate,dbSession : Session = Depends(DB.get_db)):
    return add_task_to_db(task, dbSession)

# Endpoint to update a task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskCreate,dbSession : Session = Depends(DB.get_db)):
    return update_task_in_db(task_id, updated_task, dbSession)

# Endpoint to delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int,dbSession : Session = Depends(DB.get_db)):
    return delete_task_from_db(task_id, dbSession)

# Endpoint to list tasks
@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(dbSession : Session = Depends(DB.get_db)):
    return list_tasks_from_db(dbSession)

# Endpoint to get a specific task
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int,dbSession : Session = Depends(DB.get_db)):
    return get_task_from_db(task_id, dbSession)


# Endpoint to add a note
@app.post("/notes", response_model=NoteResponse)
def add_note(note: NoteCreate, dbSession: Session = Depends(DB.get_db)):
    return add_note_to_db(note, dbSession)

# Endpoint to update a note
@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, updated_note: NoteCreate, dbSession: Session = Depends(DB.get_db)):
    return update_note_in_db(note_id, updated_note, dbSession)

# Endpoint to delete a note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, dbSession: Session = Depends(DB.get_db)):
    return delete_note_from_db(note_id, dbSession)

# Endpoint to list notes
@app.get("/notes", response_model=List[NoteResponse])
def list_notes(dbSession: Session = Depends(DB.get_db)):
    return list_notes_from_db(dbSession)

# Endpoint to get a specific note
@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, dbSession: Session = Depends(DB.get_db)):
    return get_note_from_db(note_id, dbSession)


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
