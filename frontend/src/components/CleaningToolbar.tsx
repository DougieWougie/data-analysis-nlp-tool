/**
 * Cleaning toolbar with actions for data manipulation
 */
import { useState } from 'react';

interface Column {
  name: string;
  data_type: string;
  missing_count: number;
}

interface CleaningToolbarProps {
  columns: Column[];
  onFillNA: (column: string, strategy: string, value?: any) => void;
  onDropNA: (columns?: string[]) => void;
  onExport?: () => void;
}

const CleaningToolbar = ({ columns, onFillNA, onDropNA, onExport }: CleaningToolbarProps) => {
  const [selectedColumn, setSelectedColumn] = useState<string>('');
  const [fillStrategy, setFillStrategy] = useState<string>('mean');
  const [fillValue, setFillValue] = useState<string>('');

  const handleFillNA = () => {
    if (!selectedColumn) {
      alert('Please select a column');
      return;
    }

    const column = columns.find((c) => c.name === selectedColumn);
    if (!column || column.missing_count === 0) {
      alert('Selected column has no missing values');
      return;
    }

    if (fillStrategy === 'constant' && !fillValue) {
      alert('Please enter a fill value');
      return;
    }

    onFillNA(selectedColumn, fillStrategy, fillStrategy === 'constant' ? fillValue : undefined);
    setSelectedColumn('');
    setFillValue('');
  };

  const handleDropNA = () => {
    if (confirm('Drop all rows with missing values?')) {
      onDropNA();
    }
  };

  const columnsWithNA = columns.filter((col) => col.missing_count > 0);

  return (
    <div className="cleaning-toolbar">
      <div className="toolbar-section">
        <h4>Fill Missing Values</h4>
        <div className="fill-na-form">
          <select
            value={selectedColumn}
            onChange={(e) => setSelectedColumn(e.target.value)}
            className="select-input"
          >
            <option value="">Select column...</option>
            {columnsWithNA.map((col) => (
              <option key={col.name} value={col.name}>
                {col.name} ({col.missing_count} missing)
              </option>
            ))}
          </select>

          <select
            value={fillStrategy}
            onChange={(e) => setFillStrategy(e.target.value)}
            className="select-input"
          >
            <option value="mean">Mean</option>
            <option value="median">Median</option>
            <option value="mode">Mode</option>
            <option value="constant">Constant</option>
          </select>

          {fillStrategy === 'constant' && (
            <input
              type="text"
              value={fillValue}
              onChange={(e) => setFillValue(e.target.value)}
              placeholder="Fill value"
              className="text-input"
            />
          )}

          <button onClick={handleFillNA} className="btn-primary" disabled={!selectedColumn}>
            Fill NA
          </button>
        </div>
      </div>

      <div className="toolbar-section">
        <h4>Data Actions</h4>
        <div className="action-buttons">
          <button onClick={handleDropNA} className="btn-warning">
            Drop Rows with NA
          </button>
          {onExport && (
            <button onClick={onExport} className="btn-success">
              Export CSV
            </button>
          )}
        </div>
      </div>

      <style>{`
        .cleaning-toolbar {
          background-color: white;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .toolbar-section h4 {
          margin: 0 0 1rem 0;
          font-size: 1rem;
          color: #2d3748;
          font-weight: 600;
        }

        .fill-na-form {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          align-items: center;
        }

        .select-input,
        .text-input {
          padding: 0.5rem 0.75rem;
          border: 1px solid #cbd5e0;
          border-radius: 4px;
          font-size: 0.9rem;
          min-width: 150px;
          flex: 1;
        }

        .select-input:focus,
        .text-input:focus {
          outline: none;
          border-color: #4299e1;
          box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
        }

        .action-buttons {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
        }

        button {
          padding: 0.65rem 1.25rem;
          border: none;
          border-radius: 4px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
          font-size: 0.9rem;
        }

        button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .btn-primary {
          background-color: #4299e1;
          color: white;
        }

        .btn-primary:hover:not(:disabled) {
          background-color: #3182ce;
        }

        .btn-warning {
          background-color: #ed8936;
          color: white;
        }

        .btn-warning:hover {
          background-color: #dd6b20;
        }

        .btn-success {
          background-color: #48bb78;
          color: white;
        }

        .btn-success:hover {
          background-color: #38a169;
        }

        @media (max-width: 768px) {
          .fill-na-form {
            flex-direction: column;
            align-items: stretch;
          }

          .select-input,
          .text-input {
            width: 100%;
          }

          button {
            width: 100%;
          }
        }
      `}</style>
    </div>
  );
};

export default CleaningToolbar;
