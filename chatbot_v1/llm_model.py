from schemas import ChatRequest
from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os


llm = ChatGroq(model="llama-3.1-8b-instant",
               groq_api_key=os.getenv("GROQ_API_KEY"))

def get_response(state: ChatRequest):

    # USE QUERY
    message = state.message

    # promtp
    prompt = f"Give the user response based on the user query: {message}"

    # llm response
    response_text = llm.invoke(prompt).content

    # update the llm respone in chatRequest model
    state.response = response_text

    return state

# if __name__=="__main__":
#     query = ChatRequest(message="what is the capital of india?")
#     response = get_response(state=query)
#     for msg in response:
#         print(msg)
    # print(response)

# ========== add momory ===============