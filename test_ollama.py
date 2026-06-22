import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "gpt-oss:latest",
        "prompt": "What is AI?",
        "stream": False
    }
)

print(response.json()["response"])