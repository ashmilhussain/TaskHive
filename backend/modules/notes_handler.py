from string import Template
from modules.openai import openai_call
from utils.parser import parse_llm_response
from loguru import logger
from models.notes import NoteCreate,NoteUpdate
from notes import add_note_to_db,update_note_in_db

class NotesHandler():

    def handle(self,db,intent,action,query) -> str:
        logger.info("passing through => notes_handler")
        logger.info(f"intent received => {intent}")
        logger.info(f"action received => {action}")

        prompt = """
        You are now tasked with extracting specific notes information from the user's query for notes intent.

        Instructions:
        1. Extract the following information from the user query:
            - description: Description for for tasks
            - title: The title for Tasks
            - contact: A task may be connected with a contact , check if the task is related to a contact and if yes extract it

        2. If any value is not available keep "".
        Generate a response for the explanation '$query' in the following JSON format:
        {
            "description": "Extracted description if available",
            "title": "Extracted title if available if not avialble create a short one based on description",
            "contact": "Extracted contact if available"
        }
        """

        prompt = Template(prompt).safe_substitute(
            query = query,
        )
        response = openai_call(prompt)
        response["content"] = parse_llm_response(response["content"])
        out_reposponse = {}
        task_info = response["content"]

        if action == "create" :
            note = NoteCreate(  # Changed from TaskCreate to NoteCreate
                title=task_info.get("title", ""),
                description=task_info.get("description", ""),
                contact=task_info.get("contact", "")  # Retained contact field
            )
            out = add_note_to_db(note, next(db.get_db()))  # Changed function to add_note_to_db
            out_reposponse["status"] = "note created"  # Updated status message
            out_reposponse["message"] = out.title

        elif action == "update" :
            note = NoteUpdate()  # Changed from TaskUpdate to NoteUpdate
            for field, value in task_info.items():
                if value:
                    setattr(note, field, value)  # Retained field setting
            out = update_note_in_db(4, note, next(db.get_db()))  # Changed function to update_note_in_db
            out_reposponse["status"] = "note updated"  # Updated status message
            out_reposponse["message"] = out.title
        else :
            logger.info("action didn't match")
        return out_reposponse