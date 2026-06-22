from typing import List, Dict
def create_chunks(
    pages: List[Dict],
    filename: str,
    chunk_size: int = 1000,
    overlap: int = 200
):
    chunks = []

    chunk_index = 0

    for page_data in pages:

        page_number = page_data["page"]
        text = page_data["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append(
                {
                    "id": f"{filename}_{page_number}_{chunk_index}",
                    "text": chunk_text,
                    "filename": filename,
                    "page": page_number,
                    "chunk_index": chunk_index
                }
            )

            chunk_index += 1

            start += chunk_size - overlap

    return chunks