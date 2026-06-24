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

def build_context(
    results
):

    documents = results["documents"][0]

    context = "\n\n".join(
        documents
    )

    return context

def build_prompt(question, context):

    return f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

Keep answers concise and well formatted.

Do not copy large portions of the context.

Summarize information naturally.

If the answer is not present in the context,
say "I could not find that information."

Context:
{context}

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

    return answer