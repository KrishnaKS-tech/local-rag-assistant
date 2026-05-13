import os
import json
import uuid
from datetime import datetime

CHAT_DIR = "data/chats"


def ensure_chat_directory():
    os.makedirs(CHAT_DIR, exist_ok=True)


def create_new_session(content):
    ensure_chat_directory()

    session_id = str(uuid.uuid4())

    session_data = {
        "session_id": session_id,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "content": content,
        "messages": []
    }

    save_session(session_data)

    return session_data


def save_session(session_data):
    file_path = os.path.join(
        CHAT_DIR,
        f"{session_data['session_id']}.json"
    )

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(session_data, file, indent=4)


def load_session(session_id):
    file_path = os.path.join(
        CHAT_DIR,
        f"{session_id}.json"
    )

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_sessions():
    ensure_chat_directory()

    sessions = []

    for file_name in os.listdir(CHAT_DIR):

        if file_name.endswith(".json"):

            file_path = os.path.join(CHAT_DIR, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                session_data = json.load(file)

                sessions.append(session_data)

    sessions.sort(
        key=lambda x: x["created_at"],
        reverse=True
    )

    return sessions