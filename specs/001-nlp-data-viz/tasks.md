# Tasks: Data Analysis & NLP Tool

**Input**: Design documents from `/specs/001-nlp-data-viz/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are **MANDATORY** per the Constitution (Principle IV).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure (src/api, src/models, src/services, src/utils, tests)
- [X] T002 Initialize Python environment (venv) and install dependencies (fastapi, uvicorn, pandas, openpyxl, nltk, python-multipart, pytest)
- [X] T003 Initialize frontend React project with Vite (TypeScript)
- [X] T004 [P] Install frontend dependencies (axios, recharts, vitest, @testing-library/react)
- [X] T005 [P] Configure backend linting/formatting (black, pylint)
- [X] T006 [P] Configure frontend linting/formatting (eslint, prettier)

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Implement Session Management Service (generate UUIDs, create temp dirs) in backend/src/services/session_service.py
- [X] T008 Implement File Storage Utility (save/load/delete files) in backend/src/utils/file_manager.py
- [X] T009 Define core Pydantic models (AnalysisSession, DatasetMetadata, ColumnMetadata) in backend/src/models/core.py
- [X] T010 Setup global exception handling and logging in backend/src/app.py
- [X] T011 [P] Create basic API client setup in frontend/src/services/api.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

## Phase 3: User Story 1 - Data Upload & Preview (Priority: P1) 🎯 MVP

**Goal**: Enable users to upload CSV/Excel files and view a data preview.

**Independent Test**: Upload a valid CSV, verify response contains metadata and preview rows.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T012 [P] [US1] Create unit test for file parsing service in backend/tests/unit/test_parsing_service.py
- [X] T013 [P] [US1] Create integration test for /upload endpoint in backend/tests/integration/test_upload_api.py
- [X] T014 [P] [US1] Create component test for FileUpload component in frontend/tests/components/FileUpload.test.tsx

### Implementation for User Story 1

- [X] T015 [US1] Implement Data Parsing Service (read_csv/excel, extract metadata) in backend/src/services/parsing_service.py
- [X] T016 [US1] Implement /upload endpoint in backend/src/api/routes.py (using UploadResponse model)
- [X] T017 [US1] Implement /dataset/{session_id} endpoint in backend/src/api/routes.py
- [X] T018 [P] [US1] Create FileUpload component (drag & drop zone) in frontend/src/components/FileUpload.tsx
- [X] T019 [P] [US1] Create DataPreviewTable component in frontend/src/components/DataPreviewTable.tsx
- [X] T020 [US1] Integrate Upload and Preview components in frontend/src/pages/Dashboard.tsx
- [X] T021 [US1] Handle error states (invalid file type, parse errors) in frontend/src/components/FileUpload.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

## Phase 4: User Story 2 - Column Cleaning & Selection (Priority: P1)

**Goal**: Allow users to select columns and perform basic cleaning operations.

**Independent Test**: Upload data, drop a column via API/UI, verify it's gone in the preview.

### Tests for User Story 2 ⚠️

- [X] T022 [P] [US2] Create unit test for cleaning operations (drop, fillna, rename) in backend/tests/unit/test_cleaning_service.py
- [X] T023 [P] [US2] Create integration test for /clean endpoint in backend/tests/integration/test_clean_api.py
- [X] T024 [P] [US2] Create component test for ColumnSelector component in frontend/tests/components/ColumnSelector.test.tsx

### Implementation for User Story 2

- [X] T025 [US2] Define CleaningOperation model in backend/src/models/cleaning.py
- [X] T026 [US2] Implement Cleaning Service (apply transformations to pandas DF) in backend/src/services/cleaning_service.py
- [X] T027 [US2] Implement /dataset/{session_id}/clean endpoint in backend/src/api/routes.py
- [X] T028 [P] [US2] Create ColumnSelector sidebar component in frontend/src/components/ColumnSelector.tsx
- [X] T029 [P] [US2] Create CleaningToolbar component (rename, fill NA actions) in frontend/src/components/CleaningToolbar.tsx
- [X] T030 [US2] Wire up cleaning actions to API in frontend/src/pages/Dashboard.tsx
- [X] T031 [US2] Implement state refresh logic (re-fetch preview after clean) in frontend/src/hooks/useDataset.ts

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

## Phase 5: User Story 3 - Automated Visualization Suggestions (Priority: P2)

**Goal**: Suggest and render charts based on data types.

**Independent Test**: Upload data with numerical columns, request suggestions, verify Bar/Scatter chart response.

### Tests for User Story 3 ⚠️

- [ ] T032 [P] [US3] Create unit test for suggestion logic (heuristic rules) in backend/tests/unit/test_suggestion_service.py
- [ ] T033 [P] [US3] Create integration test for /suggestions endpoint in backend/tests/integration/test_suggestions_api.py
- [ ] T034 [P] [US3] Create component test for ChartRenderer in frontend/tests/components/ChartRenderer.test.tsx

### Implementation for User Story 3

- [ ] T035 [US3] Define VisualizationSuggestion model in backend/src/models/visualization.py
- [ ] T036 [US3] Implement Suggestion Service (generate configs based on column types) in backend/src/services/suggestion_service.py
- [ ] T037 [US3] Implement /dataset/{session_id}/suggestions endpoint in backend/src/api/routes.py
- [ ] T038 [P] [US3] Create ChartRenderer component (using Recharts) in frontend/src/components/ChartRenderer.tsx
- [ ] T039 [P] [US3] Create SuggestionsPanel component (list of recommended charts) in frontend/src/components/SuggestionsPanel.tsx
- [ ] T040 [US3] Implement chart selection and rendering logic in frontend/src/pages/Dashboard.tsx

**Checkpoint**: All user stories should now be independently functional

## Phase 6: User Story 4 - Sentiment Analysis on Text (Priority: P2)

**Goal**: Analyze text columns for sentiment using NLTK.

**Independent Test**: Upload text data, run sentiment analysis, verify new column with scores.

### Tests for User Story 4 ⚠️

- [ ] T041 [P] [US4] Create unit test for NLTK sentiment wrapper in backend/tests/unit/test_nlp_service.py
- [ ] T042 [P] [US4] Create integration test for /sentiment endpoint in backend/tests/integration/test_nlp_api.py
- [ ] T043 [P] [US4] Create component test for SentimentAnalysisAction in frontend/tests/components/SentimentAction.test.tsx

### Implementation for User Story 4

- [ ] T044 [US4] Implement NLP Service (VADER initialization, apply to column) in backend/src/services/nlp_service.py
- [ ] T045 [US4] Implement /dataset/{session_id}/sentiment endpoint in backend/src/api/routes.py
- [ ] T046 [US4] Implement /dataset/{session_id}/export endpoint for downloading results in backend/src/api/routes.py
- [ ] T047 [P] [US4] Add "Analyze Sentiment" button to column headers in frontend/src/components/DataPreviewTable.tsx
- [ ] T048 [P] [US4] Create SentimentDistributionChart component in frontend/src/components/SentimentDistributionChart.tsx
- [ ] T049 [US4] Add Export button to UI in frontend/src/components/CleaningToolbar.tsx

**Checkpoint**: Full feature set complete.

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T050 [P] Update Quickstart guide with any new setup steps in specs/001-nlp-data-viz/quickstart.md
- [ ] T051 Refactor backend routes to use APIRouter for better organization
- [ ] T052 Optimize Recharts rendering for larger datasets (memoization)
- [ ] T053 [P] Add global loading states/spinners in frontend/src/components/LoadingOverlay.tsx
- [ ] T054 [P] Implement proper error toast notifications in frontend/src/App.tsx
- [ ] T055 Run final end-to-end manual test of full workflow (Upload -> Clean -> Analyze -> Visualize -> Export)

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all stories
- **User Stories (Phase 3+)**: All depend on Foundational
  - US1 (Upload) is effectively a prerequisite for using the app, though US2/3/4 code can be written in parallel, integration requires US1.
  - US2 (Clean) modifies data state, affecting US3/US4.
  - US3 (Viz) and US4 (NLP) can run in parallel.
- **Polish (Phase 7)**: Depends on all user stories

### User Story Dependencies

- **US1 (Upload)**: Independent start.
- **US2 (Clean)**: Independent code, integrates with US1 data.
- **US3 (Viz)**: Independent code, integrates with US1/US2 data.
- **US4 (NLP)**: Independent code, integrates with US1/US2 data.

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 & 2
2. Complete Phase 3 (US1)
3. **STOP and VALIDATE**: Can we upload and see data? (Yes -> MVP achieved)

### Incremental Delivery

1. Foundation ready
2. Add US1 -> Deploy to internal test
3. Add US2 -> Update deployment
4. Add US3 & US4 -> Final Feature Release
