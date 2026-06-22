from services.document_processor import extract_document
from services.chunker import create_chunks

pages = extract_document(
    "uploads/My journey into AI.pdf"
)

chunks = create_chunks(
    pages,
    "My journey into AI.pdf"
)

print(f"Chunks: {len(chunks)}")

for chunk in chunks[:3]:

    print("\n---")

    print(chunk["id"])

    print(chunk["page"])

    print(chunk["text"][:300])