from pydantic import BaseModel


class ChatRequest(BaseModel):
    message:str
    response:str = None


class SessionID(BaseModel):
    session_id: str