"""Test TSV file handling with .xls extension."""
import pytest
import tempfile
from pathlib import Path
from src.utils.file_manager import FileManager


def test_load_tsv_with_xls_extension():
    """Test loading a TSV file that has a .xls extension."""
    # Create a TSV file with .xls extension
    content = "ID\tYear\tName\tValue\n1\t2020\tAlice\t100\n2\t2021\tBob\t200\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".xls", delete=False) as f:
        f.write(content)
        temp_path = Path(f.name)

    try:
        # Should successfully read as TSV
        df = FileManager.load_dataframe(temp_path)

        # Verify the data
        assert len(df) == 2
        assert len(df.columns) == 4
        assert list(df.columns) == ["ID", "Year", "Name", "Value"]
        assert df.iloc[0]["Name"] == "Alice"
        assert df.iloc[1]["Value"] == 200
    finally:
        temp_path.unlink(missing_ok=True)


def test_load_csv_with_xls_extension():
    """Test loading a CSV file that has a .xls extension."""
    # Create a CSV file with .xls extension
    content = "ID,Year,Name,Value\n1,2020,Alice,100\n2,2021,Bob,200\n"
    with tempfile.NamedTemporaryFile(mode="w", suffix=".xls", delete=False) as f:
        f.write(content)
        temp_path = Path(f.name)

    try:
        # Should successfully read as CSV
        df = FileManager.load_dataframe(temp_path)

        # Verify the data
        assert len(df) == 2
        assert len(df.columns) == 4
        assert list(df.columns) == ["ID", "Year", "Name", "Value"]
        assert df.iloc[0]["Name"] == "Alice"
        assert int(df.iloc[1]["Value"]) == 200
    finally:
        temp_path.unlink(missing_ok=True)


def test_empty_xls_file():
    """Test that empty files raise appropriate errors."""
    # Create an empty file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".xls", delete=False) as f:
        f.write("")
        temp_path = Path(f.name)

    try:
        with pytest.raises(ValueError, match="Failed to read .xls file"):
            FileManager.load_dataframe(temp_path)
    finally:
        temp_path.unlink(missing_ok=True)
