from string import Template
from modules.openai import openai_call
from utils.parser import parse_llm_response
from loguru import logger
from models.tasks import TaskCreate,TaskUpdate
from tasks import add_task_to_db,update_task_in_db

class TaskHandler():

    def handle(self,db,intent,action,query) -> str:
        logger.info("passing through => task_handler")
        logger.info(f"intent received => {intent}")
        logger.info(f"action received => {action}")

        prompt = """
        You are now tasked with extracting specific task information from the user's query for task intent.

        Instructions:
        1. Extract the following information from the user query:
            - title: The title for Tasks
            - description: Description for for tasks
            - type: Type of task which can be of following ['call','sync','message','email','general']
            - contact: A task may be connected with a contact , check if the task is related to a contact and if yes extract it
            - due_date: Due date for the task, this can be only date availble

        2. If any value is not available keep "".
        Generate a response for the explanation '$query' in the following JSON format:
        {
            "title": "Extracted title if available",
            "description": "Extracted description if available",
            "type": "Extracted type if available",
            "contact": "Extracted contact if available"
            "due_date": "Extracted due_date if available"
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
            task = TaskCreate(
                title=task_info.get("title", ""),
                description=task_info.get("description", ""),
                type=task_info.get("type", ""),
                contact=task_info.get("contact", "")
            )
            out = add_task_to_db(task, next(db.get_db()))  # Ensure to get the session
            out_reposponse["status"]="task created"
            out_reposponse["message"]=out.title

        elif action =="update" :
            task = TaskUpdate()
            for field, value in task_info.items():
                if value:
                    setattr(task, field, value)
            out = update_task_in_db(4, task, next(db.get_db()))  # Ensure to get the session
            out_reposponse["status"]="task updated"
            out_reposponse["message"]=out.title
        else :
            logger.info("action didn't match")
        return out_reposponse
