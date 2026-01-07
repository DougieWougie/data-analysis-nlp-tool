"""Core data models for the application."""
from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class DataType(str, Enum):
    """Column data types."""

    NUMERICAL = "Numerical"
    CATEGORICAL = "Categorical"
    DATETIME = "DateTime"
    TEXT = "Text"
    BOOLEAN = "Boolean"


class ColumnMetadata(BaseModel):
    """Metadata for a single column."""

    name: str
    data_type: DataType
    missing_count: int = 0


class DatasetMetadata(BaseModel):
    """Metadata about the current dataset state."""

    row_count: int
    column_count: int
    columns: List[ColumnMetadata]
    preview: List[Dict[str, Any]] = Field(default_factory=list, description="First 50 rows")


class AnalysisSession(BaseModel):
    """Represents a user's analysis session."""

    id: str = Field(description="UUID session identifier")
    created_at: datetime = Field(default_factory=datetime.now)
    file_path: str = Field(description="Path to the current dataset file")
    original_filename: str


class UploadResponse(BaseModel):
    """Response from file upload endpoint."""

    session_id: str
    metadata: DatasetMetadata
