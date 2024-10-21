from loguru import logger
from string import Template
from modules.openai import openai_call
from utils.parser import parse_llm_response
from contacts import add_contact_db,list_contacts_db,update_contact_db,delete_contact_db,get_contact_db
from models.contacts import ContactCreate,ContactUpdate

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
            - mobile: The mobile number of the contact
            - email: The email address of the contact
            - organisation: The organization of the contact
        2. If any value is not available keep "".

        Generate a response for the explanation '$query' in the following JSON format:

        {
            "name": "Extracted name if available",
            "mobile": "Extracted mobile number if available",
            "email": "Extracted email address if available",
            "organisation": "Extracted organization if available"
        }
        """

        prompt = Template(prompt).safe_substitute(
            query = query,
        )
        response = openai_call(prompt)
        response["content"] = parse_llm_response(response["content"])
        out_reposponse = {}
        contact_info = response["content"]
        if action == "create" :
            contact = ContactCreate(
                name=contact_info.get("name", ""),
                mobile=contact_info.get("mob", ""),
                email=contact_info.get("email", ""),
                organization=contact_info.get("organisation", "")
            )
            out = add_contact_db(contact, next(db.get_db()))  # Ensure to get the session
            out_reposponse["status"]="contact created"
            out_reposponse["message"]=out.name
        elif action =="update" :
            contact = ContactUpdate()
            for field, value in contact_info.items():
                if value:
                    setattr(contact, field, value)
            out = update_contact_db(4,contact, next(db.get_db()))  # Ensure to get the session
            out_reposponse["status"]="contact updated"
            out_reposponse["message"]=out.name
        else :
            logger.info("action didn't match")
        return out_reposponse
