from pathlib import Path

from services.document_processor import extract_document
from services.chunker import create_chunks
from services.embeddings import get_embedding
from services.vector_store import add_chunks


def index_document(file_path):

    filename = Path(file_path).name

    pages = extract_document(file_path)

    chunks = create_chunks(
        pages,
        filename
    )

    embeddings = []

    for chunk in chunks:
        vector = get_embedding(
            chunk["text"]
        )

        embeddings.append(vector)

    add_chunks(
        chunks,
        embeddings
    )

    return len(chunks)