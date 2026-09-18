import os

from dotenv import load_dotenv
from ollama import generate

load_dotenv()
MODEL = os.environ.get("OLLAMA_MODEL", "granite4.2:8b")

response = generate(model=MODEL, prompt="Why is the sky blue?")
print(response["response"])
