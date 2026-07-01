from services.document_manager import (
    list_documents,
    delete_document
)

print("Before:")
print(list_documents())

deleted = delete_document(
    "My journey into AI.pdf"
)

print(f"\nDeleted {deleted} chunks\n")

print("After:")
print(list_documents())