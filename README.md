# Text Summarizer

A simple Python app that summarizes text using a lightweight sentence-ranking algorithm and a Streamlit web interface.

## Features

- Paste text or notes into the app
- Adjust summary length with a slider
- Get a concise extractive summary instantly

## Setup

1. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Files

- `app.py` — Streamlit application
- `requirements.txt` — Python dependencies
- `README.md` — Project instructions

## Notes

This summarizer is intentionally lightweight and does not require external AI APIs or large model downloads. It works best for short to medium-length text.
