# Research: Data Analysis & NLP Tool

**Feature**: Data Analysis & NLP Tool
**Date**: 2026-01-07
**Status**: Complete

## 1. Backend Framework
**Decision**: FastAPI
**Rationale**: 
- Native support for asynchronous request handling (ASGI), crucial for potentially long-running data processing tasks.
- Pydantic integration ensures strict data validation for inputs/outputs, which is vital when passing data frames between backend and frontend.
- Automatic interactive documentation (Swagger UI) simplifies testing for the frontend team.
- High performance for data-intensive applications compared to Flask.
**Alternatives Considered**:
- **Flask**: Simpler but lacks native async support and automatic validation, which would require more boilerplate for this specific use case.
- **Django**: Too heavy for a specific data analysis tool; we don't need a full ORM or admin panel.

## 2. Frontend Visualization Library
**Decision**: Recharts
**Rationale**: 
- Built specifically for React with a component-based architecture (composable).
- Good balance of simplicity and customizability.
- Supports all required chart types (Bar, Line, Scatter, Pie).
- Large community and active maintenance.
**Alternatives Considered**:
- **Chart.js (react-chartjs-2)**: Good, but canvas-based interaction can sometimes be less "React-native" than Recharts' SVG approach.
- **D3.js**: Too low-level; would slow down development significantly for standard charts.
- **Victory**: Good alternative, but Recharts API is slightly more intuitive for rapid prototyping.

## 3. Data Persistence & File Handling
**Decision**: Session-based Temporary Filesystem Storage
**Rationale**:
- The requirements specify "current analysis session" and "export as new CSV", implying no need for long-term database persistence.
- Python's `tempfile` module and FastAPI's `UploadFile` (using `SpooledTemporaryFile`) provide secure, efficient handling of uploads.
- We will generate a unique Session ID (UUID) for each user interaction to create a sandboxed temporary directory (e.g., `/tmp/{uuid}/`) to store the raw and cleaned datasets.
**Security**: Files will be auto-deleted after a timeout or explicit session end to prevent storage exhaustion.

## 4. NLP Integration Strategy
**Decision**: NLTK with VADER Sentiment
**Rationale**:
- NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner) is specifically tuned for social media and short texts, which fits the "reviews/feedback" use case well.
- It is fast and doesn't require training a model (rule-based), making it ideal for a lightweight analysis tool.
- **Implementation**: Expose a `/analyze/sentiment` endpoint that accepts a column name and returns scores attached to row IDs.

## 5. Implementation Strategy Update
- **Backend Structure**:
    - `POST /upload`: Returns a Session ID.
    - `POST /clean/{session_id}`: Applies cleaning, overwrites temp file.
    - `GET /visualize/{session_id}`: Returns JSON specific for Recharts.
    - `POST /sentiment/{session_id}`: Returns sentiment scores.
    - `GET /export/{session_id}`: Downloads CSV.
