from pydantic import BaseModel

# Chat message model
class ChatMessage(BaseModel):
    message: str