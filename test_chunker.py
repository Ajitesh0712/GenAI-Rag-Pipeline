from services.ollama_client import generate_response_stream

for token in generate_response_stream(

    "Explain RAG in 50 words."

):
    print(token, end="", flush=True)