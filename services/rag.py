from services.embeddings import get_embedding
from services.vector_store import search
from services.ollama_client import (
    generate_response,
    generate_response_stream
)
import json

from services.memory import (
    add_message,
    get_history
)

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

def build_prompt(
    question,
    context,
    history
):

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

Conversation History:
{history}

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

    history = build_history()

    rewritten_question = rewrite_question(
        question,
        history
    )

    print("\nOriginal:", question)
    print("Rewritten:", rewritten_question)

    results = retrieve_context(
        rewritten_question
    )

    context = build_context(
        results
    )
   
    prompt = build_prompt(
        question,
        context,
        history
    )

    answer = generate_response(
        prompt
    )
    add_message(
        "user",
        question
    )
    add_message(
        "assistant",
        answer
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


def ask_rag_stream(question):

    history = build_history()

    rewritten_question = rewrite_question(
        question,
        history
    )

    results = retrieve_context(
        rewritten_question
    )

    context = build_context(
        results
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
    prompt = build_prompt(
        question,
        context,
        history
    )

    def stream():

        full_answer = ""

        for token in generate_response_stream(prompt):

            full_answer += token

            yield json.dumps({
                "type": "token",
                "content": token
            }) + "\n"

        add_message(
            "user",
            question
        )

        add_message(
            "assistant",
            full_answer
        )
        yield json.dumps({

            "type": "sources",

            "content": sources

        }) + "\n"

        yield json.dumps({

            "type": "done"

        }) + "\n"

    return stream()

def build_history():

    history = get_history()

    if not history:
        return ""

    conversation = []

    for message in history:

        role = (
            "User"
            if message["role"] == "user"
            else "Assistant"
        )

        conversation.append(
            f"{role}: {message['content']}"
        )

    return "\n".join(conversation)



def rewrite_question(
    question,
    history
):

    if not history.strip():

        return question

    rewrite_prompt = f"""
You are a query rewriting assistant.

Given the conversation history and the latest user question,
rewrite the latest question so it is completely self-contained.

Rules:

- Only rewrite the user's latest question.
- Do not answer it.
- Keep the meaning identical.
- If the question is already standalone, return it unchanged.

Conversation:

{history}

Latest Question:

{question}

Standalone Question:
"""

    rewritten = generate_response(
        rewrite_prompt
    )

    return rewritten.strip()