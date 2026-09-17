import os
from dotenv import load_dotenv
from ollama import chat
from ollama import ChatResponse

load_dotenv()
MODEL = os.environ.get("OLLAMA_MODEL", "granite4.2:8b")

response: ChatResponse = chat(
  model=MODEL,
  messages=[
    {
      'role': 'user',
      'content': 'Why is the sky blue?',
    },
  ],
)
print(response['message']['content'])