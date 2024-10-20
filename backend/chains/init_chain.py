from chains.intent_chain import IntentChain  # Ensure IntentChain is imported
from modules.contact_handler import ContactHandler
from modules.task_handler import TaskHandler
from modules.notes_handler import NotesHandler
from modules.post_processor import PostProcessor

def intent_chain(db) -> IntentChain:
    post_processor = PostProcessor()
    contact_chain = ContactHandler()
    task_chain = TaskHandler()
    notes_chain = NotesHandler()
    intent_chain = IntentChain(db,post_processor,contact_chain,task_chain,notes_chain)
    return intent_chain
