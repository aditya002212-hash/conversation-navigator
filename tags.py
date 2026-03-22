from utils.extractor import normalize_text


def infer_topic_tags(text: str) -> list[str]:
    """Assign simple topic tags by checking whether certain keywords appear."""
    # This dictionary maps each tag name to a few words that usually belong to that topic.
    keyword_map = {
        "DSA": ["dsa", "data structures", "algorithms", "leetcode", "array", "tree", "graph"],
        "ML": ["ml", "machine learning", "model", "neural", "training", "regression"],
        "Career": ["career", "job", "resume", "interview", "internship", "hiring"],
    }

    normalized_text = normalize_text(text)
    tags = []

    # If any keyword appears in the message, add the matching topic tag.
    for tag, keywords in keyword_map.items():
        if any(keyword in normalized_text for keyword in keywords):
            tags.append(tag)

    # Use a default tag so every user message shows at least one label.
    if not tags:
        tags.append("General")

    return tags
