from collections import deque

MAX_HISTORY = 10

conversation = deque(maxlen=MAX_HISTORY)


def add_message(role: str, content: str):

    conversation.append(
        {
            "role": role,
            "content": content
        }
    )


def get_history():

    return list(conversation)


def clear_history():

    conversation.clear()