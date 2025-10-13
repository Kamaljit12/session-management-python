from backend.models import ChatRequest, ChatResponse, Session
from backend.database import init_db, get_connection
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.chatbot import get_response
from typing import List
import uuid


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ Run at startup
    init_db()
    print("✅ Database initialized")

    # yield to keep app running
    yield

    # 🧹 Run at shutdown (optional cleanup)
    print("🛑 Shutting down...")

app = FastAPI(lifespan=lifespan, title="Chat Session API", version="1.0.0")


# 🗨️ Chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    query = request.message
    response = get_response(query)
    return {"response": response}


@app.post("/chat_with_sql", response_model=ChatResponse)
async def chat(request: ChatRequest):
    conn = get_connection()
    cur = conn.cursor()

    # 1️⃣ Create new session if not provided
    session_id = request.session_id or str(uuid.uuid4())

    # If new, insert into sessions table
    cur.execute("INSERT OR IGNORE INTO sessions (session_id) VALUES (?)", (session_id,))

    # 2️⃣ Store user message
    cur.execute("INSERT INTO messages (session_id, role, text) VALUES (?, ?, ?)",
                (session_id, "user", request.message))

    # 3️⃣ Generate bot response (replace with your model logic)
    bot_response = get_response(request.message)
    cur.execute("INSERT INTO messages (session_id, role, text) VALUES (?, ?, ?)",
                (session_id, "bot", bot_response))

    conn.commit()

    # 4️⃣ Retrieve full chat history
    cur.execute("SELECT role, text FROM messages WHERE session_id = ? ORDER BY id", (session_id,))
    history = [{"role": r, "text": t} for r, t in cur.fetchall()]

    conn.close()

    return ChatResponse(session_id=session_id, history=history)


# 🧾 Get all previous sessions
@app.get("/sessions", response_model=List[Session])
async def get_sessions():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT session_id, created_at FROM sessions ORDER BY created_at DESC")
        sessions = [{"session_id": s, "created_at": c} for s, c in cur.fetchall()]
        return sessions
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)