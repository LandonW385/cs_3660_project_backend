from pydantic import BaseModel

# Define request model
class MessageResponse(BaseModel):
    message: str