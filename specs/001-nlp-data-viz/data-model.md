# Data Model: Data Analysis & NLP Tool

**Feature**: Data Analysis & NLP Tool
**Status**: Design
**Source**: Derived from `specs/001-nlp-data-viz/spec.md`

## Entities

### 1. AnalysisSession
Represents a user's current interaction context.
- **id**: UUID (Primary Key)
- **created_at**: DateTime
- **file_path**: String (Path to temporary storage of the current CSV/Excel file)
- **original_filename**: String

### 2. DatasetMetadata
Summary information about the current state of the data.
- **row_count**: Integer
- **column_count**: Integer
- **columns**: List[ColumnMetadata]
- **preview**: List[Dict] (First 50 rows as JSON objects)

### 3. ColumnMetadata
- **name**: String
- **original_name**: String (to track renames)
- **data_type**: Enum (Numeric, Categorical, DateTime, Text, Boolean)
- **missing_count**: Integer

### 4. CleaningOperation
A transformation to apply to the dataset.
- **type**: Enum
    - `DROP_COLUMNS`
    - `RENAME_COLUMN`
    - `DROP_NA`
    - `FILL_NA` (mean, median, mode, constant)
    - `CAST_TYPE`
- **params**: Dict (Specific arguments for the operation, e.g., `{"columns": ["col1"], "value": 0}`)

### 5. VisualizationSuggestion
A recommended chart configuration.
- **type**: Enum (BAR, LINE, SCATTER, PIE, HISTOGRAM)
- **title**: String
- **x_axis**: String (Column Name)
- **y_axis**: String (Column Name)
- **description**: String (Why this was suggested)

### 6. SentimentResult
The outcome of NLP analysis.
- **column_name**: String
- **scores**: List[RowScore]

### 7. RowScore
- **row_index**: Integer
- **compound_score**: Float (-1.0 to 1.0)
- **label**: Enum (POSITIVE, NEUTRAL, NEGATIVE)

## State Transitions

1.  **Upload**: Creates `AnalysisSession`, saves initial file.
2.  **Clean**: Reads file -> Applies Pandas operations -> Overwrites file (or saves version) -> Returns new `DatasetMetadata`.
3.  **Analyze**: Reads file -> Computes Sentiment -> Appends new column "sentiment_{col}" -> Overwrites file -> Returns `DatasetMetadata` (with new column).
