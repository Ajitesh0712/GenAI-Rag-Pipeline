from services.document_processor import (
    extract_document
)

from services.chunker import (
    create_chunks
)

from services.embeddings import (
    get_embedding
)

from services.vector_store import (
    add_chunks
)

pages = extract_document(
    "uploads/My journey into AI.pdf"
)

chunks = create_chunks(
    pages,
    "My journey into AI.pdf"
)

embeddings = []

for chunk in chunks:

    vector = get_embedding(
        chunk["text"]
    )

    embeddings.append(
        vector
    )

add_chunks(
    chunks,
    embeddings
)

print(
    f"Indexed {len(chunks)} chunks"
)