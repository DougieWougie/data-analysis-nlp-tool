"""Integration tests for NLP/sentiment analysis API endpoints."""
import pytest
from fastapi.testclient import TestClient
import io

from src.app import app

client = TestClient(app)


@pytest.fixture
def sample_csv_with_text():
    """Create a sample CSV file with text data for sentiment analysis."""
    csv_content = """id,review,rating
1,This product is amazing! I love it.,5
2,Terrible experience would not recommend.,1
3,It works fine nothing special.,3
4,Best purchase ever! Highly recommended.,5
5,Complete waste of money.,1"""
    return io.BytesIO(csv_content.encode())


@pytest.fixture
def sample_csv_no_text():
    """Create a sample CSV file without text data."""
    csv_content = """id,value,count
1,100,5
2,200,10
3,150,8"""
    return io.BytesIO(csv_content.encode())


class TestNLPAPI:
    """Test suite for NLP/sentiment analysis API."""

    def test_analyze_sentiment_success(self, sample_csv_with_text):
        """Test successful sentiment analysis."""
        # Upload file first
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("reviews.csv", sample_csv_with_text, "text/csv")}
        )
        assert upload_response.status_code == 200
        session_id = upload_response.json()["session_id"]

        # Run sentiment analysis
        response = client.post(
            f"/api/v1/dataset/{session_id}/sentiment",
            json={"target_column": "review"}
        )
        assert response.status_code == 200

        # Check response structure
        data = response.json()
        assert "columns" in data
        assert "preview" in data

        # Check that sentiment columns were added
        column_names = [col["name"] for col in data["columns"]]
        assert "review_sentiment" in column_names
        assert "review_sentiment_score" in column_names

    def test_sentiment_analysis_values(self, sample_csv_with_text):
        """Test that sentiment values are correctly computed."""
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("reviews.csv", sample_csv_with_text, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        response = client.post(
            f"/api/v1/dataset/{session_id}/sentiment",
            json={"target_column": "review"}
        )
        assert response.status_code == 200

        data = response.json()
        preview = data["preview"]

        # Check that sentiment values exist
        assert all("review_sentiment" in row for row in preview)
        assert all("review_sentiment_score" in row for row in preview)

        # Check that sentiments are valid labels
        valid_labels = ["POSITIVE", "NEGATIVE", "NEUTRAL"]
        for row in preview:
            assert row["review_sentiment"] in valid_labels

        # Check that scores are in valid range
        for row in preview:
            score = row["review_sentiment_score"]
            assert -1 <= score <= 1

    def test_analyze_sentiment_invalid_column(self, sample_csv_with_text):
        """Test sentiment analysis with non-existent column."""
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("reviews.csv", sample_csv_with_text, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        response = client.post(
            f"/api/v1/dataset/{session_id}/sentiment",
            json={"target_column": "nonexistent"}
        )
        assert response.status_code == 400
        assert "not found" in response.json()["detail"].lower()

    def test_analyze_sentiment_numeric_column(self, sample_csv_with_text):
        """Test sentiment analysis on numeric column (should fail)."""
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("reviews.csv", sample_csv_with_text, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        response = client.post(
            f"/api/v1/dataset/{session_id}/sentiment",
            json={"target_column": "rating"}
        )
        assert response.status_code == 400
        assert "string" in response.json()["detail"].lower()

    def test_analyze_sentiment_invalid_session(self):
        """Test sentiment analysis with invalid session ID."""
        response = client.post(
            "/api/v1/dataset/invalid-uuid/sentiment",
            json={"target_column": "text"}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_analyze_sentiment_nonexistent_session(self):
        """Test sentiment analysis with non-existent but valid UUID."""
        fake_uuid = "12345678-1234-1234-1234-123456789012"
        response = client.post(
            f"/api/v1/dataset/{fake_uuid}/sentiment",
            json={"target_column": "text"}
        )
        assert response.status_code == 404

    def test_sentiment_persists_in_session(self, sample_csv_with_text):
        """Test that sentiment analysis results persist in the session."""
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("reviews.csv", sample_csv_with_text, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        # Run sentiment analysis
        sentiment_response = client.post(
            f"/api/v1/dataset/{session_id}/sentiment",
            json={"target_column": "review"}
        )
        assert sentiment_response.status_code == 200

        # Retrieve dataset and check sentiment columns still exist
        get_response = client.get(f"/api/v1/dataset/{session_id}")
        assert get_response.status_code == 200

        data = get_response.json()
        column_names = [col["name"] for col in data["columns"]]
        assert "review_sentiment" in column_names
        assert "review_sentiment_score" in column_names

    def test_multiple_sentiment_analyses(self, sample_csv_with_text):
        """Test running sentiment analysis on the same column multiple times."""
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("reviews.csv", sample_csv_with_text, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        # Run sentiment analysis first time
        response1 = client.post(
            f"/api/v1/dataset/{session_id}/sentiment",
            json={"target_column": "review"}
        )
        assert response1.status_code == 200

        # Run sentiment analysis second time (should work or warn)
        response2 = client.post(
            f"/api/v1/dataset/{session_id}/sentiment",
            json={"target_column": "review"}
        )
        # Should succeed (may overwrite or skip)
        assert response2.status_code in [200, 400]

    def test_sentiment_request_format(self, sample_csv_with_text):
        """Test that sentiment request requires correct format."""
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("reviews.csv", sample_csv_with_text, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        # Test missing target_column
        response = client.post(
            f"/api/v1/dataset/{session_id}/sentiment",
            json={}
        )
        assert response.status_code == 422  # Validation error

    def test_sentiment_response_format(self, sample_csv_with_text):
        """Test that sentiment response has correct format."""
        upload_response = client.post(
            "/api/v1/upload",
            files={"file": ("reviews.csv", sample_csv_with_text, "text/csv")}
        )
        session_id = upload_response.json()["session_id"]

        response = client.post(
            f"/api/v1/dataset/{session_id}/sentiment",
            json={"target_column": "review"}
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        data = response.json()
        # Should return DatasetMetadata format
        assert "row_count" in data
        assert "column_count" in data
        assert "columns" in data
        assert "preview" in data
