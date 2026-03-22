import json
from html import escape
from pathlib import Path

import streamlit as st

from utils.extractor import get_user_messages, load_messages, load_uploaded_messages, normalize_text
from utils.sections import build_question_groups, build_sections, truncate_text
from utils.tags import infer_topic_tags


# Store the sample data inside a dedicated folder to keep the project organized.
DATA_FILE = Path("data/sample_chat.json")


def inject_styles() -> None:
    """Add lightweight custom styles for spacing and message cards."""
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #f8fafc 0%, #eef4ff 100%);
                border-right: 1px solid #dbeafe;
            }

            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1100px;
            }

            .section-card,
            .message-card {
                background: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
                padding: 1rem 1.1rem;
                margin-bottom: 1rem;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
            }

            .message-card.selected {
                border: 2px solid #2563eb;
                box-shadow: 0 12px 30px rgba(37, 99, 235, 0.15);
                background: #f8fbff;
            }

            .message-role {
                font-size: 0.85rem;
                font-weight: 700;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                color: #475569;
                margin-bottom: 0.65rem;
            }

            .message-content {
                line-height: 1.65;
                color: #0f172a;
            }

            .section-card {
                margin-bottom: 1.25rem;
                background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
            }

            .section-heading {
                font-size: 1.05rem;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 0.4rem;
            }

            .section-summary {
                color: #334155;
                line-height: 1.65;
                margin-bottom: 0.8rem;
            }

            .tag-row {
                margin-top: 0.85rem;
            }

            .topic-tag {
                display: inline-block;
                font-size: 0.75rem;
                font-weight: 600;
                padding: 0.3rem 0.6rem;
                margin-right: 0.45rem;
                border-radius: 999px;
                background: #e0ecff;
                color: #1d4ed8;
            }

            .sidebar-caption {
                color: #64748b;
                font-size: 0.9rem;
                margin-bottom: 0.75rem;
            }

            .section-meta {
                color: #64748b;
                font-size: 0.85rem;
                margin-bottom: 0.8rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    # This sets the browser tab title and tells Streamlit to use more horizontal space.
    st.set_page_config(page_title="Conversation Navigator", layout="wide")
    inject_styles()

    st.title("Conversation Navigator")
    st.caption("Upload a conversation, skim section summaries, and jump to grouped user questions.")

    uploaded_file = st.sidebar.file_uploader("Upload conversation JSON", type=["json"])

    try:
        messages = load_uploaded_messages(uploaded_file) if uploaded_file else load_messages(DATA_FILE)
    except ValueError as error:
        st.sidebar.error(str(error))
        messages = load_messages(DATA_FILE)
    except Exception:
        st.sidebar.error("The uploaded file could not be read as conversation JSON.")
        messages = load_messages(DATA_FILE)

    user_messages = get_user_messages(messages)
    sections = build_sections(messages)
    question_groups = build_question_groups(user_messages)

    st.sidebar.header("Explore Conversation")
    st.sidebar.caption("Questions are grouped by topic, and each section includes a short summary.")
    search_query = st.sidebar.text_input("Search user questions")

    matching_user_messages = []
    normalized_query = normalize_text(search_query)

    for topic, questions in question_groups.items():
        filtered_questions = [
            question
            for question in questions
            if not normalized_query or normalized_query in normalize_text(question["content"])
        ]
        if filtered_questions:
            matching_user_messages.append((topic, filtered_questions))

    # session_state helps us remember which message the user selected after each rerun.
    if "selected_user_message" not in st.session_state:
        st.session_state.selected_user_message = 1 if user_messages else None
    elif user_messages:
        st.session_state.selected_user_message = min(st.session_state.selected_user_message or 1, len(user_messages))
    else:
        st.session_state.selected_user_message = None

    st.sidebar.subheader("Sections")
    for section in sections:
        question_count = len(section["user_question_numbers"])
        label = f"Section {section['id']}: {section['topic']}"
        with st.sidebar.expander(label, expanded=section["id"] == 1):
            st.caption(f"{question_count} user question{'s' if question_count != 1 else ''}")
            st.write(section["summary"])
            if section["user_question_numbers"]:
                first_question = section["user_question_numbers"][0]
                st.markdown(f"[Jump to first question](#user-message-{first_question})")

    st.sidebar.subheader("Questions By Topic")
    if matching_user_messages:
        st.sidebar.markdown(
            "<div class='sidebar-caption'>Choose a topic, highlight a question, or use the jump link to move through the conversation.</div>",
            unsafe_allow_html=True,
        )
        for topic, questions in matching_user_messages:
            with st.sidebar.expander(f"{topic} ({len(questions)})", expanded=True):
                for question in questions:
                    index = question["index"]
                    preview = truncate_text(question["content"], 60)
                    button_label = f"#{index} {preview}"
                    if st.button(button_label, key=f"sidebar-message-{topic}-{index}", use_container_width=True):
                        st.session_state.selected_user_message = index
                    st.markdown(f"[Jump to message #{index}](#user-message-{index})")
                    st.caption(" | ".join(question["tags"]))
    else:
        st.sidebar.info("No user questions matched your search.")

    if user_messages:
        export_data = {"questions": user_messages, "sections": sections}
        st.sidebar.subheader("Export")
        if st.sidebar.button("Prepare Navigation Export", use_container_width=True):
            st.sidebar.success("Navigation data is ready to download.")
        st.sidebar.download_button(
            label="Download JSON",
            data=json.dumps(export_data, indent=2),
            file_name="conversation_navigation.json",
            mime="application/json",
            use_container_width=True,
        )

    st.subheader("Conversation Overview")

    for section in sections:
        question_count = len(section["user_question_numbers"])
        st.markdown(
            f"""
            <div class="section-card">
                <div class="section-heading">Section {section['id']} - {escape(section['topic'])}</div>
                <div class="section-meta">{question_count} user question{'s' if question_count != 1 else ''}</div>
                <div class="section-summary">{escape(section['summary'])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Full Conversation")

    user_message_number = 0

    for message in messages:
        # Each message card shows the speaker, the message text, and topic tags for user messages.
        role = message.get("role", "unknown").capitalize()
        content = message.get("content", "")
        is_selected_user_message = False
        tags = []

        if message.get("role") == "user":
            user_message_number += 1
            tags = infer_topic_tags(content)
            is_selected_user_message = user_message_number == st.session_state.selected_user_message
            st.markdown(f"<div id='user-message-{user_message_number}'></div>", unsafe_allow_html=True)

        selected_class = " selected" if is_selected_user_message else ""
        tag_html = "".join(f"<span class='topic-tag'>{tag}</span>" for tag in tags)
        escaped_content = escape(content).replace("\n", "<br>")
        tag_section = f'<div class="tag-row">{tag_html}</div>' if tags else ""

        st.markdown(
            f"""
            <div class="message-card{selected_class}">
                <div class="message-role">{role}</div>
                <div class="message-content">{escaped_content}</div>
                {tag_section}
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
