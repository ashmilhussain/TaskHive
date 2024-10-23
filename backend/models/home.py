from models.contacts import ContactResponse  # Ensure correct imports
from models.tasks import TaskResponse
from models.notes import NoteResponse
from pydantic import BaseModel
from typing import List

# Pydantic model for response
class HomeResponse(BaseModel):
    contacts : List[ContactResponse]
    tasks : List[TaskResponse]
    notes : List[NoteResponse]