import sqlite3
from pathlib import Path

DB_PATH = Path("chat_history.db")


def get_connection():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS chat_sessions(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP

        )

    """)

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS messages(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            session_id INTEGER NOT NULL,

            role TEXT NOT NULL,

            content TEXT NOT NULL,

            created_at TIMESTAMP
            DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(session_id)
            REFERENCES chat_sessions(id)

        )

    """)

    conn.commit()

    conn.close()

def create_chat(title="New Chat"):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO chat_sessions(title)
        VALUES(?)
        """,
        (title,)
    )

    conn.commit()

    chat_id = cursor.lastrowid

    conn.close()

    return chat_id


def save_message(
    session_id,
    role,
    content
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages(

            session_id,

            role,

            content

        )

        VALUES(

            ?, ?, ?

        )
        """,

        (
            session_id,
            role,
            content
        )

    )

    conn.commit()

    conn.close()


def get_chat_history(session_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content

        FROM messages

        WHERE session_id = ?

        ORDER BY id ASC
        """,
        (session_id,)
    )

    rows = cursor.fetchall()

    conn.close()

    history = []

    for row in rows:

        history.append({

            "role": row["role"],

            "content": row["content"]

        })

    return history


def list_chats():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title, created_at

        FROM chat_sessions

        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    chats = []

    for row in rows:

        chats.append({

            "id": row["id"],

            "title": row["title"],

            "created_at": row["created_at"]

        })

    return chats

def build_history(session_id):

    history = get_chat_history(session_id)

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

def update_chat_title(
    session_id,
    title
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        UPDATE chat_sessions
        SET title = ?
        WHERE id = ?
        """,

        (
            title,
            session_id
        )

    )

    conn.commit()

    conn.close()

def delete_chat(session_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM messages
        WHERE session_id = ?
        """,
        (session_id,)
    )

    cursor.execute(
        """
        DELETE FROM chat_sessions
        WHERE id = ?
        """,
        (session_id,)
    )

    conn.commit()

    conn.close()