from loguru import logger
from string import Template
from modules.openai import openai_call

class NotesHandler():

    def handle(self,intent,action,query) -> str:
        logger.info("passing through => note_handler")
        logger.info("intent received => ", intent)
        logger.info("action received => ", action)
        return "notes"