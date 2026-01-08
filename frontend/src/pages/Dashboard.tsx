/**
 * Main dashboard page
 */
import { useState, useEffect } from 'react';
import FileUpload from '../components/FileUpload';
import DataPreviewTable from '../components/DataPreviewTable';
import ColumnSelector from '../components/ColumnSelector';
import CleaningToolbar from '../components/CleaningToolbar';
import SuggestionsPanel from '../components/SuggestionsPanel';
import ChartRenderer from '../components/ChartRenderer';
import SentimentDistributionChart from '../components/SentimentDistributionChart';
import { useDataset } from '../hooks/useDataset';
import api from '../services/api';

interface DatasetMetadata {
  row_count: number;
  column_count: number;
  columns: Array<{
    name: string;
    data_type: string;
    missing_count: number;
  }>;
  preview: Record<string, any>[];
}

interface VisualizationSuggestion {
  type: 'BAR' | 'LINE' | 'SCATTER' | 'PIE' | 'HISTOGRAM';
  title: string;
  x_axis?: string;
  y_axis?: string;
  description: string;
}

const Dashboard = () => {
  const {
    sessionId,
    setSessionId,
    metadata,
    setMetadata,
    loading,
    error,
    dropColumn,
    renameColumn,
    fillNA,
    dropNA,
    castType,
  } = useDataset();

  const [suggestions, setSuggestions] = useState<VisualizationSuggestion[]>([]);
  const [selectedSuggestion, setSelectedSuggestion] = useState<VisualizationSuggestion | null>(null);
  const [suggestionsLoading, setSuggestionsLoading] = useState(false);

  // Fetch suggestions when session changes
  useEffect(() => {
    if (sessionId) {
      fetchSuggestions();
    }
  }, [sessionId, metadata]); // Re-fetch when metadata changes (after cleaning)

  const fetchSuggestions = async () => {
    if (!sessionId) return;

    setSuggestionsLoading(true);
    try {
      const response = await api.get(`/api/v1/dataset/${sessionId}/suggestions`);
      setSuggestions(response.data);
    } catch (err) {
      console.error('Failed to fetch suggestions:', err);
      setSuggestions([]);
    } finally {
      setSuggestionsLoading(false);
    }
  };

  const handleUploadSuccess = (newSessionId: string, newMetadata: DatasetMetadata) => {
    setSessionId(newSessionId);
    setMetadata(newMetadata);
  };

  const handleUploadError = (error: string) => {
    console.error('Upload error:', error);
  };

  const handleDropColumn = async (columnName: string) => {
    try {
      await dropColumn(columnName);
    } catch (err) {
      console.error('Failed to drop column:', err);
    }
  };

  const handleRenameColumn = async (oldName: string, newName: string) => {
    try {
      await renameColumn(oldName, newName);
    } catch (err) {
      console.error('Failed to rename column:', err);
    }
  };

  const handleFillNA = async (column: string, strategy: string, value?: any) => {
    try {
      await fillNA(column, strategy, value);
    } catch (err) {
      console.error('Failed to fill NA:', err);
    }
  };

  const handleDropNA = async () => {
    try {
      await dropNA();
    } catch (err) {
      console.error('Failed to drop NA rows:', err);
    }
  };

  const handleChangeType = async (columnName: string, newType: string) => {
    try {
      await castType(columnName, newType);
    } catch (err) {
      console.error('Failed to change column type:', err);
    }
  };

  const handleExport = async () => {
    if (!sessionId) return;

    try {
      const response = await api.get(`/api/v1/dataset/${sessionId}/export`, {
        responseType: 'blob',
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'cleaned_dataset.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Failed to export:', err);
    }
  };

  const handleAnalyzeSentiment = async (columnName: string) => {
    if (!sessionId) return;

    try {
      const response = await api.post(`/api/v1/dataset/${sessionId}/sentiment`, {
        target_column: columnName
      });

      // Update metadata with the new sentiment columns
      setMetadata(response.data);
    } catch (err) {
      console.error('Failed to analyze sentiment:', err);
    }
  };

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Data Analysis & NLP Tool</h1>
        <p>Upload your CSV or Excel file to get started</p>
      </header>

      <main className="dashboard-content">
        <FileUpload onUpload={handleUploadSuccess} onError={handleUploadError} />

        {loading && (
          <div className="loading-overlay">
            <p>Processing...</p>
          </div>
        )}

        {error && (
          <div className="error-banner">
            <p>{error}</p>
          </div>
        )}

        {metadata && (
          <>
            <div className="dataset-info">
              <div className="info-card">
                <span className="info-label">Total Rows</span>
                <span className="info-value">{metadata.row_count.toLocaleString()}</span>
              </div>
              <div className="info-card">
                <span className="info-label">Columns</span>
                <span className="info-value">{metadata.column_count}</span>
              </div>
              {sessionId && (
                <div className="info-card">
                  <span className="info-label">Session ID</span>
                  <span className="info-value session-id">{sessionId.substring(0, 8)}...</span>
                </div>
              )}
            </div>

            <div className="workspace">
              <aside className="sidebar">
                <ColumnSelector
                  columns={metadata.columns}
                  onDropColumn={handleDropColumn}
                  onRenameColumn={handleRenameColumn}
                  onChangeType={handleChangeType}
                />
                <CleaningToolbar
                  columns={metadata.columns}
                  onFillNA={handleFillNA}
                  onDropNA={handleDropNA}
                  onExport={handleExport}
                />
                <SuggestionsPanel
                  suggestions={suggestions}
                  onSelectSuggestion={setSelectedSuggestion}
                  loading={suggestionsLoading}
                />
              </aside>

              <main className="main-content">
                {selectedSuggestion && (
                  <div className="visualization-section">
                    <ChartRenderer
                      suggestion={selectedSuggestion}
                      data={metadata.preview}
                    />
                  </div>
                )}

                {/* Show sentiment distribution if sentiment columns exist */}
                {metadata.columns.some(col => col.name.endsWith('_sentiment')) && (
                  <SentimentDistributionChart
                    data={metadata.preview}
                    sentimentColumn={metadata.columns.find(col => col.name.endsWith('_sentiment'))!.name}
                  />
                )}

                <DataPreviewTable
                  columns={metadata.columns}
                  preview={metadata.preview}
                  rowCount={metadata.row_count}
                  onAnalyzeSentiment={handleAnalyzeSentiment}
                />
              </main>
            </div>
          </>
        )}
      </main>

      <style>{`
        .dashboard {
          min-height: 100vh;
          background-color: #f7fafc;
        }

        .dashboard-header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 3rem 2rem;
          text-align: center;
        }

        .dashboard-header h1 {
          margin: 0 0 0.5rem 0;
          font-size: 2.5rem;
          font-weight: 700;
        }

        .dashboard-header p {
          margin: 0;
          font-size: 1.1rem;
          opacity: 0.9;
        }

        .dashboard-content {
          max-width: 1400px;
          margin: 0 auto;
          padding: 2rem;
        }

        .loading-overlay {
          text-align: center;
          padding: 2rem;
          background-color: #edf2f7;
          border-radius: 8px;
          margin: 2rem 0;
        }

        .error-banner {
          padding: 1rem;
          background-color: #fed7d7;
          color: #c53030;
          border-radius: 8px;
          margin: 2rem 0;
        }

        .dataset-info {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1.5rem;
          margin: 2rem 0;
        }

        .info-card {
          background-color: white;
          padding: 1.5rem;
          border-radius: 8px;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }

        .info-label {
          color: #718096;
          font-size: 0.9rem;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .info-value {
          color: #2d3748;
          font-size: 1.75rem;
          font-weight: 600;
        }

        .session-id {
          font-size: 1.2rem;
          font-family: monospace;
        }

        .workspace {
          display: grid;
          grid-template-columns: 350px 1fr;
          gap: 2rem;
          margin-top: 2rem;
        }

        .sidebar {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .main-content {
          min-width: 0;
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }

        .visualization-section {
          background: white;
          border-radius: 8px;
          padding: 0;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        @media (max-width: 1024px) {
          .workspace {
            grid-template-columns: 1fr;
          }
        }

        @media (max-width: 768px) {
          .dashboard-header h1 {
            font-size: 1.75rem;
          }

          .dashboard-content {
            padding: 1rem;
          }

          .dataset-info {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default Dashboard;
