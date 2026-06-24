import requests
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gpt-oss:latest"
def generate_response(prompt: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"]