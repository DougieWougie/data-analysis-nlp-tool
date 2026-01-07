"""Unit tests for parsing service."""
import pytest
import pandas as pd
from pathlib import Path
import tempfile
from src.services.parsing_service import ParsingService
from src.models.core import DataType


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age,score,is_active\n")
        f.write("Alice,25,95.5,true\n")
        f.write("Bob,30,87.3,false\n")
        f.write("Charlie,,92.1,true\n")
        temp_path = Path(f.name)
    yield temp_path
    temp_path.unlink(missing_ok=True)


@pytest.fixture
def temp_excel_file():
    """Create a temporary Excel file for testing."""
    df = pd.DataFrame({
        "product": ["A", "B", "C"],
        "price": [10.5, 20.0, 15.75],
        "quantity": [5, None, 10],
    })
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as f:
        temp_path = Path(f.name)
        df.to_excel(temp_path, index=False)
    yield temp_path
    temp_path.unlink(missing_ok=True)


def test_parse_csv_file(temp_csv_file):
    """Test parsing a CSV file."""
    service = ParsingService()
    metadata = service.parse_file(temp_csv_file)

    assert metadata.row_count == 3
    assert metadata.column_count == 4
    assert len(metadata.columns) == 4
    assert len(metadata.preview) == 3


def test_parse_excel_file(temp_excel_file):
    """Test parsing an Excel file."""
    service = ParsingService()
    metadata = service.parse_file(temp_excel_file)

    assert metadata.row_count == 3
    assert metadata.column_count == 3
    assert len(metadata.columns) == 3


def test_detect_data_types(temp_csv_file):
    """Test data type detection."""
    service = ParsingService()
    metadata = service.parse_file(temp_csv_file)

    column_types = {col.name: col.data_type for col in metadata.columns}
    assert column_types["name"] == DataType.TEXT
    assert column_types["age"] == DataType.NUMERICAL
    assert column_types["score"] == DataType.NUMERICAL
    assert column_types["is_active"] == DataType.BOOLEAN


def test_detect_missing_values(temp_csv_file):
    """Test missing value detection."""
    service = ParsingService()
    metadata = service.parse_file(temp_csv_file)

    age_column = next(col for col in metadata.columns if col.name == "age")
    assert age_column.missing_count == 1


def test_invalid_file_format():
    """Test handling of invalid file format."""
    service = ParsingService()
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
        temp_path = Path(f.name)
        f.write(b"invalid content")

    try:
        with pytest.raises(ValueError, match="Unsupported file format"):
            service.parse_file(temp_path)
    finally:
        temp_path.unlink(missing_ok=True)


def test_preview_limit(temp_csv_file):
    """Test that preview is limited to first 50 rows."""
    # Create a CSV with more than 50 rows
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("col1,col2\n")
        for i in range(100):
            f.write(f"{i},{i*2}\n")
        temp_path = Path(f.name)

    try:
        service = ParsingService()
        metadata = service.parse_file(temp_path)

        assert metadata.row_count == 100
        assert len(metadata.preview) == 50
    finally:
        temp_path.unlink(missing_ok=True)
