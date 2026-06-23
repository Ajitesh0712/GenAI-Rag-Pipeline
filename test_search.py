from services.embeddings import (
    get_embedding
)

from services.vector_store import (
    search
)

query = (
    "Tell me about your recommendation system"
)

query_embedding = get_embedding(
    query
)

results = search(
    query_embedding
)

print(results["documents"][0])