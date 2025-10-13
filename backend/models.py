from pydantic import BaseModel
from typing import List, Dict

class ChatRequest(BaseModel):
    session_id: str = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    history: List[Dict[str, str]]

class Session(BaseModel):
    session_id: str
    created_at: str