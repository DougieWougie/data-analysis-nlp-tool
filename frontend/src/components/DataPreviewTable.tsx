/**
 * Data preview table component
 */
interface Column {
  name: string;
  data_type: string;
  missing_count: number;
}

interface DataPreviewTableProps {
  columns: Column[];
  preview: Record<string, any>[];
  rowCount: number;
}

const DataPreviewTable = ({ columns, preview, rowCount }: DataPreviewTableProps) => {
  if (!columns || columns.length === 0) {
    return null;
  }

  return (
    <div className="data-preview-container">
      <div className="preview-header">
        <h2>Data Preview</h2>
        <p className="row-info">
          Showing first {preview.length} of {rowCount} rows
        </p>
      </div>

      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col.name}>
                  <div className="column-header">
                    <span className="column-name">{col.name}</span>
                    <span className="column-type">{col.data_type}</span>
                    {col.missing_count > 0 && (
                      <span className="missing-badge">{col.missing_count} missing</span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {preview.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {columns.map((col) => (
                  <td key={`${rowIndex}-${col.name}`}>
                    {row[col.name] !== null && row[col.name] !== undefined
                      ? String(row[col.name])
                      : <span className="null-value">null</span>}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <style>{`
        .data-preview-container {
          width: 100%;
          margin: 2rem 0;
        }

        .preview-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }

        .preview-header h2 {
          margin: 0;
          font-size: 1.5rem;
          color: #2d3748;
        }

        .row-info {
          color: #718096;
          font-size: 0.9rem;
          margin: 0;
        }

        .table-wrapper {
          overflow-x: auto;
          border: 1px solid #e2e8f0;
          border-radius: 8px;
          background-color: white;
        }

        .data-table {
          width: 100%;
          border-collapse: collapse;
          font-size: 0.9rem;
        }

        .data-table thead {
          background-color: #f7fafc;
          position: sticky;
          top: 0;
        }

        .data-table th {
          padding: 1rem;
          text-align: left;
          border-bottom: 2px solid #e2e8f0;
          font-weight: 600;
        }

        .column-header {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .column-name {
          color: #2d3748;
          font-size: 0.95rem;
        }

        .column-type {
          color: #718096;
          font-size: 0.75rem;
          font-weight: normal;
          text-transform: capitalize;
        }

        .missing-badge {
          display: inline-block;
          padding: 0.15rem 0.5rem;
          background-color: #fed7d7;
          color: #c53030;
          border-radius: 12px;
          font-size: 0.7rem;
          font-weight: 500;
        }

        .data-table td {
          padding: 0.75rem 1rem;
          border-bottom: 1px solid #e2e8f0;
          color: #4a5568;
        }

        .data-table tbody tr:hover {
          background-color: #f7fafc;
        }

        .data-table tbody tr:last-child td {
          border-bottom: none;
        }

        .null-value {
          color: #a0aec0;
          font-style: italic;
        }

        @media (max-width: 768px) {
          .table-wrapper {
            max-height: 500px;
            overflow-y: auto;
          }

          .data-table {
            font-size: 0.8rem;
          }

          .data-table th,
          .data-table td {
            padding: 0.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default DataPreviewTable;
