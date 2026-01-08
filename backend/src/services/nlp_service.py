"""Service for performing NLP tasks including sentiment analysis."""
import pandas as pd
import logging
from typing import Dict, Any
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)


class NLPService:
    """Service for NLP operations using NLTK."""

    def __init__(self):
        """Initialize the NLP service with VADER sentiment analyzer."""
        try:
            # Ensure VADER lexicon is downloaded
            nltk.data.find('sentiment/vader_lexicon.zip')
        except LookupError:
            logger.info("Downloading VADER lexicon...")
            nltk.download('vader_lexicon', quiet=True)

        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self, df: pd.DataFrame, target_column: str) -> pd.DataFrame:
        """
        Perform sentiment analysis on a text column in the dataframe.

        Args:
            df: The pandas DataFrame containing the text data
            target_column: Name of the column containing text to analyze

        Returns:
            DataFrame with added sentiment columns:
                - {target_column}_sentiment: Label (POSITIVE/NEGATIVE/NEUTRAL)
                - {target_column}_sentiment_score: Compound score (-1 to 1)

        Raises:
            ValueError: If target_column doesn't exist or isn't text type
        """
        # Validate column exists
        if target_column not in df.columns:
            raise ValueError(f"Column '{target_column}' not found in dataframe")

        # Validate column is text type
        if df[target_column].dtype not in ['object', 'string']:
            raise ValueError(f"Column '{target_column}' must be of type string/text, got {df[target_column].dtype}")

        # Create a copy to avoid modifying original
        result_df = df.copy()

        # Analyze sentiment for each row
        sentiments = []
        scores = []

        for value in result_df[target_column]:
            if pd.isna(value) or value == '':
                # Handle missing/empty values
                sentiments.append('NEUTRAL')
                scores.append(0.0)
            else:
                # Get sentiment scores
                sentiment_dict = self.sentiment_analyzer.polarity_scores(str(value))
                compound_score = sentiment_dict['compound']

                # Classify sentiment based on compound score
                if compound_score >= 0.05:
                    label = 'POSITIVE'
                elif compound_score <= -0.05:
                    label = 'NEGATIVE'
                else:
                    label = 'NEUTRAL'

                sentiments.append(label)
                scores.append(compound_score)

        # Add sentiment columns to dataframe
        sentiment_col = f"{target_column}_sentiment"
        score_col = f"{target_column}_sentiment_score"

        result_df[sentiment_col] = sentiments
        result_df[score_col] = scores

        logger.info(f"Sentiment analysis completed for column '{target_column}'. "
                   f"Added columns: {sentiment_col}, {score_col}")

        return result_df

    def get_sentiment_distribution(self, df: pd.DataFrame, sentiment_column: str) -> Dict[str, Any]:
        """
        Get distribution statistics for a sentiment column.

        Args:
            df: DataFrame containing sentiment results
            sentiment_column: Name of the sentiment label column

        Returns:
            Dictionary with sentiment distribution statistics
        """
        if sentiment_column not in df.columns:
            raise ValueError(f"Sentiment column '{sentiment_column}' not found")

        distribution = df[sentiment_column].value_counts().to_dict()

        return {
            'distribution': distribution,
            'total': len(df),
            'positive_percentage': (distribution.get('POSITIVE', 0) / len(df)) * 100,
            'negative_percentage': (distribution.get('NEGATIVE', 0) / len(df)) * 100,
            'neutral_percentage': (distribution.get('NEUTRAL', 0) / len(df)) * 100,
        }
