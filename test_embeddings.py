from services.embeddings import get_embedding

vector = get_embedding(
    "Machine Learning"
)

print(type(vector))
print(len(vector))
print(vector[:10])