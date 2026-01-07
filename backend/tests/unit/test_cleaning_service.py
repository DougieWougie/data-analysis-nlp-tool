"""Unit tests for cleaning service."""
import pytest
import pandas as pd
import tempfile
from pathlib import Path
from src.services.cleaning_service import CleaningService
from src.models.cleaning import CleaningOperation, OperationType


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie", "David"],
        "age": [25, None, 30, 28],
        "score": [95.5, 87.3, None, 92.1],
        "city": ["NYC", "LA", "Chicago", "Boston"],
    })


@pytest.fixture
def cleaning_service():
    """Create cleaning service instance."""
    return CleaningService()


def test_drop_columns(cleaning_service, sample_dataframe):
    """Test dropping columns."""
    operation = CleaningOperation(
        type=OperationType.DROP_COLUMNS,
        params={"columns": ["city"]}
    )

    result = cleaning_service.apply_operation(sample_dataframe, operation)

    assert "city" not in result.columns
    assert len(result.columns) == 3
    assert "name" in result.columns
    assert "age" in result.columns


def test_drop_multiple_columns(cleaning_service, sample_dataframe):
    """Test dropping multiple columns."""
    operation = CleaningOperation(
        type=OperationType.DROP_COLUMNS,
        params={"columns": ["city", "score"]}
    )

    result = cleaning_service.apply_operation(sample_dataframe, operation)

    assert "city" not in result.columns
    assert "score" not in result.columns
    assert len(result.columns) == 2


def test_rename_column(cleaning_service, sample_dataframe):
    """Test renaming a column."""
    operation = CleaningOperation(
        type=OperationType.RENAME_COLUMN,
        params={"old_name": "name", "new_name": "full_name"}
    )

    result = cleaning_service.apply_operation(sample_dataframe, operation)

    assert "name" not in result.columns
    assert "full_name" in result.columns
    assert list(result["full_name"]) == ["Alice", "Bob", "Charlie", "David"]


def test_drop_na_rows(cleaning_service, sample_dataframe):
    """Test dropping rows with NA values."""
    operation = CleaningOperation(
        type=OperationType.DROP_NA,
        params={}
    )

    result = cleaning_service.apply_operation(sample_dataframe, operation)

    # Should have 2 rows (Alice and David) without any NA values
    assert len(result) == 2
    assert result.iloc[0]["name"] == "Alice"
    assert result.iloc[1]["name"] == "David"


def test_drop_na_specific_columns(cleaning_service, sample_dataframe):
    """Test dropping rows with NA in specific columns."""
    operation = CleaningOperation(
        type=OperationType.DROP_NA,
        params={"columns": ["age"]}
    )

    result = cleaning_service.apply_operation(sample_dataframe, operation)

    # Should have 3 rows (all except Bob who has NA in age)
    assert len(result) == 3
    assert "Bob" not in result["name"].values


def test_fill_na_with_mean(cleaning_service, sample_dataframe):
    """Test filling NA with mean value."""
    operation = CleaningOperation(
        type=OperationType.FILL_NA,
        params={"column": "age", "strategy": "mean"}
    )

    result = cleaning_service.apply_operation(sample_dataframe, operation)

    # Mean of [25, 30, 28] = 27.67
    assert result["age"].isna().sum() == 0
    assert result.iloc[1]["age"] == pytest.approx(27.67, rel=0.01)


def test_fill_na_with_median(cleaning_service, sample_dataframe):
    """Test filling NA with median value."""
    operation = CleaningOperation(
        type=OperationType.FILL_NA,
        params={"column": "age", "strategy": "median"}
    )

    result = cleaning_service.apply_operation(sample_dataframe, operation)

    # Median of [25, 30, 28] = 28
    assert result["age"].isna().sum() == 0
    assert result.iloc[1]["age"] == 28


def test_fill_na_with_constant(cleaning_service, sample_dataframe):
    """Test filling NA with a constant value."""
    operation = CleaningOperation(
        type=OperationType.FILL_NA,
        params={"column": "age", "strategy": "constant", "value": 0}
    )

    result = cleaning_service.apply_operation(sample_dataframe, operation)

    assert result["age"].isna().sum() == 0
    assert result.iloc[1]["age"] == 0


def test_fill_na_with_mode(cleaning_service, sample_dataframe):
    """Test filling NA with mode (most common value)."""
    df = pd.DataFrame({
        "category": ["A", "A", "B", None, "A"]
    })

    operation = CleaningOperation(
        type=OperationType.FILL_NA,
        params={"column": "category", "strategy": "mode"}
    )

    result = cleaning_service.apply_operation(df, operation)

    assert result["category"].isna().sum() == 0
    assert result.iloc[3]["category"] == "A"


def test_apply_multiple_operations(cleaning_service, sample_dataframe):
    """Test applying multiple operations in sequence."""
    operations = [
        CleaningOperation(
            type=OperationType.DROP_COLUMNS,
            params={"columns": ["city"]}
        ),
        CleaningOperation(
            type=OperationType.FILL_NA,
            params={"column": "age", "strategy": "mean"}
        ),
    ]

    result = cleaning_service.apply_operations(sample_dataframe, operations)

    assert "city" not in result.columns
    assert result["age"].isna().sum() == 0


def test_invalid_operation_type(cleaning_service, sample_dataframe):
    """Test handling of invalid operation type."""
    # Pydantic will validate the enum, so we need to bypass it
    # Create an operation with a valid type, then modify it
    from src.models.cleaning import OperationType
    import pytest
    from pydantic import ValidationError

    # Test that Pydantic validates the enum
    with pytest.raises(ValidationError):
        CleaningOperation(
            type="INVALID_TYPE",  # type: ignore
            params={}
        )


def test_drop_nonexistent_column(cleaning_service, sample_dataframe):
    """Test dropping a column that doesn't exist."""
    operation = CleaningOperation(
        type=OperationType.DROP_COLUMNS,
        params={"columns": ["nonexistent"]}
    )

    # Should not raise an error, just ignore nonexistent columns
    result = cleaning_service.apply_operation(sample_dataframe, operation)
    assert len(result.columns) == 4
