import os

from dotenv import load_dotenv
from ollama import chat

load_dotenv()
MODEL = os.environ.get("OLLAMA_MODEL", "granite4.2:8b")

stream = chat(
    model=MODEL,
    messages=[{"role": "user", "content": "Why is the sky blue?"}],
    stream=True,
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
