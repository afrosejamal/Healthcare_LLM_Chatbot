import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"  # good balance of speed + quality on Groq

def get_chat_response(messages: list, temperature: float = 0.4, max_tokens: int = 700) -> str:
    """
    messages: list of dicts like [{"role": "system"/"user"/"assistant", "content": "..."}]
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Sorry, I had trouble processing that. (Error: {str(e)})"