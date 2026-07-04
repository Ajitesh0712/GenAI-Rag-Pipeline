import json
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


def generate_response_stream(prompt: str):

    response = requests.post(

        OLLAMA_URL,

        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": True
        },

        stream=True

    )

    response.raise_for_status()

    for line in response.iter_lines():

        if not line:
            continue

        data = json.loads(line)

        if "response" in data:

            yield data["response"]

        if data.get("done"):

            break