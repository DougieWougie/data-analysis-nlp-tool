"""API route handlers."""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
from typing import List
import logging

from src.models.core import UploadResponse, DatasetMetadata
from src.models.cleaning import CleaningOperation
from src.services.session_service import SessionService
from src.services.parsing_service import ParsingService
from src.services.cleaning_service import CleaningService
from src.utils.file_manager import FileManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")

# Initialize services
session_service = SessionService()
parsing_service = ParsingService()
cleaning_service = CleaningService()
file_manager = FileManager()


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
