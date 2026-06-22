from services.document_processor import (
    extract_document
)

result = extract_document(
    "uploads/My journey into AI.pdf"
)

for page in result:

    print(
        f"Page {page['page']}"
    )

    print(
        page["text"][:300]
    )

    print("-" * 50)