from pathlib import Path

from services.chunker import create_chunks
from services.embeddings import get_embedding
from services.vector_store import add_chunks

from services.document_processor import extract_document
from services.url_processor import extract_url


def index_pages(
    pages,
    source_name
):

    chunks = create_chunks(
        pages,
        source_name
    )

    if not chunks:
        raise ValueError(
            "No readable text found."
        )

    embeddings = []

    for chunk in chunks:

        embeddings.append(
            get_embedding(
                chunk["text"]
            )
        )

    add_chunks(
        chunks,
        embeddings
    )

    return len(chunks)


def index_document(file_path):

    filename = Path(file_path).name

    pages = extract_document(
        file_path
    )

    return index_pages(
        pages,
        filename
    )


def index_url(url):

    pages = extract_url(
        url
    )

    return index_pages(
        pages,
        url
    )