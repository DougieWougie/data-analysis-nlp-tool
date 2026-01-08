"""Service for generating visualization suggestions based on data analysis."""
import pandas as pd
from typing import List
import logging

from src.models.visualization import VisualizationSuggestion, ChartType

logger = logging.getLogger(__name__)


class SuggestionService:
    """Service for analyzing data and generating chart suggestions."""

    MAX_SUGGESTIONS = 10

    def __init__(self):
        """Initialize the suggestion service."""
        pass

    def generate_suggestions(self, df: pd.DataFrame) -> List[VisualizationSuggestion]:
        """
        Generate visualization suggestions based on dataframe column types and content.

        Args:
            df: The pandas DataFrame to analyze

        Returns:
            List of VisualizationSuggestion objects

        Strategy:
            - Identify column types (numeric, categorical, datetime, text)
            - Apply heuristic rules to suggest appropriate visualizations
            - Prioritize most useful/common visualizations
        """
        if df.empty or len(df.columns) == 0:
            return []

        suggestions = []

        # Analyze column types
        numeric_cols = self._get_numeric_columns(df)
        categorical_cols = self._get_categorical_columns(df)
        datetime_cols = self._get_datetime_columns(df)

        # Generate suggestions based on column types
        suggestions.extend(self._suggest_histograms(df, numeric_cols))
        suggestions.extend(self._suggest_scatter_plots(df, numeric_cols))
        suggestions.extend(self._suggest_bar_charts(df, categorical_cols, numeric_cols))
        suggestions.extend(self._suggest_pie_charts(df, categorical_cols, numeric_cols))
        suggestions.extend(self._suggest_line_charts(df, datetime_cols, numeric_cols))

        # Limit to MAX_SUGGESTIONS
        return suggestions[:self.MAX_SUGGESTIONS]

    def _get_numeric_columns(self, df: pd.DataFrame) -> List[str]:
        """Get list of numeric column names."""
        return df.select_dtypes(include=['number']).columns.tolist()

    def _get_categorical_columns(self, df: pd.DataFrame) -> List[str]:
        """Get list of categorical column names."""
        categorical = []
        for col in df.columns:
            if df[col].dtype == 'object' or df[col].dtype.name == 'category':
                # Consider it categorical if it has reasonable number of unique values
                if df[col].nunique() <= 20:
                    categorical.append(col)
        return categorical

    def _get_datetime_columns(self, df: pd.DataFrame) -> List[str]:
        """Get list of datetime column names."""
        datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()

        # Also check for columns that might be parseable as dates
        for col in df.select_dtypes(include=['object']).columns:
            if col not in datetime_cols:
                try:
                    pd.to_datetime(df[col].head(10))
                    datetime_cols.append(col)
                except:
                    pass

        return datetime_cols

    def _suggest_histograms(self, df: pd.DataFrame, numeric_cols: List[str]) -> List[VisualizationSuggestion]:
        """Suggest histogram visualizations for numeric columns."""
        suggestions = []
        for col in numeric_cols[:3]:  # Limit to first 3 numeric columns
            suggestions.append(VisualizationSuggestion(
                type=ChartType.HISTOGRAM,
                title=f"Distribution of {col}",
                x_axis=col,
                y_axis="count",
                description=f"Histogram showing the distribution of values in {col}"
            ))
        return suggestions

    def _suggest_scatter_plots(self, df: pd.DataFrame, numeric_cols: List[str]) -> List[VisualizationSuggestion]:
        """Suggest scatter plots for pairs of numeric columns."""
        suggestions = []

        # Generate scatter plots for first few numeric column pairs
        if len(numeric_cols) >= 2:
            # Take up to 2 pairs to avoid too many suggestions
            for i in range(min(2, len(numeric_cols) - 1)):
                x_col = numeric_cols[i]
                y_col = numeric_cols[i + 1]

                suggestions.append(VisualizationSuggestion(
                    type=ChartType.SCATTER,
                    title=f"{y_col} vs {x_col}",
                    x_axis=x_col,
                    y_axis=y_col,
                    description=f"Scatter plot showing relationship between {x_col} and {y_col}"
                ))

        return suggestions

    def _suggest_bar_charts(self, df: pd.DataFrame, categorical_cols: List[str],
                           numeric_cols: List[str]) -> List[VisualizationSuggestion]:
        """Suggest bar charts for categorical vs numeric data."""
        suggestions = []

        if categorical_cols and numeric_cols:
            # Suggest bar chart for first categorical column with first numeric column
            cat_col = categorical_cols[0]
            num_col = numeric_cols[0]

            suggestions.append(VisualizationSuggestion(
                type=ChartType.BAR,
                title=f"{num_col} by {cat_col}",
                x_axis=cat_col,
                y_axis=num_col,
                description=f"Bar chart comparing {num_col} across different {cat_col} categories"
            ))

        # If only categorical, suggest count-based bar chart
        elif categorical_cols and not numeric_cols:
            cat_col = categorical_cols[0]
            suggestions.append(VisualizationSuggestion(
                type=ChartType.BAR,
                title=f"Count by {cat_col}",
                x_axis=cat_col,
                y_axis="count",
                description=f"Bar chart showing frequency of each {cat_col} category"
            ))

        return suggestions

    def _suggest_pie_charts(self, df: pd.DataFrame, categorical_cols: List[str],
                           numeric_cols: List[str]) -> List[VisualizationSuggestion]:
        """Suggest pie charts for categorical distributions."""
        suggestions = []

        if categorical_cols:
            cat_col = categorical_cols[0]
            # Only suggest pie chart if there aren't too many categories
            if df[cat_col].nunique() <= 8:
                if numeric_cols:
                    num_col = numeric_cols[0]
                    suggestions.append(VisualizationSuggestion(
                        type=ChartType.PIE,
                        title=f"{num_col} Distribution by {cat_col}",
                        x_axis=cat_col,
                        y_axis=num_col,
                        description=f"Pie chart showing proportion of {num_col} by {cat_col}"
                    ))
                else:
                    suggestions.append(VisualizationSuggestion(
                        type=ChartType.PIE,
                        title=f"{cat_col} Distribution",
                        x_axis=cat_col,
                        y_axis="count",
                        description=f"Pie chart showing distribution of {cat_col} categories"
                    ))

        return suggestions

    def _suggest_line_charts(self, df: pd.DataFrame, datetime_cols: List[str],
                            numeric_cols: List[str]) -> List[VisualizationSuggestion]:
        """Suggest line charts for time series data."""
        suggestions = []

        if datetime_cols and numeric_cols:
            date_col = datetime_cols[0]

            # Suggest line chart for first 2 numeric columns over time
            for num_col in numeric_cols[:2]:
                suggestions.append(VisualizationSuggestion(
                    type=ChartType.LINE,
                    title=f"{num_col} Over Time",
                    x_axis=date_col,
                    y_axis=num_col,
                    description=f"Line chart showing trend of {num_col} over {date_col}"
                ))

        return suggestions
