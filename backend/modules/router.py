from base.abstract_handlers import AbstractHandler
from typing import Any
from loguru import logger


class Router(AbstractHandler):
    """
    A handler that routes requests to appropriate handlers based on the detected intent.

    The Router class determines the correct handler to process the request based on the intent extracted
    from the request. It forwards the request to the appropriate handler or returns a fallback response
    if no suitable handler is found.

    Attributes:
        fallback_handler (AbstractHandler): Handler to process requests that do not match any specific intent.
        general_handler (AbstractHandler): Handler for general intent processing.
        capability_handler (AbstractHandler): Handler for capability-related intents.
        metadata_handler (AbstractHandler): Handler for metadata-related intents.
    """


    def __init__(self,db,fallback_handler, contact_handler, task_handler,notes_handler) -> None:
        """
        Initializes the Router with the provided handlers.

        Args:
            common_context (dict): Shared context information used across handlers.
            fallback_handler (AbstractHandler): Handler for fallback responses.
            general_handler (AbstractHandler): Handler for general intent processing.
            capability_handler (AbstractHandler): Handler for capability-related intents.
            metadata_handler (AbstractHandler): Handler for metadata-related intents.
        """

        self.fallback_handler = fallback_handler
        self.contact_handler = contact_handler
        self.task_handler = task_handler
        self.notes_handler = notes_handler
        self.db = db


    def handle(self,request: Any) -> str:
        """
        Routes the request to the appropriate handler based on the detected intent.


        Args:
            request (Any): The incoming request containing intent information.

        Returns:
            str: The result of the handled request.
        """

        logger.info("passing through => Router")
        response = request

        intent_extractor = request.get("intent_extractor", {})
        intent = intent_extractor.get("intent", "")
        action = intent_extractor.get("action", "")
        query = request.get("query", {})
        if intent:
            if intent == "contact":
                return self.contact_handler.handle(self.db,intent,action,query)
            elif intent == "task":
                return self.contact_handler.handle(intent,action,query)
            elif intent == "notes":
                return self.contact_handler.handle(intent,action,query)
            else:
                response = "Sorry, I can't help you with that. Is there anything i can help you with ?"
                return self.fallback_handler.handle(response)

        else:
            logger.info("No intents detected")
            response = "Sorry, I can't help you with that. Is there anything i can help you with ?"
            return self.fallback_handler.handle(response)
