# Triage Agent

An email triage workflow built with LangGraph, LangChain, and Groq. It classifies an email, validates the result deterministically, and routes high-risk or uncertain messages to human review.

## Features

- Structured classification into complaint, feedback, request, spam, or other
- Priority scoring from low to critical
- Confidence and human-review validation rules
- Automatic processing or human-review routing
- Notebook examples for graph visualization and sample emails

## Setup

1. Create and activate a Python 3.11 virtual environment.
2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a local `.env` file that is never committed:

   ```text
   GROQ_API_KEY=your_groq_api_key
   GROQ_MODEL=qwen/qwen3.8-27b
   ```

4. Open `app/graph.ipynb` from the project root and run the cells.

## Security

This project is a local notebook workflow; it does not start a web server or expose an HTTP API. The Groq key is read from `.env` and is not included in the repository. Keep the GitHub repository private unless you intentionally add an authenticated deployment boundary, and never print or commit API keys.

If a key has ever been exposed, revoke it in the Groq console and create a replacement before using this project.

## Project Layout

- `app/graph.ipynb`: LangGraph workflow and examples
- `app/state.py`: Typed state and structured triage result schema
- `app/config.ipynb`: Environment configuration checks
- `01_test_groq.ipynb`: Local Groq connectivity experiments
- `requirements.txt`: Python dependencies