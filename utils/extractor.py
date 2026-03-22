import json
from pathlib import Path
from typing import BinaryIO


def normalize_text(text: str) -> str:
    """Lowercase and trim text so simple search matching is easier."""
    return text.strip().lower()


def normalize_messages(raw_messages: object) -> list[dict]:
    """Validate message data and coerce it into the expected list-of-dicts format."""
    if not isinstance(raw_messages, list):
        raise ValueError("Conversation data must be a JSON array of messages.")

    normalized_messages = []

    for index, message in enumerate(raw_messages, start=1):
        if not isinstance(message, dict):
            raise ValueError(f"Message #{index} must be a JSON object.")

        role = str(message.get("role", "unknown")).strip().lower() or "unknown"
        content = str(message.get("content", "")).strip()

        normalized_messages.append({"role": role, "content": content})

    return normalized_messages


def load_messages(file_path: Path) -> list[dict]:
    """Read the JSON file and return the full list of chat messages."""
    with file_path.open("r", encoding="utf-8") as file:
        return normalize_messages(json.load(file))


def load_uploaded_messages(uploaded_file: BinaryIO) -> list[dict]:
    """Read uploaded JSON conversation data and return normalized messages."""
    return normalize_messages(json.load(uploaded_file))


def get_user_messages(messages: list[dict]) -> list[dict]:
    """Keep only the messages where the role is 'user'."""
    return [message for message in messages if message.get("role") == "user"]
