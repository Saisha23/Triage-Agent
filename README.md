# Triage Agent

An AI-assisted email triage service built with FastAPI, LangGraph, LangChain, Groq, and SQLAlchemy. Each email is classified into a known category, assigned a priority and confidence score, validated with deterministic rules, and routed either to automatic processing or human review.

## What it does

- Classifies email as `Complaint`, `Feedback`, `Request`, `Spam`, or `Other`.
- Assigns `Low`, `Medium`, `High`, or `Critical` priority.
- Routes low-confidence, high-priority, critical, or model-flagged messages to human review.
- Stores emails and triage results through SQLAlchemy.
- Exposes endpoints for triage, stored emails, the review queue, and review decisions.
- Includes notebooks for configuration, graph exploration, and Groq experiments.

## Requirements

- Python 3.11 or newer
- A Groq API key
- A SQLAlchemy-compatible database URL (SQLite is suitable for local development)

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a local `.env` file in the project root. Use your own values; never place real credentials in this README, source files, notebooks, or commits:

```dotenv
GROQ_API_KEY=<your-groq-api-key>
GROQ_MODEL=<your-groq-model>
DATABASE_URL=sqlite:///./triage.db
```

The repository ignores `.env` files. If a credential is ever committed or exposed, revoke it with the provider and create a replacement.

## Initialize the database

With the virtual environment active and `.env` configured:

```powershell
python create_tables.py
```

For a PostgreSQL database, replace `DATABASE_URL` with the appropriate SQLAlchemy URL and ensure the database is available before running the command.

## Run the API

Start the development server from the project root:

```powershell
uvicorn app.main:app --reload
```

The interactive API documentation is available at <http://127.0.0.1:8000/docs>.

### Endpoints

`POST /triage` classifies an email:

```json
{
   "subject": "Unable to access my account",
   "email": "I have been locked out since this morning."
}
```

Other endpoints:

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Health message |
| `POST` | `/triage` | Classify an email |
| `GET` | `/emails` | List stored emails and triage results |
| `GET` | `/review-queue` | List pending human reviews |
| `POST` | `/review` | Approve or reject a review item |

The current API triage route returns the classification result. Persistence utilities and database inspection scripts are also included for local workflow testing.

## Notebooks and scripts

- `app/graph.ipynb`: Notebook version of the triage graph.
- `app/config.ipynb`: Checks required environment configuration.
- `01_test_groq.ipynb`: Local Groq connectivity experiment.
- `check_database.py`: Persists a sample triage result for testing.
- `test_persistence.py`: Example persistence call.
- `create_tables.py`: Creates and updates the database tables.

## Project structure

```text
app/
   database.py       Database engine and sessions
   graph.py          LangGraph classification and validation workflow
   main.py           FastAPI application and endpoints
   models.py         SQLAlchemy email and triage models
   persistence.py    Persistence helper
   state.py          Pydantic result schemas and graph state
```

## Security checklist

- Keep `.env` local and out of version control.
- Use placeholders when documenting configuration.
- Do not print `GROQ_API_KEY`, database credentials, or tokens in logs.
- Rotate any credential that may have been exposed.
- Add authentication and authorization before exposing the API beyond a trusted local environment.