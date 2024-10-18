from app.base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger
from string import Template
from app.utils.parser import parse_llm_response
from modules.openai import openai_call


class IntentExtracter(AbstractHandler):

    def __init__(self , model_configs) -> None:
        
        self.model_configs = model_configs

    def handle(self, request: Any) -> str:

        response = request
        logger.info("passing through => Intent extractor")

        prompt = """
        You are part of a personal assistant where you have to extract intent from users chats and match it with given intents.

        -- system context ---
        Your system will be able to help user reagrding their contacts, tasks, notes, and events.adding modiflying these items are your core capabilities

        Available intents are:
        -- Intent section ---
        contacts : to do create modify and search contacts
        tasks : to do create modify and search tasks
        notes : to do create modify and search notes
        events : to do create modify and search events
        out_of_context: If chat is irrelevant to chatbot context and its capabilities
        --- Intent section ---

        Instructions:
        1.Only one intent must be identified.Multiple intents are prohibited.
        2.Pay special attention to whether the previous intent has been completed.

        Generate a response for the user query '$question' in the following JSON format:

        {
            "explanation": "Explain how you finalized the intent based on user context and instructions. Include your reasoning for determining whether the previous intent was completed or if the current query relates to a new intent.",
            "intent": "Detected intent, strictly one from the $capability_list"
        }
        """


        response = openai_call(prompt)
        if response["error"] is not None:
            return logger.error(response["error"])

        response["intent_extractor"] = parse_llm_response(response['content'])

        return super().handle(response)


