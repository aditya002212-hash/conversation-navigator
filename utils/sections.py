from utils.tags import infer_topic_tags


def build_question_groups(user_messages: list[dict]) -> dict[str, list[dict]]:
    """Group user questions by their first inferred topic tag."""
    grouped_questions: dict[str, list[dict]] = {}

    for index, message in enumerate(user_messages, start=1):
        content = message.get("content", "")
        topic = infer_topic_tags(content)[0]
        grouped_questions.setdefault(topic, []).append(
            {"index": index, "content": content, "tags": infer_topic_tags(content)}
        )

    return dict(sorted(grouped_questions.items(), key=lambda item: item[0]))


def summarize_section(messages: list[dict], topic: str) -> str:
    """Create a simple rule-based summary from the messages in a section."""
    user_messages = [message.get("content", "").strip() for message in messages if message.get("role") == "user"]
    assistant_messages = [message.get("content", "").strip() for message in messages if message.get("role") == "assistant"]

    summary_parts = [f"This section focuses on {topic.lower()}."]

    if user_messages:
        summary_parts.append(f"The user asks {truncate_text(user_messages[0], 100)}")

    if len(user_messages) > 1:
        summary_parts.append(f"There are {len(user_messages)} user questions in this section.")

    if assistant_messages:
        summary_parts.append(f"The assistant responds with {truncate_text(assistant_messages[0], 100)}")

    return " ".join(summary_parts)


def build_sections(messages: list[dict]) -> list[dict]:
    """Split the conversation into sections whenever the dominant user topic changes."""
    sections: list[dict] = []
    current_section: dict | None = None
    user_message_number = 0

    for message in messages:
        role = message.get("role")
        content = message.get("content", "")
        tags = infer_topic_tags(content) if role == "user" else []
        topic = tags[0] if tags else (current_section["topic"] if current_section else "General")

        if role == "user":
            user_message_number += 1

        section_starts_new = current_section is None or (role == "user" and topic != current_section["topic"])

        if section_starts_new:
            if current_section is not None:
                current_section["summary"] = summarize_section(current_section["messages"], current_section["topic"])
                sections.append(current_section)

            current_section = {
                "id": len(sections) + 1,
                "topic": topic,
                "messages": [],
                "user_question_numbers": [],
                "summary": "",
            }

        current_section["messages"].append(message)

        if role == "user":
            current_section["user_question_numbers"].append(user_message_number)

    if current_section is not None:
        current_section["summary"] = summarize_section(current_section["messages"], current_section["topic"])
        sections.append(current_section)

    return sections


def truncate_text(text: str, max_length: int) -> str:
    """Shorten text for compact labels and summaries."""
    if len(text) <= max_length:
        return text
    return f"{text[: max_length - 3].rstrip()}..."
