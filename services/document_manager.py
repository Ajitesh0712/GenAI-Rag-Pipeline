from collections import defaultdict
from services.vector_store import collection


def list_documents():

    data = collection.get()

    documents = defaultdict(int)

    metadatas = data.get("metadatas", [])

    for metadata in metadatas:

        filename = metadata.get("filename")

        if filename:
            documents[filename] += 1

    result = []

    for filename, chunks in documents.items():

        result.append({
            "filename": filename,
            "chunks": chunks
        })

    return sorted(result, key=lambda x: x["filename"])


def delete_document(filename):

    data = collection.get()

    ids_to_delete = []

    for doc_id, metadata in zip(
        data["ids"],
        data["metadatas"]
    ):

        if metadata["filename"] == filename:
            ids_to_delete.append(doc_id)

    if ids_to_delete:
        collection.delete(ids=ids_to_delete)

    return len(ids_to_delete)