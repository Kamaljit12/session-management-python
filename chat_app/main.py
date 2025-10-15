# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
import uuid
from langchain_groq import ChatGroq
from chat_memory import save_memory, load_memory

app = FastAPI(title="Chatbot with Memory API")

# Active sessions (temporary memory cache)
active_sessions = {}

# -------------------------------
# 1️⃣ Define Request/Response Models
# -------------------------------
class ChatRequest(BaseModel):
    session_id: str | None = None
    query: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    history: list


# -------------------------------
# 2️⃣ Mock Chatbot Logic (replace with Groq, OpenAI, etc.)
# -------------------------------
def chatbot_response(user_message: str) -> str:
    # For now, just a simple rule-based mock
    model = ChatGroq(model="")
    pass


# -------------------------------
# 3️⃣ Chat Endpoint
# -------------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Step 1: If no session_id, create a new one
    if not request.session_id:
        session_id = str(uuid.uuid4())
        memory = ConversationBufferMemory(return_messages=True)
        active_sessions[session_id] = memory
    else:
        session_id = request.session_id
        # Load from memory or database
        memory = active_sessions.get(session_id)
        if memory is None:
            memory = load_memory(session_id) or ConversationBufferMemory(return_messages=True)
            active_sessions[session_id] = memory

    # Step 2: Get chatbot response
    user_msg = request.query
    memory.chat_memory.add_user_message(user_msg)
    bot_response = chatbot_response(user_msg)
    memory.chat_memory.add_ai_message(bot_response)

    # Step 3: Save to SQL DB
    save_memory(session_id, memory)

    # Step 4: Prepare response
    history = [
        {"role": "user" if msg.type == "human" else "assistant", "content": msg.content}
        for msg in memory.chat_memory.messages
    ]

    return ChatResponse(session_id=session_id, response=bot_response, history=history)


# -------------------------------
# 4️⃣ Get all sessions (optional)
# -------------------------------
@app.get("/sessions")
def list_sessions():
    from database import SessionLocal
    from models import ChatSession

    db = SessionLocal()
    sessions = db.query(ChatSession).all()
    db.close()

    return [
        {"session_id": s.session_id, "created_at": s.created_at, "updated_at": s.updated_at}
        for s in sessions
    ]


# -------------------------------
# 5️⃣ Get conversation by session_id
# -------------------------------
@app.get("/session/{session_id}")
def get_session(session_id: str):
    memory = load_memory(session_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Session not found")

    history = [
        {"role": "user" if msg.type == "human" else "assistant", "content": msg.content}
        for msg in memory.chat_memory.messages
    ]

    return {"session_id": session_id, "history": history}
