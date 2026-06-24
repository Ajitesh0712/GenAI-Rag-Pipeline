from services.rag import ask_rag

question = (
    "Tell me about the recommendation system project"
)

answer = ask_rag(
    question
)

print(answer)