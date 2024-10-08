import openai  # Add this import for OpenAI API
from fastapi import FastAPI, HTTPException, Depends
from typing import List
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean  # Add this import for task completion status
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware
import os  # Import os for environment variable access
import json  # Add this import for JSON parsing

from models.contacts import ContactCreate,ContactResponse  # Ensure correct imports
from models.tasks import TaskCreate, TaskResponse
from models.chat import ChatMessage
from contacts import add_contact_db,list_contacts_db,update_contact_db,delete_contact_db,get_contact_db

# Import the new functions from tasks.py
from tasks import add_task_to_db, update_task_in_db, delete_task_from_db, list_tasks_from_db, get_task_from_db

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./taskhive.db"  # Changed database name to taskhive
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Create the database table
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/contacts", response_model=ContactResponse)
def add_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return add_contact_db(contact,db)

@app.put("/contacts/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, updated_contact: ContactCreate, db: Session = Depends(get_db)):
    return update_contact_db(contact_id, updated_contact, db)

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    return delete_contact_db(contact_id, db)

@app.get("/contacts", response_model=List[ContactResponse])
def list_contacts(db: Session = Depends(get_db)):
    return list_contacts_db(db)

@app.get("/contacts/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    return get_contact_db(contact_id, db)


# Endpoint to add a task
@app.post("/tasks", response_model=TaskResponse)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    return add_task_to_db(task, db)

# Endpoint to update a task
@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskCreate, db: Session = Depends(get_db)):
    return update_task_in_db(task_id, updated_task, db)

# Endpoint to delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return delete_task_from_db(task_id, db)

# Endpoint to list tasks
@app.get("/tasks", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    return list_tasks_from_db(db)

# Endpoint to get a specific task
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return get_task_from_db(task_id, db)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_response(chat_message: ChatMessage):
    openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your OpenAI API key from environment variable
    prompt = (
        "Analyze the following query to determine whether the intent is to create a new contact or add a task for an existing contact. Based on the identified intent:\n\n"
        "If the intent is to create a contact, extract the name, phone number, email, and organization.\n"
        "If the intent is to add a task for an existing contact, extract the task description, due date, and identify the contact (name, phone, or email) to assign the task to.\n"
        "Return only the JSON format minified and without any markdown with the extracted details. If the intent does not match \"create_contact\" or \"add_task,\" return a JSON response with the intent as \"out_of_context.\" If any details are missing, indicate their absence with null. out put must be a minfied json for mandatory"
        "Query:\n"
        +chat_message.message+
        "Expected Output:\n"
        "Return the following JSON format:\n\n"
        "{\n"
        "  \"intent\": \"[Extracted Intent]\",\n"
        "  \"details\": {\n"
        "    \"name\": \"[Extracted Name]\",\n"
        "    \"phone\": \"[Extracted Phone Number]\",\n"
        "    \"email\": \"[Extracted Email]\",\n"
        "    \"organization\": \"[Extracted Organization]\",\n"
        "    \"task_description\": \"[Extracted Task Description]\",\n"
        "    \"due_date\": \"[Extracted Due Date]\",\n"
        "    \"assigned_contact\": {\n"
        "      \"name\": \"[Extracted Contact Name]\",\n"
        "      \"phone\": \"[Extracted Contact Phone]\",\n"
        "      \"email\": \"[Extracted Contact Email]\"\n"
        "    }\n"
        "  }\n"
        "}\n"
    )
    try:
        # Call the OpenAI API with the provided message
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Specify the model
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        
        response_message = ""
        # Use a synchronous loop to handle the response
        for chunk in response:  # Iterate over the response chunks
            if chunk.choices and chunk.choices[0].delta.content:  # Check if choices exist and content is not None
                delta_content = chunk.choices[0].delta.content  # Extract the response message
                response_message += delta_content  # Append to the response message
        print(response_message)
        # Parse the JSON response
        parsed_response = json.loads(response_message)  # Parse the JSON string
        
        # Check if the parsed response has the expected structure
        if "intent" in parsed_response and "details" in parsed_response:
            intent = parsed_response["intent"]  # Extract intent
            details = parsed_response["details"]  # Extract details
            
            # Print intent and details to the terminal
            print("Intent:", intent)  # Print the intent
            print("Details:", details)  # Print the details
        else:
            print("Error: Unexpected JSON structure:", parsed_response)

        return {"response": response_message}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))  # Return an error response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)