# Conversation Navigator

A simple Streamlit prototype that helps users navigate long AI conversations.

## Problem
In long chat conversations, it becomes difficult to scroll back and find a specific user question.

## Solution
This app extracts user questions and displays them in a clickable sidebar, allowing quick navigation to earlier parts of the conversation.

## Features
- Loads chat messages from JSON
- Extracts user questions
- Sidebar navigation
- Search in questions
- Clean conversation display

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
