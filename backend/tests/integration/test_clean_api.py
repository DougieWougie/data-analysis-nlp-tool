"""Integration tests for cleaning API endpoint."""
import pytest
from fastapi.testclient import TestClient
import io


@pytest.fixture
def client():
    """Create test client."""
    from src.app import app
    return TestClient(app)


@pytest.fixture
def uploaded_session(client):
    """Upload a CSV file and return session_id."""
    content = b"name,age,score,city\nAlice,25,95.5,NYC\nBob,,87.3,LA\nCharlie,30,,Chicago\n"
    csv_file = io.BytesIO(content)

    response = client.post(
        "/api/v1/upload",
        files={"file": ("test.csv", csv_file, "text/csv")}
    )

    assert response.status_code == 200
    return response.json()["session_id"]


def test_drop_column(client, uploaded_session):
    """Test dropping a column."""
    operations = [
        {
            "type": "DROP_COLUMNS",
            "params": {"columns": ["city"]}
        }
    ]

    response = client.post(
        f"/api/v1/dataset/{uploaded_session}/clean",
        json=operations
    )

    assert response.status_code == 200
    data = response.json()
    assert data["column_count"] == 3
    column_names = [col["name"] for col in data["columns"]]
    assert "city" not in column_names
    assert "name" in column_names


def test_rename_column(client, uploaded_session):
    """Test renaming a column."""
    operations = [
        {
            "type": "RENAME_COLUMN",
            "params": {"old_name": "name", "new_name": "full_name"}
        }
    ]

    response = client.post(
        f"/api/v1/dataset/{uploaded_session}/clean",
        json=operations
    )

    assert response.status_code == 200
    data = response.json()
    column_names = [col["name"] for col in data["columns"]]
    assert "name" not in column_names
    assert "full_name" in column_names


def test_fill_na(client, uploaded_session):
    """Test filling NA values."""
    operations = [
        {
            "type": "FILL_NA",
            "params": {"column": "age", "strategy": "mean"}
        }
    ]

    response = client.post(
        f"/api/v1/dataset/{uploaded_session}/clean",
        json=operations
    )

    assert response.status_code == 200
    data = response.json()

    # Check that age column has no missing values
    age_column = next(col for col in data["columns"] if col["name"] == "age")
    assert age_column["missing_count"] == 0


def test_drop_na_rows(client, uploaded_session):
    """Test dropping rows with NA values."""
    operations = [
        {
            "type": "DROP_NA",
            "params": {}
        }
    ]

    response = client.post(
        f"/api/v1/dataset/{uploaded_session}/clean",
        json=operations
    )

    assert response.status_code == 200
    data = response.json()

    # Only Alice has no NA values, so should have 1 row
    assert data["row_count"] == 1


def test_multiple_operations(client, uploaded_session):
    """Test applying multiple cleaning operations."""
    operations = [
        {
            "type": "FILL_NA",
            "params": {"column": "age", "strategy": "mean"}
        },
        {
            "type": "DROP_COLUMNS",
            "params": {"columns": ["city"]}
        }
    ]

    response = client.post(
        f"/api/v1/dataset/{uploaded_session}/clean",
        json=operations
    )

    assert response.status_code == 200
    data = response.json()

    # Check column was dropped
    assert data["column_count"] == 3
    column_names = [col["name"] for col in data["columns"]]
    assert "city" not in column_names

    # Check NA was filled
    age_column = next(col for col in data["columns"] if col["name"] == "age")
    assert age_column["missing_count"] == 0


def test_clean_invalid_session(client):
    """Test cleaning with invalid session ID."""
    operations = [
        {
            "type": "DROP_COLUMNS",
            "params": {"columns": ["city"]}
        }
    ]

    response = client.post(
        "/api/v1/dataset/invalid-session-id/clean",
        json=operations
    )

    assert response.status_code == 404


def test_clean_empty_operations(client, uploaded_session):
    """Test cleaning with empty operations list."""
    response = client.post(
        f"/api/v1/dataset/{uploaded_session}/clean",
        json=[]
    )

    # Should return unchanged dataset
    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] == 3


def test_clean_invalid_operation_type(client, uploaded_session):
    """Test cleaning with invalid operation type."""
    operations = [
        {
            "type": "INVALID_TYPE",
            "params": {}
        }
    ]

    response = client.post(
        f"/api/v1/dataset/{uploaded_session}/clean",
        json=operations
    )

    # Pydantic validation returns 422 for enum validation errors
    assert response.status_code == 422
