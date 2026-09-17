from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(
  model='granite4.2:8b',
  messages=[
    {
      'role': 'user',
      'content': 'Why is the sky blue?',
    },
  ],
)
print(response['message']['content'])