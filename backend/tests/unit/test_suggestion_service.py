"""Unit tests for the Suggestion Service."""
import pytest
import pandas as pd
from src.services.suggestion_service import SuggestionService
from src.models.visualization import VisualizationSuggestion, ChartType


@pytest.fixture
def suggestion_service():
    """Create a SuggestionService instance."""
    return SuggestionService()


@pytest.fixture
def sample_numeric_df():
    """Create a sample dataframe with numeric columns."""
    return pd.DataFrame({
        'sales': [100, 200, 150, 300, 250],
        'quantity': [5, 10, 8, 15, 12],
        'price': [20, 20, 18.75, 20, 20.83]
    })


@pytest.fixture
def sample_categorical_df():
    """Create a sample dataframe with categorical columns."""
    return pd.DataFrame({
        'category': ['A', 'B', 'A', 'C', 'B', 'A'],
        'region': ['North', 'South', 'North', 'East', 'South', 'West'],
        'count': [10, 20, 15, 25, 30, 5]
    })


@pytest.fixture
def sample_mixed_df():
    """Create a sample dataframe with mixed column types."""
    return pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=5),
        'sales': [100, 200, 150, 300, 250],
        'category': ['A', 'B', 'A', 'C', 'B'],
        'region': ['North', 'South', 'North', 'East', 'South']
    })


class TestSuggestionService:
    """Test suite for SuggestionService."""

    def test_generate_suggestions_numeric_columns(self, suggestion_service, sample_numeric_df):
        """Test that numeric columns generate appropriate chart suggestions."""
        suggestions = suggestion_service.generate_suggestions(sample_numeric_df)

        assert len(suggestions) > 0
        assert all(isinstance(s, VisualizationSuggestion) for s in suggestions)

        # Should suggest scatter plot for numeric vs numeric
        scatter_suggestions = [s for s in suggestions if s.type == ChartType.SCATTER]
        assert len(scatter_suggestions) > 0

        # Should suggest histograms for numeric distributions
        histogram_suggestions = [s for s in suggestions if s.type == ChartType.HISTOGRAM]
        assert len(histogram_suggestions) > 0

    def test_generate_suggestions_categorical_data(self, suggestion_service, sample_categorical_df):
        """Test that categorical data generates bar/pie chart suggestions."""
        suggestions = suggestion_service.generate_suggestions(sample_categorical_df)

        assert len(suggestions) > 0

        # Should suggest bar charts for categorical data
        bar_suggestions = [s for s in suggestions if s.type == ChartType.BAR]
        assert len(bar_suggestions) > 0

        # Should suggest pie charts for categorical distributions
        pie_suggestions = [s for s in suggestions if s.type == ChartType.PIE]
        assert len(pie_suggestions) > 0

    def test_generate_suggestions_time_series(self, suggestion_service, sample_mixed_df):
        """Test that datetime columns generate line chart suggestions."""
        suggestions = suggestion_service.generate_suggestions(sample_mixed_df)

        assert len(suggestions) > 0

        # Should suggest line charts for time series data
        line_suggestions = [s for s in suggestions if s.type == ChartType.LINE]
        assert len(line_suggestions) > 0

        # Check that datetime column is used as x_axis
        datetime_suggestions = [s for s in line_suggestions if s.x_axis == 'date']
        assert len(datetime_suggestions) > 0

    def test_generate_suggestions_empty_dataframe(self, suggestion_service):
        """Test that empty dataframe returns empty suggestions list."""
        empty_df = pd.DataFrame()
        suggestions = suggestion_service.generate_suggestions(empty_df)

        assert suggestions == []

    def test_generate_suggestions_single_column(self, suggestion_service):
        """Test suggestions for single column dataframe."""
        single_col_df = pd.DataFrame({'values': [1, 2, 3, 4, 5]})
        suggestions = suggestion_service.generate_suggestions(single_col_df)

        # Should at least suggest histogram for single numeric column
        assert len(suggestions) > 0
        histogram_suggestions = [s for s in suggestions if s.type == ChartType.HISTOGRAM]
        assert len(histogram_suggestions) > 0

    def test_suggestion_structure(self, suggestion_service, sample_numeric_df):
        """Test that suggestions have all required fields."""
        suggestions = suggestion_service.generate_suggestions(sample_numeric_df)

        for suggestion in suggestions:
            assert suggestion.type in ChartType
            assert isinstance(suggestion.title, str)
            assert len(suggestion.title) > 0
            assert isinstance(suggestion.description, str)
            assert len(suggestion.description) > 0
            # x_axis and y_axis can be None for some chart types like PIE

    def test_max_suggestions_limit(self, suggestion_service):
        """Test that the service doesn't return too many suggestions."""
        # Create a dataframe with many columns
        large_df = pd.DataFrame({f'col_{i}': range(10) for i in range(20)})
        suggestions = suggestion_service.generate_suggestions(large_df)

        # Should limit suggestions to a reasonable number (e.g., 10)
        assert len(suggestions) <= 10

    def test_suggestions_are_relevant(self, suggestion_service, sample_categorical_df):
        """Test that suggestions make sense for the data types."""
        suggestions = suggestion_service.generate_suggestions(sample_categorical_df)

        # For categorical data, should not suggest scatter plots
        for suggestion in suggestions:
            if suggestion.type == ChartType.SCATTER:
                # If scatter is suggested, at least one axis should be numeric
                numeric_cols = ['count']
                assert suggestion.x_axis in numeric_cols or suggestion.y_axis in numeric_cols
