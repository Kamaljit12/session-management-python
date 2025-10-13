from groq import Groq
from backend.config import Config

# Initialize the Groq API client using your API key
client = Groq(api_key=Config.GROQ_API_KEY)

def get_response(query: str) -> str:
    """
    Send a query to the Groq LLM model and return the AI-generated response.

    Args:
        query (str): The user's question or message.
    Returns:
        str: The model's text response.
    """
    try:
        # Create a simple but context-aware prompt
        prompt = f"Answer the following user query clearly and concisely:\n\n{query}"

        # Send request to Groq model
        response = client.chat.completions.create(
            model=Config.GROQ_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract and return response text
        return response.choices[0].message.content.strip()

    except Exception as e:
        # Handle unexpected API errors or connectivity issues
        return f"⚠️ Error while processing query: {str(e)}"
