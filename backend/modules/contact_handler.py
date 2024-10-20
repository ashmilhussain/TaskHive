from loguru import logger
from string import Template
from modules.openai import openai_call
from utils.parser import parse_llm_response
from contacts import add_contact_db,list_contacts_db,update_contact_db,delete_contact_db,get_contact_db
from models.contacts import ContactCreate
from sqlalchemy.orm import Session

class ContactHandler():

    def handle(self,db,intent,action,query) -> str:
        logger.info("passing through => contact_handler")
        logger.info(f"intent received => {intent}")
        logger.info(f"action received => {action}")

        prompt = """
        You are now tasked with extracting specific contact information from the user's query for contact intent.

        Instructions:
        1. Extract the following information from the user query:
            - name: The name of the contact
            - mob: The mobile number of the contact
            - email: The email address of the contact
            - organisation: The organization of the contact
        2. If any value is not available keep "".

        Generate a response for the explanation '$query' in the following JSON format:

        {
            "name": "Extracted name if available",
            "mob": "Extracted mobile number if available",
            "email": "Extracted email address if available",
            "organisation": "Extracted organization if available"
        }
        """

        prompt = Template(prompt).safe_substitute(
            query = query,
        )
        response = openai_call(prompt)
        response["content"] = parse_llm_response(response["content"])
        out = "contact triggered"
        contact_info = response["content"]
        contact = ContactCreate(
            name=contact_info.get("name", ""),
            mobile=contact_info.get("mob", ""),
            email=contact_info.get("email", ""),
            organization=contact_info.get("organisation", "")
        )
        if action == "create" :
            out = add_contact_db(contact, next(db.get_db()))  # Ensure to get the session
        elif action =="update" :
            out = update_contact_db(2,contact, next(db.get_db()))  # Ensure to get the session
        else :
            logger.info("action didn't match")
        return out
