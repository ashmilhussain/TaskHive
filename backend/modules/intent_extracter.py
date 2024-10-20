from base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger
from string import Template
from modules.openai import openai_call
from utils.parser import parse_llm_response

class IntentExtracter(AbstractHandler):


    def __init__(self) -> None:
        """
        Initializes the IntentExtractor with common context and model configurations.

        Args:
            common_context (Any): Shared context information used across handlers.
            model_configs (dict): Configuration settings for the model.
        """
        

    def handle(self, request: Any) -> str:

        response = request
        logger.info("passing through => Intent extractor")

        prompt = """
        You are part of a personal assistant where you have to extract intent from users chats and match it with given intents.

        -- system context ---
        Your system will be able to help user reagrding their contacts, tasks and notes. actions like adding and updating these items are your core capabilities

        Available intents are:
        -- Intent Type section ---
        contact : to do create modify and search contacts
        task : to do create modify and search tasks
        note : to do create modify and search notes
        out_of_context: If chat is irrelevant to chatbot context and its capabilities
        --- Intent Type section ---

        Available actions are:
        -- Intent Action section ---
        create : to do create modify and search contacts
        update : to do create modify and search tasks
        out_of_context: If chat is irrelevant to chatbot context and its capabilities
        --- Intent Action section ---

        Instructions:
        1.Only one intent must be identified.Multiple intents are prohibited.
        2.Only one intent action must be identified.Multiple intent actions are prohibited.

        Generate a response for the user query '$question' in the following JSON format:

        {
            "explanation": "Explain how you finalized the intent based on user context and instructions",
            "intent": "Detected intent, strictly one from the Intent Type section",
            "action": "Detected intent actions, strictly one from the Intent Action section"
        }
        """

        prompt = Template(prompt).safe_substitute(
            question = request["question"],
        )

        response = openai_call(prompt)

        response["intent_extractor"] = parse_llm_response(response["content"])
        response["query"]=request["question"]
        response.pop("content", None)

        return super().handle(response)


