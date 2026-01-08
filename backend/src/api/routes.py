"""API route handlers."""
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from pathlib import Path
from typing import List
import logging
import io

from src.models.core import UploadResponse, DatasetMetadata
from src.models.cleaning import CleaningOperation
from src.models.visualization import VisualizationSuggestion
from src.services.session_service import SessionService
from src.services.parsing_service import ParsingService
from src.services.cleaning_service import CleaningService
from src.services.suggestion_service import SuggestionService
from src.services.nlp_service import NLPService
from src.utils.file_manager import FileManager
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")

# Initialize services
session_service = SessionService()
parsing_service = ParsingService()
cleaning_service = CleaningService()
suggestion_service = SuggestionService()
nlp_service = NLPService()
file_manager = FileManager()


# Request models
class SentimentRequest(BaseModel):
    """Request model for sentiment analysis."""
    target_column: str


@router.post("/upload", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload a CSV or Excel file and create a new analysis session.

    Args:
        file: The uploaded file

    Returns:
        UploadResponse with session_id and dataset metadata

    Raises:
        HTTPException: If file format is unsupported or parsing fails
    """
    try:
        # Validate file extension
        filename = file.filename or ""
        file_ext = Path(filename).suffix.lower()
        if file_ext not in [".csv", ".xlsx", ".xls"]:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format: {file_ext}. Please upload CSV or Excel files."
            )

        # Create session
        session_id = session_service.create_session()
        session_dir = session_service.get_session_path(session_id)

        # Save uploaded file
        file_path = file_manager.get_dataset_path(session_dir, f"dataset{file_ext}")
        file_manager.save_uploaded_file(file.file, file_path)

        # Parse file and extract metadata
        metadata = parsing_service.parse_file(file_path)

        logger.info(f"File uploaded successfully. Session: {session_id}, File: {filename}")

        return UploadResponse(session_id=session_id, metadata=metadata)

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Parsing error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail="File upload failed")


@router.get("/dataset/{session_id}", response_model=DatasetMetadata)
async def get_dataset(session_id: str):
    """
    Get the current state of a dataset.

    Args:
        session_id: The session UUID

    Returns:
        DatasetMetadata with current dataset state

    Raises:
        HTTPException: If session not found
    """
    try:
        # Check if session exists
        if not session_service.session_exists(session_id):
            raise HTTPException(status_code=404, detail="Session not found")

        # Find the dataset file
        session_dir = session_service.get_session_path(session_id)
        dataset_files = list(session_dir.glob("dataset.*"))

        if not dataset_files:
            raise HTTPException(status_code=404, detail="No dataset found in session")

        # Parse the dataset file
        dataset_file = dataset_files[0]
        metadata = parsing_service.parse_file(dataset_file)

        return metadata

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to retrieve dataset: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve dataset")


@router.post("/dataset/{session_id}/clean", response_model=DatasetMetadata)
async def clean_dataset(session_id: str, operations: List[CleaningOperation]):
    """
    Apply cleaning operations to a dataset.

    Args:
        session_id: The session UUID
        operations: List of cleaning operations to apply

    Returns:
        DatasetMetadata with the cleaned dataset state

    Raises:
        HTTPException: If session not found or cleaning fails
    """
    try:
        # Check if session exists
        if not session_service.session_exists(session_id):
            raise HTTPException(status_code=404, detail="Session not found")

        # Find the dataset file
        session_dir = session_service.get_session_path(session_id)
        dataset_files = list(session_dir.glob("dataset.*"))

        if not dataset_files:
            raise HTTPException(status_code=404, detail="No dataset found in session")

        # Load the current dataset
        dataset_file = dataset_files[0]
        df = file_manager.load_dataframe(dataset_file)

        # Apply cleaning operations
        cleaned_df = cleaning_service.apply_operations(df, operations)

        # Save the cleaned dataset (path may change if .xls -> .xlsx)
        saved_file = file_manager.save_dataframe(cleaned_df, dataset_file)

        # Parse and return metadata
        metadata = parsing_service.parse_file(saved_file)

        logger.info(f"Cleaned dataset for session {session_id}. Applied {len(operations)} operations.")

        return metadata

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Cleaning validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Failed to clean dataset: {e}")
        raise HTTPException(status_code=500, detail="Failed to clean dataset")


@router.get("/dataset/{session_id}/export")
async def export_dataset(session_id: str):
    """
    Export the current dataset as a CSV file.

    Args:
        session_id: The session UUID

    Returns:
        StreamingResponse with CSV file content

    Raises:
        HTTPException: If session not found or export fails
    """
    try:
        # Check if session exists
        if not session_service.session_exists(session_id):
            raise HTTPException(status_code=404, detail="Session not found")

        # Find the dataset file
        session_dir = session_service.get_session_path(session_id)
        dataset_files = list(session_dir.glob("dataset.*"))

        if not dataset_files:
            raise HTTPException(status_code=404, detail="No dataset found in session")

        # Load the current dataset
        dataset_file = dataset_files[0]
        df = file_manager.load_dataframe(dataset_file)

        # Convert to CSV in memory
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        logger.info(f"Exported dataset for session {session_id}")

        # Return CSV as streaming response
        return StreamingResponse(
            io.BytesIO(csv_buffer.getvalue().encode('utf-8')),
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=cleaned_dataset.csv"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to export dataset: {e}")
        raise HTTPException(status_code=500, detail="Failed to export dataset")


@router.get("/dataset/{session_id}/suggestions", response_model=List[VisualizationSuggestion])
async def get_visualization_suggestions(session_id: str):
    """
    Get visualization suggestions based on the current dataset.

    Args:
        session_id: The session UUID

    Returns:
        List of VisualizationSuggestion objects with recommended charts

    Raises:
        HTTPException: If session not found or analysis fails
    """
    try:
        # Check if session exists
        if not session_service.session_exists(session_id):
            raise HTTPException(status_code=404, detail="Session not found")

        # Find the dataset file
        session_dir = session_service.get_session_path(session_id)
        dataset_files = list(session_dir.glob("dataset.*"))

        if not dataset_files:
            raise HTTPException(status_code=404, detail="No dataset found in session")

        # Load the current dataset
        dataset_file = dataset_files[0]
        df = file_manager.load_dataframe(dataset_file)

        # Generate suggestions
        suggestions = suggestion_service.generate_suggestions(df)

        logger.info(f"Generated {len(suggestions)} visualization suggestions for session {session_id}")

        return suggestions

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to generate suggestions: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate visualization suggestions")


@router.post("/dataset/{session_id}/sentiment", response_model=DatasetMetadata)
async def analyze_sentiment(session_id: str, request: SentimentRequest):
    """
    Perform sentiment analysis on a text column in the dataset.

    Args:
        session_id: The session UUID
        request: SentimentRequest with target_column name

    Returns:
        DatasetMetadata with updated dataset including sentiment columns

    Raises:
        HTTPException: If session not found, column invalid, or analysis fails
    """
    try:
        # Check if session exists
        if not session_service.session_exists(session_id):
            raise HTTPException(status_code=404, detail="Session not found")

        # Find the dataset file
        session_dir = session_service.get_session_path(session_id)
        dataset_files = list(session_dir.glob("dataset.*"))

        if not dataset_files:
            raise HTTPException(status_code=404, detail="No dataset found in session")

        # Load the current dataset
        dataset_file = dataset_files[0]
        df = file_manager.load_dataframe(dataset_file)

        # Perform sentiment analysis
        try:
            analyzed_df = nlp_service.analyze_sentiment(df, request.target_column)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Save the updated dataset
        saved_file = file_manager.save_dataframe(analyzed_df, dataset_file)

        # Parse and return metadata
        metadata = parsing_service.parse_file(saved_file)

        logger.info(f"Sentiment analysis completed for session {session_id}, column: {request.target_column}")

        return metadata

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to analyze sentiment: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform sentiment analysis")
