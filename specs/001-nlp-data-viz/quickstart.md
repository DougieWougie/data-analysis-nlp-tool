# Quickstart: Data Analysis & NLP Tool

**Branch**: `001-nlp-data-viz`

## Prerequisites

- **Python**: 3.11+
- **Node.js**: 20+
- **npm** or **yarn**

## Setup

### 1. Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m nltk.downloader vader_lexicon  # Required for sentiment analysis
```

### 2. Frontend (React)

```bash
cd frontend
npm install
```

## Running the Application

### Start Backend

```bash
# From /backend
uvicorn src.app:app --reload --port 8000
```

- API Docs: http://localhost:8000/docs

### Start Frontend

```bash
# From /frontend
npm run dev
```

- UI: http://localhost:5173

## Key Commands

- **Run Backend Tests**: `pytest`
- **Run Frontend Tests**: `npm test` (or `npx vitest`)
- **Format Code**:
    - Python: `black .`
    - JS/TS: `npm run format`

## Troubleshooting

- **NLTK Data Missing**: If sentiment analysis fails, ensure you ran `python -m nltk.downloader vader_lexicon`.
- **CORS Errors**: The backend is configured to allow localhost:5173 by default. Check `src/app.py` middleware if port changes.
