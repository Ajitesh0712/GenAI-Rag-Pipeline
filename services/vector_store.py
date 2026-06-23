import chromadb
from chromadb.config import Settings



client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)

def add_chunks(
    chunks,
    embeddings
):

    ids = []

    documents = []

    metadatas = []

    for chunk in chunks:

        ids.append(
            chunk["id"]
        )

        documents.append(
            chunk["text"]
        )

        metadatas.append(
            {
                "filename":
                    chunk["filename"],

                "page":
                    chunk["page"],

                "chunk_index":
                    chunk["chunk_index"]
            }
        )

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


def search(
    query_embedding,
    top_k=3
):

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )

    return results