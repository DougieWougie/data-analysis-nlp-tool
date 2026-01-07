# Feature Specification: Data Analysis & NLP Tool

**Feature Branch**: `001-nlp-data-viz`
**Created**: 2026-01-07
**Status**: Draft
**Input**: User description: "React application to analyse data from xls, xlsx, and csv. The application should allow us to select and clean columns before providing a range of suggested visualisations. Finally the application should implement nltk and implement sentiment analysis for any text fields."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Data Upload & Preview (Priority: P1)

As a Data Analyst, I want to upload spreadsheet files (Excel, CSV) and preview their contents so that I can verify the data before processing.

**Why this priority**: This is the entry point for the application; without data ingestion, no other features are possible.

**Independent Test**: Can be fully tested by uploading a valid .csv/.xlsx file and verifying the raw data table is displayed correctly.

**Acceptance Scenarios**:

1. **Given** the application is open, **When** I drag and drop a valid CSV file, **Then** the system parses the file and displays a preview table of the first 50 rows.
2. **Given** the application is open, **When** I upload an Excel (.xlsx) file with multiple sheets, **Then** the system prompts me to select which sheet to import.
3. **Given** I attempt to upload an unsupported file type (e.g., .pdf), **When** I confirm the upload, **Then** the system displays an error message "Unsupported file format".

---

### User Story 2 - Column Cleaning & Selection (Priority: P1)

As a Data Analyst, I want to select specific columns to analyze and perform basic cleaning operations (renaming, handling missing values) so that my analysis is based on high-quality data.

**Why this priority**: Raw data is rarely analysis-ready. This step ensures downstream visualizations and NLP are accurate.

**Independent Test**: Can be tested by uploading a dataset with nulls, applying a "drop rows" cleaning rule, and verifying the row count decreases.

**Acceptance Scenarios**:

1. **Given** a loaded dataset, **When** I uncheck specific columns in the sidebar, **Then** those columns are removed from the data preview and subsequent analysis.
2. **Given** a column with missing values, **When** I choose "Fill with Mean" for that column, **Then** all empty cells are populated with the calculated mean of the column.
3. **Given** a column with a confusing header, **When** I rename "col_1" to "Revenue", **Then** the header updates in the preview.

---

### User Story 3 - Automated Visualization Suggestions (Priority: P2)

As a Data Analyst, I want the system to suggest appropriate visualizations based on the selected data types so that I can quickly identify trends without manually configuring charts.

**Why this priority**: Provides the core "insight" value proposition, automating the manual work of chart selection.

**Independent Test**: Can be tested by selecting one numerical and one categorical column and verifying the system suggests a Bar Chart.

**Acceptance Scenarios**:

1. **Given** selected data includes one time-series column and one numerical column, **When** I request visualizations, **Then** the system suggests a Line Chart.
2. **Given** selected data includes two numerical columns, **When** I request visualizations, **Then** the system suggests a Scatter Plot.
3. **Given** the system generates a chart, **When** I hover over a data point, **Then** a tooltip displays the precise values.

---

### User Story 4 - Sentiment Analysis on Text (Priority: P2)

As a Data Analyst, I want to view sentiment scores for text columns so that I can understand the emotional tone of qualitative data (e.g., feedback, reviews).

**Why this priority**: Adds advanced analytical capability (NLP) requested specifically by the user.

**Independent Test**: Can be tested by uploading a file with a "Review" column containing "I love this product", and verifying the sentiment output is positive.

**Acceptance Scenarios**:

1. **Given** a dataset with text columns, **When** I click "Analyze Sentiment" for a specific column, **Then** the system adds a new column "Sentiment_Score" to the dataset.
2. **Given** the sentiment analysis is complete, **When** I view the summary, **Then** the system displays a distribution chart of Positive, Neutral, and Negative records.
3. **Given** a text field contains mixed language or symbols, **When** analysis runs, **Then** the system processes it without crashing, assigning a neutral score if undeterminable.

### Edge Cases

- What happens when an uploaded file is extremely large (>50MB)?
- How does the system handle columns with mixed data types (e.g., numbers and text in the same column)?
- What happens if the user selects a text column for a numerical visualization?
- How does the sentiment analyzer handle non-English text?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST support file imports for .csv, .xls, and .xlsx formats.
- **FR-002**: System MUST allow users to select a subset of columns to retain for the current analysis session.
- **FR-003**: System MUST provide data cleaning functions: Rename Column, Drop Missing Values, Fill Missing Values (Mean/Median/Zero), and Change Data Type.
- **FR-004**: System MUST automatically detect data types (Numerical, Categorical, DateTime, Text) for each column upon import.
- **FR-005**: System MUST generate at least 3 relevant visualization suggestions based on the data types of selected columns.
- **FR-006**: System MUST perform sentiment analysis on user-selected text columns, generating a polarity score (e.g., -1 to +1) or label (Positive/Negative).
- **FR-007**: System MUST allow users to export the cleaned data and analysis results (including sentiment scores) as a new CSV file.

### Key Entities

- **Dataset**: Represents the loaded file content, including raw rows and metadata (column types).
- **Transformation**: A specific cleaning or filtering action applied to the dataset (e.g., "Rename col A to B").
- **Visualization**: A chart object derived from the dataset, including type (Bar, Line) and mapping (x-axis, y-axis).
- **SentimentResult**: The output of the NLP process, linking a row ID to a sentiment score/label.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully upload and parse a 10MB CSV file in under 5 seconds.
- **SC-002**: 90% of generated visualization suggestions are valid for the underlying data type (e.g., no pie charts for time-series).
- **SC-003**: Users can complete a full "Import -> Clean -> Visualize" workflow in fewer than 10 clicks.
- **SC-004**: Sentiment analysis correctly identifies the tone of clear positive/negative benchmark phrases with >80% accuracy.