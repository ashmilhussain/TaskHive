from modules.router import Router
from modules.intent_extracter import IntentExtracter


from loguru import logger

class IntentChain:
    """
    IntentChain class represents the main processing chain for handling user intents.

    This class orchestrates various modules to process user input, extract intents,
    route requests, and manage context across interactions.

    Attributes:
        vector_store: A storage system for vector embeddings.
        data_source: A data source to be used in processing.
        context_store: A storage system for maintaining context across interactions.
        common_context (dict): A shared context dictionary used across modules.
        configs (dict): Configuration settings for the models.
        input_formatter (InputFormatter): Module for formatting user input.
        context_retriver (ContextRetreiver): Module for retrieving context.
        intent_extractor (IntentExtracter): Module for extracting intents from user input.
        post_processor (PostProcessor): Module for post-processing responses.
        router (Router): Module for routing requests to appropriate chains.
        handler: The first module in the processing chain.

    The IntentChain class follows a modular design, where each module is responsible
    for a specific part of the processing pipeline. This allows for flexibility
    and easy extension of functionality.
    """
    def __init__(self,db,post_processor,contact_handler,task_handler,note_handler):
        logger.info("loading modules into chain")


        self.common_context = {
            "chain_retries" : 0,
        }

        self.intent_extractor = IntentExtracter()
        self.router = Router(db,post_processor,contact_handler, task_handler,note_handler)

        self.intent_extractor.set_next(self.router)
        self.handler = self.intent_extractor


    def invoke(self, user_request):
        # try:
            # self.common_context["chain_retries"] = 0
            # self.common_context["context_id"] = user_request["context_id"]
            logger.info("Intent chain started")
            return self.handler.handle(user_request)
        # except Exception as error:
        #     logger.error(f"An error occurred: {error}")
        #     return "Oops! Something went wrong. Try Again!"
