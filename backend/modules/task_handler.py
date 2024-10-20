from string import Template
from modules.openai import openai_call
from loguru import logger

class TaskHandler():

    def handle(self,intent,action,query) -> str:
        logger.info("passing through => task_handler")
        logger.info("intent received => ", intent)
        logger.info("action received => ", action)
        return "tasks"