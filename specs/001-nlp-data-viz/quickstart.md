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

**Note**: The VADER lexicon will be automatically downloaded on first use if not present.

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

## Features

### 1. Data Upload & Preview
- Upload CSV or Excel files (up to 10MB recommended)
- Automatic data type detection (Numerical, Categorical, Text, DateTime, Boolean)
- Preview first 50 rows
- View column statistics (row count, missing values)

### 2. Data Cleaning
- **Drop Columns**: Remove unwanted columns
- **Rename Columns**: Change column names
- **Fill Missing Values**: Use mean, median, mode, or constant values
- **Drop NA Rows**: Remove rows with missing data
- **Cast Type**: Convert column data types

### 3. Visualization Suggestions
- Automatic chart recommendations based on data types
- Supported charts: Bar, Line, Scatter, Pie, Histogram
- Interactive chart rendering with Recharts
- Real-time updates after data cleaning

### 4. Sentiment Analysis (NLP)
- Click "🔍 Sentiment" button on any text column
- VADER-based sentiment scoring (-1 to 1)
- Automatic labeling (POSITIVE, NEGATIVE, NEUTRAL)
- Visual sentiment distribution chart
- Export results with sentiment columns

### 5. Export
- Download cleaned/analyzed data as CSV
- Preserves all transformations and analysis results

## Troubleshooting

- **NLTK Data Missing**: If sentiment analysis fails, ensure you ran `python -m nltk.downloader vader_lexicon`. The service will attempt auto-download on first use.
- **CORS Errors**: The backend is configured to allow localhost:5173 by default. Check `src/app.py` middleware if port changes.
- **Port Conflicts**: If port 8000 or 5173 is in use, modify the port in the startup commands.
- **File Upload Issues**: Ensure files are valid CSV/Excel format and under 10MB for optimal performance.
