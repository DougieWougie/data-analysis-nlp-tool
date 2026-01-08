"""Pydantic models for visualization suggestions."""
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ChartType(str, Enum):
    """Supported chart types for visualization."""
    BAR = "BAR"
    LINE = "LINE"
    SCATTER = "SCATTER"
    PIE = "PIE"
    HISTOGRAM = "HISTOGRAM"


class VisualizationSuggestion(BaseModel):
    """A recommended chart configuration based on data analysis."""
    type: ChartType = Field(..., description="The type of chart to render")
    title: str = Field(..., description="Suggested title for the chart")
    x_axis: Optional[str] = Field(None, description="Column name for x-axis (if applicable)")
    y_axis: Optional[str] = Field(None, description="Column name for y-axis (if applicable)")
    description: str = Field(..., description="Explanation of why this chart was suggested")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "type": "BAR",
                "title": "Sales by Category",
                "x_axis": "category",
                "y_axis": "sales",
                "description": "Bar chart showing sales distribution across categories"
            }
        }
