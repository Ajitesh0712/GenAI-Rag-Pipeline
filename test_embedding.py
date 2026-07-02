from services.embeddings import get_embedding

embedding = get_embedding("Hello World")

print(type(embedding))
print(len(embedding))