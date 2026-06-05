import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def get_recipe(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    data = response.json()
    return data["response"]