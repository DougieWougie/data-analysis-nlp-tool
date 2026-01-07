"""Service for cleaning and transforming datasets."""
import pandas as pd
from typing import List
from src.models.cleaning import CleaningOperation, OperationType


class CleaningService:
    """Handles data cleaning operations on pandas DataFrames."""

    def apply_operation(self, df: pd.DataFrame, operation: CleaningOperation) -> pd.DataFrame:
        """
        Apply a single cleaning operation to a DataFrame.

        Args:
            df: The DataFrame to clean
            operation: The cleaning operation to apply

        Returns:
            The cleaned DataFrame

        Raises:
            ValueError: If operation type is unknown
        """
        # Create a copy to avoid modifying the original
        result = df.copy()

        if operation.type == OperationType.DROP_COLUMNS:
            return self._drop_columns(result, operation.params)

        elif operation.type == OperationType.RENAME_COLUMN:
            return self._rename_column(result, operation.params)

        elif operation.type == OperationType.DROP_NA:
            return self._drop_na(result, operation.params)

        elif operation.type == OperationType.FILL_NA:
            return self._fill_na(result, operation.params)

        elif operation.type == OperationType.CAST_TYPE:
            return self._cast_type(result, operation.params)

        else:
            raise ValueError(f"Unknown operation type: {operation.type}")

    def apply_operations(
        self, df: pd.DataFrame, operations: List[CleaningOperation]
    ) -> pd.DataFrame:
        """
        Apply multiple cleaning operations in sequence.

        Args:
            df: The DataFrame to clean
            operations: List of cleaning operations to apply

        Returns:
            The cleaned DataFrame
        """
        result = df.copy()
        for operation in operations:
            result = self.apply_operation(result, operation)
        return result

    def _drop_columns(self, df: pd.DataFrame, params: dict) -> pd.DataFrame:
        """Drop specified columns."""
        columns = params.get("columns", [])
        # Only drop columns that exist
        columns_to_drop = [col for col in columns if col in df.columns]
        return df.drop(columns=columns_to_drop)

    def _rename_column(self, df: pd.DataFrame, params: dict) -> pd.DataFrame:
        """Rename a column."""
        old_name = params.get("old_name")
        new_name = params.get("new_name")

        if old_name not in df.columns:
            raise ValueError(f"Column '{old_name}' does not exist")

        return df.rename(columns={old_name: new_name})

    def _drop_na(self, df: pd.DataFrame, params: dict) -> pd.DataFrame:
        """Drop rows with NA values."""
        columns = params.get("columns", None)

        if columns:
            # Drop rows with NA in specific columns
            return df.dropna(subset=columns)
        else:
            # Drop rows with NA in any column
            return df.dropna()

    def _fill_na(self, df: pd.DataFrame, params: dict) -> pd.DataFrame:
        """Fill NA values using various strategies."""
        column = params.get("column")
        strategy = params.get("strategy", "constant")

        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist")

        result = df.copy()

        if strategy == "mean":
            fill_value = result[column].mean()
            result[column] = result[column].fillna(fill_value)

        elif strategy == "median":
            fill_value = result[column].median()
            result[column] = result[column].fillna(fill_value)

        elif strategy == "mode":
            # Use the most common value
            fill_value = result[column].mode()[0] if not result[column].mode().empty else None
            if fill_value is not None:
                result[column] = result[column].fillna(fill_value)

        elif strategy == "constant":
            fill_value = params.get("value", 0)
            result[column] = result[column].fillna(fill_value)

        else:
            raise ValueError(f"Unknown fill strategy: {strategy}")

        return result

    def _cast_type(self, df: pd.DataFrame, params: dict) -> pd.DataFrame:
        """Cast a column to a different data type."""
        column = params.get("column")
        dtype = params.get("dtype")

        if column not in df.columns:
            raise ValueError(f"Column '{column}' does not exist")

        result = df.copy()
        result[column] = result[column].astype(dtype)
        return result
