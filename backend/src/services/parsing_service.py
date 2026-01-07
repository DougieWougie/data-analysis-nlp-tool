"""Service for parsing and analyzing uploaded files."""
from pathlib import Path
import pandas as pd
import numpy as np
from src.models.core import DatasetMetadata, ColumnMetadata, DataType
from src.utils.file_manager import FileManager


class ParsingService:
    """Parses uploaded files and extracts metadata."""

    PREVIEW_ROWS = 50

    def parse_file(self, file_path: Path) -> DatasetMetadata:
        """
        Parse a file and extract metadata.

        Args:
            file_path: Path to the file to parse

        Returns:
            DatasetMetadata with row count, column info, and preview

        Raises:
            ValueError: If file format is not supported
        """
        # Load the DataFrame
        df = FileManager.load_dataframe(file_path)

        # Extract metadata
        row_count = len(df)
        column_count = len(df.columns)

        # Analyze columns
        columns = [self._analyze_column(df, col) for col in df.columns]

        # Generate preview (first N rows)
        preview = df.head(self.PREVIEW_ROWS).replace({np.nan: None}).to_dict(orient="records")

        return DatasetMetadata(
            row_count=row_count,
            column_count=column_count,
            columns=columns,
            preview=preview,
        )

    def _analyze_column(self, df: pd.DataFrame, column_name: str) -> ColumnMetadata:
        """
        Analyze a single column and determine its metadata.

        Args:
            df: The DataFrame
            column_name: Name of the column to analyze

        Returns:
            ColumnMetadata for the column
        """
        series = df[column_name]
        missing_count = int(series.isna().sum())

        # Detect data type
        data_type = self._detect_data_type(series)

        return ColumnMetadata(
            name=column_name,
            data_type=data_type,
            missing_count=missing_count,
        )

    def _detect_data_type(self, series: pd.Series) -> DataType:
        """
        Detect the data type of a pandas Series.

        Args:
            series: The pandas Series to analyze

        Returns:
            Detected DataType
        """
        # Drop NA values for type detection
        series_clean = series.dropna()

        if len(series_clean) == 0:
            return DataType.TEXT

        # Check for boolean
        if pd.api.types.is_bool_dtype(series):
            return DataType.BOOLEAN

        # Check if values can be interpreted as boolean strings
        if series_clean.dtype == object:
            unique_values = set(str(v).lower() for v in series_clean.unique())
            if unique_values.issubset({'true', 'false', '1', '0', 'yes', 'no'}):
                return DataType.BOOLEAN

        # Check for numerical
        if pd.api.types.is_numeric_dtype(series):
            return DataType.NUMERICAL

        # Check for datetime
        if pd.api.types.is_datetime64_any_dtype(series):
            return DataType.DATETIME

        # Try to parse as datetime
        if series_clean.dtype == object:
            try:
                pd.to_datetime(series_clean, errors='raise')
                return DataType.DATETIME
            except (ValueError, TypeError):
                pass

        # Check for categorical (if few unique values relative to total)
        if series_clean.dtype == object:
            unique_ratio = len(series_clean.unique()) / len(series_clean)
            if unique_ratio < 0.5 and len(series_clean.unique()) < 20:
                return DataType.CATEGORICAL

        # Default to TEXT
        return DataType.TEXT
