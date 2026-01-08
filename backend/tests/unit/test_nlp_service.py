"""Unit tests for the NLP Service."""
import pytest
import pandas as pd
from src.services.nlp_service import NLPService


@pytest.fixture
def nlp_service():
    """Create an NLPService instance."""
    return NLPService()


@pytest.fixture
def sample_text_df():
    """Create a sample dataframe with text data."""
    return pd.DataFrame({
        'review': [
            'This product is amazing! I love it.',
            'Terrible experience, would not recommend.',
            'It works fine, nothing special.',
            'Best purchase ever! Highly recommended.',
            'Complete waste of money.',
        ]
    })


@pytest.fixture
def sample_mixed_df():
    """Create a sample dataframe with mixed data types."""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'comment': [
            'Great service!',
            'Not happy with this.',
            'Average experience.'
        ],
        'rating': [5, 2, 3]
    })


class TestNLPService:
    """Test suite for NLPService."""

    def test_analyze_sentiment_basic(self, nlp_service, sample_text_df):
        """Test basic sentiment analysis on text column."""
        result_df = nlp_service.analyze_sentiment(sample_text_df, 'review')

        # Check that sentiment columns were added
        assert 'review_sentiment' in result_df.columns
        assert 'review_sentiment_score' in result_df.columns

        # Check that all rows have sentiment values
        assert result_df['review_sentiment'].notna().all()
        assert result_df['review_sentiment_score'].notna().all()

        # Check that scores are in valid range [-1, 1]
        assert (result_df['review_sentiment_score'] >= -1).all()
        assert (result_df['review_sentiment_score'] <= 1).all()

    def test_sentiment_labels(self, nlp_service, sample_text_df):
        """Test that sentiment labels are correctly assigned."""
        result_df = nlp_service.analyze_sentiment(sample_text_df, 'review')

        # Get sentiments
        sentiments = result_df['review_sentiment'].tolist()

        # Check that sentiments are valid labels
        valid_labels = ['POSITIVE', 'NEGATIVE', 'NEUTRAL']
        assert all(s in valid_labels for s in sentiments)

        # First review should be positive (amazing, love)
        assert result_df.iloc[0]['review_sentiment'] == 'POSITIVE'

        # Second review should be negative (terrible)
        assert result_df.iloc[1]['review_sentiment'] == 'NEGATIVE'

    def test_sentiment_scores_correlation(self, nlp_service, sample_text_df):
        """Test that sentiment scores correlate with labels."""
        result_df = nlp_service.analyze_sentiment(sample_text_df, 'review')

        for idx, row in result_df.iterrows():
            label = row['review_sentiment']
            score = row['review_sentiment_score']

            if label == 'POSITIVE':
                assert score > 0.05
            elif label == 'NEGATIVE':
                assert score < -0.05
            elif label == 'NEUTRAL':
                assert -0.05 <= score <= 0.05

    def test_analyze_sentiment_mixed_data(self, nlp_service, sample_mixed_df):
        """Test sentiment analysis on dataframe with multiple columns."""
        result_df = nlp_service.analyze_sentiment(sample_mixed_df, 'comment')

        # Original columns should still exist
        assert 'id' in result_df.columns
        assert 'comment' in result_df.columns
        assert 'rating' in result_df.columns

        # Sentiment columns should be added
        assert 'comment_sentiment' in result_df.columns
        assert 'comment_sentiment_score' in result_df.columns

        # Original data should be unchanged
        assert result_df['id'].tolist() == [1, 2, 3]
        assert result_df['rating'].tolist() == [5, 2, 3]

    def test_analyze_sentiment_invalid_column(self, nlp_service, sample_text_df):
        """Test that analyzing non-existent column raises error."""
        with pytest.raises(ValueError, match="Column 'nonexistent' not found"):
            nlp_service.analyze_sentiment(sample_text_df, 'nonexistent')

    def test_analyze_sentiment_empty_strings(self, nlp_service):
        """Test sentiment analysis with empty strings."""
        df = pd.DataFrame({
            'text': ['Good product', '', 'Bad product', None, 'Okay']
        })

        result_df = nlp_service.analyze_sentiment(df, 'text')

        # Should handle empty/null values
        assert 'text_sentiment' in result_df.columns
        assert 'text_sentiment_score' in result_df.columns

    def test_analyze_sentiment_preserves_order(self, nlp_service, sample_text_df):
        """Test that sentiment analysis preserves row order."""
        original_reviews = sample_text_df['review'].tolist()
        result_df = nlp_service.analyze_sentiment(sample_text_df, 'review')

        # Check that row order is preserved
        assert result_df['review'].tolist() == original_reviews

    def test_analyze_sentiment_numeric_column(self, nlp_service, sample_mixed_df):
        """Test that analyzing numeric column raises appropriate error."""
        with pytest.raises(ValueError, match="must be of type string"):
            nlp_service.analyze_sentiment(sample_mixed_df, 'rating')

    def test_sentiment_column_names(self, nlp_service, sample_text_df):
        """Test that sentiment column names follow expected pattern."""
        result_df = nlp_service.analyze_sentiment(sample_text_df, 'review')

        # Check column naming convention
        assert 'review_sentiment' in result_df.columns
        assert 'review_sentiment_score' in result_df.columns

        # Test with different column name
        df2 = pd.DataFrame({'feedback': ['Great!', 'Bad!']})
        result_df2 = nlp_service.analyze_sentiment(df2, 'feedback')

        assert 'feedback_sentiment' in result_df2.columns
        assert 'feedback_sentiment_score' in result_df2.columns

    def test_sentiment_consistency(self, nlp_service):
        """Test that same text produces same sentiment result."""
        df = pd.DataFrame({
            'text': ['This is excellent!', 'This is excellent!']
        })

        result_df = nlp_service.analyze_sentiment(df, 'text')

        # Same text should produce same sentiment
        assert result_df.iloc[0]['text_sentiment'] == result_df.iloc[1]['text_sentiment']
        assert result_df.iloc[0]['text_sentiment_score'] == result_df.iloc[1]['text_sentiment_score']
