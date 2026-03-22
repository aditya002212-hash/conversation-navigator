# Context-Aware Conversation Navigator

A Streamlit-based system that improves navigation in long AI conversations by introducing structured sections, topic grouping, and question-based navigation.

---

## 🚨 Problem

Long AI conversations (like ChatGPT chats) become difficult to navigate:
- Users must scroll extensively
- Context is hard to revisit
- No structured overview of discussion

---

## 💡 Solution

This project introduces a structured navigation system:
- Extracts user questions
- Groups them by topic
- Splits conversation into sections
- Generates section summaries
- Enables jump navigation

---

## ⚙️ Features

- 📂 Upload your own chat JSON
- 🧠 Topic-based grouping (DSA, ML, Career, etc.)
- 📌 Sidebar navigation for user questions
- 🧭 Section-based conversation structuring
- 📝 Rule-based section summaries
- 🔍 Search functionality
- 🎯 Highlight selected message

---

## 🧠 Why This Matters

This project explores how AI interfaces can evolve from:
> Linear chat → Structured knowledge systems

Potential applications:
- AI learning assistants
- Developer productivity tools
- Research workflows
- Long-form AI collaboration

---

## 🛠 Tech Stack

- Python
- Streamlit
- Modular architecture (utils/)

---

## 🚀 Future Improvements

- LLM-based summarization
- Semantic topic clustering
- ChatGPT plugin integration
- Real-time conversation indexing

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
