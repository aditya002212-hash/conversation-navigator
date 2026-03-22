# Conversation Navigator

A beginner-friendly Streamlit MVP for exploring chat conversations.

## Features

- Loads chat messages from `data/sample_chat.json`
- Supports uploaded `.json` conversation files
- Extracts only user messages
- Groups user questions by topic in the sidebar
- Shows conversation sections with rule-based summaries
- Uses a sectioned sidebar instead of a flat question list
- Displays the full conversation in the main area
- Adds simple search for user questions
- Organizes helper code inside `utils/`

## Project Files

- `app.py` - Streamlit application
- `utils/extractor.py` - Helpers for loading data and filtering user messages
- `utils/tags.py` - Helpers for assigning topic tags
- `utils/sections.py` - Helpers for building sections, summaries, and grouped questions
- `data/sample_chat.json` - Sample conversation data
- `requirements.txt` - Python dependency list

## Run Locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the app:

   ```bash
   streamlit run app.py
   ```

3. Open the local URL shown in your terminal.

## Sample Data Format

Each message in `data/sample_chat.json` uses this structure:

```json
{
  "role": "user",
  "content": "What should I visit first?"
}
```
