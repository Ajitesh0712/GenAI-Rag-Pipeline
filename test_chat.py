from services.chat_db import (

    initialize_database,

    create_chat,

    list_chats

)

initialize_database()

create_chat("HardwareAI")

create_chat("Resume Review")

print(list_chats())