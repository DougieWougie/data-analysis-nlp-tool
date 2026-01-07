"""Integration tests for upload API endpoint."""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import io


@pytest.fixture
def client():
    """Create test client."""
    from src.app import app
    return TestClient(app)


@pytest.fixture
def sample_csv():
    """Create a sample CSV file content."""
    content = b"name,age,score\nAlice,25,95.5\nBob,30,87.3\n"
    return io.BytesIO(content)


@pytest.fixture
def sample_excel():
    """Create a sample Excel file."""
    import pandas as pd
    df = pd.DataFrame({
        "product": ["A", "B"],
        "price": [10.5, 20.0],
    })
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer


def test_upload_csv_success(client, sample_csv):
    """Test successful CSV upload."""
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.csv", sample_csv, "text/csv")}
    )

    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "metadata" in data
    assert data["metadata"]["row_count"] == 2
    assert data["metadata"]["column_count"] == 3


def test_upload_excel_success(client, sample_excel):
    """Test successful Excel upload."""
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.xlsx", sample_excel, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )

    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert "metadata" in data
    assert data["metadata"]["row_count"] == 2


def test_upload_invalid_format(client):
    """Test upload with invalid file format."""
    invalid_file = io.BytesIO(b"invalid content")
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.txt", invalid_file, "text/plain")}
    )

    assert response.status_code in [400, 422]


def test_upload_missing_file(client):
    """Test upload with missing file."""
    response = client.post("/api/v1/upload")

    assert response.status_code == 422


def test_upload_metadata_contains_preview(client, sample_csv):
    """Test that upload response contains data preview."""
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.csv", sample_csv, "text/csv")}
    )

    assert response.status_code == 200
    data = response.json()
    assert "preview" in data["metadata"]
    assert len(data["metadata"]["preview"]) > 0


def test_upload_metadata_contains_column_info(client, sample_csv):
    """Test that upload response contains column metadata."""
    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.csv", sample_csv, "text/csv")}
    )

    assert response.status_code == 200
    data = response.json()
    assert "columns" in data["metadata"]
    assert len(data["metadata"]["columns"]) == 3

    # Verify column structure
    column = data["metadata"]["columns"][0]
    assert "name" in column
    assert "data_type" in column
    assert "missing_count" in column
