"""Integration tests for visualization suggestions API endpoints."""
import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import io

from src.app import app

client = TestClient(app)


@pytest.fixture
def sample_csv_numeric():
    """Create a sample CSV file with numeric data."""
    csv_content = """sales,quantity,price
100,5,20.0
200,10,20.0
150,8,18.75
300,15,20.0
250,12,20.83"""
    return io.BytesIO(csv_content.encode())


@pytest.fixture
def sample_csv_categorical():
    """Create a sample CSV file with categorical data."""
    csv_content = """category,region,count
A,North,10
B,South,20
A,North,15
C,East,25
B,South,30"""
    return io.BytesIO(csv_content.encode())


@pytest.fixture
def sample_csv_mixed():
    """Create a sample CSV file with mixed data types."""
    csv_content = """date,sales,category,region
2024-01-01,100,A,North
2024-01-02,200,B,South
2024-01-03,150,A,North
2024-01-04,300,C,East
2024-01-05,250,B,South"""
    return io.BytesIO(csv_content.encode())


class TestSuggestionsAPI:
    """Test suite for visualization suggestions API."""

    def test_get_suggestions_success(self, sample_csv_numeric):
        """Test successful retrieval of visualization suggestions."""
        # Upload a file first
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("test.csv", sample_csv_numeric, "text/csv")}
        )
        assert upload_response.status_code == 200
        session_id = upload_response.json()["session_id"]

        # Get suggestions
        response = client.get(f"/api/v1/dataset/{session_id}/suggestions")
        assert response.status_code == 200

        suggestions = response.json()
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

        # Verify suggestion structure
        for suggestion in suggestions:
            assert "type" in suggestion
            assert "title" in suggestion
            assert "description" in suggestion
            assert suggestion["type"] in ["BAR", "LINE", "SCATTER", "PIE", "HISTOGRAM"]

    def test_get_suggestions_numeric_data(self, sample_csv_numeric):
        """Test suggestions for numeric data include appropriate chart types."""
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("numeric.csv", sample_csv_numeric, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        response = client.get(f"/api/v1/dataset/{session_id}/suggestions")
        assert response.status_code == 200

        suggestions = response.json()
        chart_types = [s["type"] for s in suggestions]

        # Should include scatter and histogram for numeric data
        assert "SCATTER" in chart_types or "HISTOGRAM" in chart_types

    def test_get_suggestions_categorical_data(self, sample_csv_categorical):
        """Test suggestions for categorical data include bar/pie charts."""
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("categorical.csv", sample_csv_categorical, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        response = client.get(f"/api/v1/dataset/{session_id}/suggestions")
        assert response.status_code == 200

        suggestions = response.json()
        chart_types = [s["type"] for s in suggestions]

        # Should include bar or pie charts for categorical data
        assert "BAR" in chart_types or "PIE" in chart_types

    def test_get_suggestions_time_series_data(self, sample_csv_mixed):
        """Test suggestions for time series data include line charts."""
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("timeseries.csv", sample_csv_mixed, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        response = client.get(f"/api/v1/dataset/{session_id}/suggestions")
        assert response.status_code == 200

        suggestions = response.json()
        chart_types = [s["type"] for s in suggestions]

        # Should include line charts for time series
        assert "LINE" in chart_types

    def test_get_suggestions_invalid_session(self):
        """Test suggestions endpoint with invalid session ID."""
        response = client.get("/api/v1/dataset/invalid-uuid/suggestions")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_suggestions_nonexistent_session(self):
        """Test suggestions endpoint with non-existent but valid UUID."""
        fake_uuid = "12345678-1234-1234-1234-123456789012"
        response = client.get(f"/api/v1/dataset/{fake_uuid}/suggestions")
        assert response.status_code == 404

    def test_suggestions_after_cleaning(self, sample_csv_numeric):
        """Test that suggestions update after data cleaning operations."""
        # Upload file
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("test.csv", sample_csv_numeric, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        # Get initial suggestions
        initial_response = client.get(f"/api/v1/dataset/{session_id}/suggestions")
        initial_suggestions = initial_response.json()

        # Drop a column
        clean_response = client.post(
            f"/api/v1/dataset/{session_id}/clean",
            json=[{
                "type": "DROP_COLUMNS",
                "params": {"columns": ["price"]}
            }]
        )
        assert clean_response.status_code == 200

        # Get updated suggestions
        updated_response = client.get(f"/api/v1/dataset/{session_id}/suggestions")
        assert updated_response.status_code == 200
        updated_suggestions = updated_response.json()

        # Suggestions should be recalculated (might be different)
        assert isinstance(updated_suggestions, list)

    def test_suggestions_response_format(self, sample_csv_mixed):
        """Test that suggestions response has correct format."""
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("test.csv", sample_csv_mixed, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        response = client.get(f"/api/v1/dataset/{session_id}/suggestions")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        suggestions = response.json()
        for suggestion in suggestions:
            # All suggestions should have these fields
            assert "type" in suggestion
            assert "title" in suggestion
            assert "description" in suggestion
            # x_axis and y_axis are optional depending on chart type
            if suggestion["type"] in ["BAR", "LINE", "SCATTER"]:
                assert "x_axis" in suggestion or "y_axis" in suggestion
