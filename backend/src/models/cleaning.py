"""Data models for cleaning operations."""
from enum import Enum
from typing import Dict, Any, List
from pydantic import BaseModel, Field


class OperationType(str, Enum):
    """Types of cleaning operations."""

    DROP_COLUMNS = "DROP_COLUMNS"
    RENAME_COLUMN = "RENAME_COLUMN"
    DROP_NA = "DROP_NA"
    FILL_NA = "FILL_NA"
    CAST_TYPE = "CAST_TYPE"


class CleaningOperation(BaseModel):
    """Represents a single cleaning operation to apply to a dataset."""

    type: OperationType
    params: Dict[str, Any] = Field(default_factory=dict)


class CleaningRequest(BaseModel):
    """Request body for cleaning operations."""

    operations: List[CleaningOperation] = Field(default_factory=list)
