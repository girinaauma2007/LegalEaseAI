# LegalEase — AI-Powered Legal Document Generator

LegalEase implements the requested Streamlit → FastAPI → Gemini architecture and supports editable previews plus TXT, DOCX and PDF export.

## Project tree

```text
LegalEase/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── Procfile
├── Dockerfile
├── docker-compose.yml
├── backend/ (main.py, routes.py, schemas.py, config.py)
├── ai_core/ (gemini_generator.py)
├── formatters/ (common.py, text_formatter.py, docx_formatter.py, pdf_formatter.py)
├── assets/logo.svg
├── tests/ (test_api.py, test_formatters.py)
└── .streamlit/config.toml
```

## Windows VS Code setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and set `GEMINI_API_KEY`.

## Run backend

```powershell
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Check `http://127.0.0.1:8000/health` and API docs at `http://127.0.0.1:8000/docs`.

## Run frontend

In a second terminal:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

Open the Streamlit URL, normally `http://localhost:8501`.

## Test

```powershell
pytest -q
```

The automated generation test mocks Gemini, so a live API key is not required for tests.

## API example

POST `/generate`:

```json
{
  "document_type": "Freelance Work Contract",
  "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
  "terms": ["Payment within 30 days", "Maintain confidentiality"],
  "effective_date": "September 26, 2026",
  "language": "English",
  "additional_instructions": "Include signature blocks."
}
```

## Model compatibility

The original documentation selected `gemini-1.5-pro`. This project does not hard-code that retired model; it reads `GEMINI_MODEL` from `.env`. The default is `gemini-3.8-flash`. Use a currently supported model available to your Google AI account.

## Legal/safety note

Generated content is a draft, not legal advice. The prompt instructs the model not to invent missing facts and to use placeholders where information is missing. Users should have documents reviewed for the relevant jurisdiction and transaction before signing or relying on them.
