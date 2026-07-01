from services.embeddings import get_embedding
from services.vector_store import search
from services.ollama_client import generate_response

def retrieve_context(
    question,
    top_k=3
):

    query_embedding = get_embedding(
        question
    )

    results = search(
        query_embedding,
        top_k
    )

    return results

def build_context(results):

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = []

    for doc, meta in zip(documents, metadatas):

        context.append(
            f"""
Document: {meta['filename']}
Page: {meta['page']}
Chunk: {meta['chunk_index']}

{doc}
"""
        )

    return "\n\n------------------------\n\n".join(context)

def build_prompt(question, context):

    return f"""
You are a professional AI assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context,
reply:

"I could not find that information in the provided documents."

Formatting Rules:

- Respond in Markdown.
- Use a main heading (#) for the topic.
- Use section headings (##) where appropriate.
- Use bullet points for lists.
- Use **bold** for important terms.
- Keep paragraphs short (2-4 lines).
- Leave one blank line between sections.
- Do NOT write everything in one paragraph.
- Do NOT mention the context or that you were given context.
- Summarize naturally instead of copying large blocks.

Example Format:

# Topic Name

## Overview

Short explanation.

## Key Features

- Feature 1
- Feature 2
- Feature 3

## Technologies

- Python
- Flask
- ChromaDB

## Summary

One short concluding paragraph.

-------------------------

Context:
{context}

-------------------------

Question:
{question}

Answer:
"""

def ask_rag(
    question
):

    results = retrieve_context(
        question
    )

    context = build_context(
        results
    )

    prompt = build_prompt(
        question,
        context
    )

    answer = generate_response(
        prompt
    )

    sources = []
    seen = set()

    for metadata in results["metadatas"][0]:

        key = (
            metadata["filename"],
            metadata["page"]
        )

        if key not in seen:

            seen.add(key)

            sources.append({
                "filename": metadata["filename"],
                "page": metadata["page"]
            })

    return {
        "answer": answer,
        "sources": sources
    }

