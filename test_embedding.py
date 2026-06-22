# test_embedding.py

import requests

response = requests.post(
    "http://localhost:11434/api/embeddings",
    json={
        "model": "nomic-embed-text",
        "prompt": "What is artificial intelligence?"
    }
)

data = response.json()

print("Vector length:", len(data["embedding"]))
print("First 10 values:", data["embedding"][:10])