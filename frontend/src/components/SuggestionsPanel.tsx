/**
 * SuggestionsPanel component for displaying visualization recommendations
 */
import { useState } from 'react';

interface VisualizationSuggestion {
  type: 'BAR' | 'LINE' | 'SCATTER' | 'PIE' | 'HISTOGRAM';
  title: string;
  x_axis?: string;
  y_axis?: string;
  description: string;
}

interface SuggestionsPanelProps {
  suggestions: VisualizationSuggestion[];
  onSelectSuggestion: (suggestion: VisualizationSuggestion) => void;
  loading?: boolean;
}

const getChartIcon = (type: string) => {
  switch (type) {
    case 'BAR':
      return '📊';
    case 'LINE':
      return '📈';
    case 'SCATTER':
      return '🔵';
    case 'PIE':
      return '🥧';
    case 'HISTOGRAM':
      return '📉';
    default:
      return '📊';
  }
};

const SuggestionsPanel = ({ suggestions, onSelectSuggestion, loading }: SuggestionsPanelProps) => {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);

  const handleSuggestionClick = (suggestion: VisualizationSuggestion, index: number) => {
    setSelectedIndex(index);
    onSelectSuggestion(suggestion);
  };

  if (loading) {
    return (
      <div className="suggestions-panel">
        <h3 className="panel-title">Visualization Suggestions</h3>
        <div className="loading-state">
          <p>Analyzing your data...</p>
        </div>
      </div>
    );
  }

  if (!suggestions || suggestions.length === 0) {
    return (
      <div className="suggestions-panel">
        <h3 className="panel-title">Visualization Suggestions</h3>
        <div className="empty-state">
          <p>No suggestions available. Upload data to see visualization recommendations.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="suggestions-panel">
      <h3 className="panel-title">Visualization Suggestions</h3>
      <p className="panel-subtitle">Click on a suggestion to visualize your data</p>

      <div className="suggestions-list">
        {suggestions.map((suggestion, index) => (
          <div
            key={index}
            className={`suggestion-card ${selectedIndex === index ? 'selected' : ''}`}
            onClick={() => handleSuggestionClick(suggestion, index)}
          >
            <div className="suggestion-icon">{getChartIcon(suggestion.type)}</div>
            <div className="suggestion-content">
              <div className="suggestion-header">
                <span className="suggestion-type">{suggestion.type}</span>
                <h4 className="suggestion-title">{suggestion.title}</h4>
              </div>
              <p className="suggestion-description">{suggestion.description}</p>
              {suggestion.x_axis && suggestion.y_axis && (
                <div className="suggestion-axes">
                  <span className="axis-label">
                    X: <strong>{suggestion.x_axis}</strong>
                  </span>
                  <span className="axis-separator">→</span>
                  <span className="axis-label">
                    Y: <strong>{suggestion.y_axis}</strong>
                  </span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <style>{`
        .suggestions-panel {
          background: white;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .panel-title {
          font-size: 1.25rem;
          font-weight: 600;
          color: #2d3748;
          margin: 0 0 0.5rem 0;
        }

        .panel-subtitle {
          font-size: 0.9rem;
          color: #718096;
          margin: 0 0 1.5rem 0;
        }

        .loading-state,
        .empty-state {
          text-align: center;
          padding: 2rem;
          color: #718096;
        }

        .suggestions-list {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }

        .suggestion-card {
          display: flex;
          gap: 1rem;
          padding: 1rem;
          border: 2px solid #e2e8f0;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .suggestion-card:hover {
          border-color: #667eea;
          box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
          transform: translateY(-2px);
        }

        .suggestion-card.selected {
          border-color: #667eea;
          background-color: #f7fafc;
          box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
        }

        .suggestion-icon {
          font-size: 2rem;
          display: flex;
          align-items: center;
          justify-content: center;
          width: 3rem;
          height: 3rem;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border-radius: 8px;
          flex-shrink: 0;
        }

        .suggestion-content {
          flex: 1;
        }

        .suggestion-header {
          margin-bottom: 0.5rem;
        }

        .suggestion-type {
          display: inline-block;
          font-size: 0.75rem;
          font-weight: 600;
          color: #667eea;
          background: #e9ecfe;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          margin-bottom: 0.25rem;
        }

        .suggestion-title {
          font-size: 1rem;
          font-weight: 600;
          color: #2d3748;
          margin: 0.25rem 0 0 0;
        }

        .suggestion-description {
          font-size: 0.875rem;
          color: #718096;
          margin: 0.5rem 0 0 0;
          line-height: 1.5;
        }

        .suggestion-axes {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-top: 0.75rem;
          padding-top: 0.75rem;
          border-top: 1px solid #e2e8f0;
          font-size: 0.875rem;
          color: #4a5568;
        }

        .axis-label strong {
          color: #2d3748;
        }

        .axis-separator {
          color: #cbd5e0;
        }

        @media (max-width: 768px) {
          .suggestion-card {
            flex-direction: column;
            text-align: center;
          }

          .suggestion-icon {
            margin: 0 auto;
          }

          .suggestion-axes {
            flex-direction: column;
            gap: 0.25rem;
          }

          .axis-separator {
            display: none;
          }
        }
      `}</style>
    </div>
  );
};

export default SuggestionsPanel;
