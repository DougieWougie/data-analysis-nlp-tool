/**
 * Column selector sidebar component
 */
import { useState } from 'react';

interface Column {
  name: string;
  data_type: string;
  missing_count: number;
}

interface ColumnSelectorProps {
  columns: Column[];
  onDropColumn: (columnName: string) => void;
  onRenameColumn: (oldName: string, newName: string) => void;
  onChangeType?: (columnName: string, newType: string) => void;
}

const ColumnSelector = ({ columns, onDropColumn, onRenameColumn, onChangeType }: ColumnSelectorProps) => {
  const [renamingColumn, setRenamingColumn] = useState<string | null>(null);
  const [newName, setNewName] = useState('');
  const [changingTypeColumn, setChangingTypeColumn] = useState<string | null>(null);

  const dataTypes = ['Numerical', 'Categorical', 'DateTime', 'Text', 'Boolean'];

  const handleRenameClick = (columnName: string) => {
    setRenamingColumn(columnName);
    setNewName(columnName);
  };

  const handleRenameSubmit = (oldName: string) => {
    if (newName && newName !== oldName) {
      onRenameColumn(oldName, newName);
    }
    setRenamingColumn(null);
    setNewName('');
  };

  const handleRenameCancel = () => {
    setRenamingColumn(null);
    setNewName('');
  };

  const handleTypeChange = (columnName: string, newType: string) => {
    if (onChangeType) {
      onChangeType(columnName, newType);
    }
    setChangingTypeColumn(null);
  };

  if (columns.length === 0) {
    return (
      <div className="column-selector">
        <h3>Columns</h3>
        <p className="no-columns">No columns available</p>
      </div>
    );
  }

  return (
    <div className="column-selector">
      <div className="selector-header">
        <h3>Columns</h3>
        <span className="column-count">{columns.length} columns</span>
      </div>

      <div className="column-list">
        {columns.map((column) => (
          <div key={column.name} className="column-item">
            {renamingColumn === column.name ? (
              <div className="rename-form">
                <input
                  type="text"
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleRenameSubmit(column.name);
                    if (e.key === 'Escape') handleRenameCancel();
                  }}
                  autoFocus
                  aria-label="Rename column"
                />
                <button
                  onClick={() => handleRenameSubmit(column.name)}
                  className="btn-confirm"
                  aria-label="Save"
                >
                  ✓
                </button>
                <button onClick={handleRenameCancel} className="btn-cancel" aria-label="Cancel">
                  ✕
                </button>
              </div>
            ) : (
              <>
                <div className="column-info">
                  <span className="column-name">{column.name}</span>
                  {changingTypeColumn === column.name ? (
                    <select
                      className="type-selector"
                      value={column.data_type}
                      onChange={(e) => handleTypeChange(column.name, e.target.value)}
                      autoFocus
                      onBlur={() => setChangingTypeColumn(null)}
                    >
                      {dataTypes.map((type) => (
                        <option key={type} value={type}>
                          {type}
                        </option>
                      ))}
                    </select>
                  ) : (
                    <button
                      className="column-type-btn"
                      onClick={() => onChangeType && setChangingTypeColumn(column.name)}
                      title="Click to change data type"
                      disabled={!onChangeType}
                    >
                      {column.data_type}
                    </button>
                  )}
                  {column.missing_count > 0 && (
                    <span className="missing-badge">{column.missing_count} missing</span>
                  )}
                </div>
                <div className="column-actions">
                  <button
                    onClick={() => handleRenameClick(column.name)}
                    className="btn-action"
                    title="Rename column"
                    aria-label="Rename column"
                  >
                    ✏️
                  </button>
                  <button
                    onClick={() => onDropColumn(column.name)}
                    className="btn-action btn-danger"
                    title="Drop column"
                    aria-label="Drop column"
                  >
                    🗑️
                  </button>
                </div>
              </>
            )}
          </div>
        ))}
      </div>

      <style>{`
        .column-selector {
          background-color: white;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          max-height: 600px;
          overflow-y: auto;
        }

        .selector-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
          padding-bottom: 1rem;
          border-bottom: 2px solid #e2e8f0;
        }

        .selector-header h3 {
          margin: 0;
          font-size: 1.25rem;
          color: #2d3748;
        }

        .column-count {
          background-color: #edf2f7;
          padding: 0.25rem 0.75rem;
          border-radius: 12px;
          font-size: 0.875rem;
          color: #4a5568;
          font-weight: 500;
        }

        .no-columns {
          text-align: center;
          color: #a0aec0;
          padding: 2rem;
        }

        .column-list {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .column-item {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem;
          border: 1px solid #e2e8f0;
          border-radius: 6px;
          transition: all 0.2s;
        }

        .column-item:hover {
          border-color: #cbd5e0;
          box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .column-info {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          flex: 1;
        }

        .column-name {
          font-weight: 600;
          color: #2d3748;
          font-size: 0.95rem;
        }

        .column-type-btn {
          font-size: 0.8rem;
          color: #718096;
          text-transform: capitalize;
          background: none;
          border: 1px solid transparent;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          cursor: pointer;
          transition: all 0.2s;
          text-align: left;
        }

        .column-type-btn:hover:not(:disabled) {
          background-color: #edf2f7;
          border-color: #cbd5e0;
          color: #4299e1;
        }

        .column-type-btn:disabled {
          cursor: default;
        }

        .type-selector {
          font-size: 0.8rem;
          padding: 0.25rem 0.5rem;
          border: 1px solid #4299e1;
          border-radius: 4px;
          background-color: #ebf8ff;
          color: #2d3748;
          cursor: pointer;
          text-transform: capitalize;
        }

        .type-selector:focus {
          outline: none;
          box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
        }

        .missing-badge {
          display: inline-block;
          padding: 0.15rem 0.5rem;
          background-color: #fed7d7;
          color: #c53030;
          border-radius: 12px;
          font-size: 0.7rem;
          font-weight: 500;
          width: fit-content;
        }

        .column-actions {
          display: flex;
          gap: 0.5rem;
        }

        .btn-action {
          background: none;
          border: 1px solid #e2e8f0;
          padding: 0.5rem;
          border-radius: 4px;
          cursor: pointer;
          transition: all 0.2s;
          font-size: 1rem;
        }

        .btn-action:hover {
          background-color: #f7fafc;
          border-color: #cbd5e0;
        }

        .btn-danger:hover {
          background-color: #fff5f5;
          border-color: #fc8181;
        }

        .rename-form {
          display: flex;
          gap: 0.5rem;
          width: 100%;
        }

        .rename-form input {
          flex: 1;
          padding: 0.5rem;
          border: 1px solid #cbd5e0;
          border-radius: 4px;
          font-size: 0.9rem;
        }

        .rename-form input:focus {
          outline: none;
          border-color: #4299e1;
          box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
        }

        .btn-confirm,
        .btn-cancel {
          padding: 0.5rem 0.75rem;
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-weight: 600;
          transition: all 0.2s;
        }

        .btn-confirm {
          background-color: #48bb78;
          color: white;
        }

        .btn-confirm:hover {
          background-color: #38a169;
        }

        .btn-cancel {
          background-color: #e2e8f0;
          color: #4a5568;
        }

        .btn-cancel:hover {
          background-color: #cbd5e0;
        }
      `}</style>
    </div>
  );
};

export default ColumnSelector;
