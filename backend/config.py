from dotenv import load_dotenv
load_dotenv()
import os

class Config:
    DATABASE_URL = "sqlite:///./test.db"
    SECRET_KEY = "your_secret_key"
    LOCAL_DB_PATH = "backend/database/chat_sessions.db"
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL_NAME = "llama-3.1-8b-instant"