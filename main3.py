from ollama import generate

response = generate(model='granite4.2:8b', prompt='Why is the sky blue?')
print(response['response'])