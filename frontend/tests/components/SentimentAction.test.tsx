/**
 * Component tests for Sentiment Analysis Action
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import DataPreviewTable from '../../src/components/DataPreviewTable';

describe('SentimentAnalysisAction', () => {
  const mockColumns = [
    { name: 'id', data_type: 'Numerical', missing_count: 0 },
    { name: 'review', data_type: 'Text', missing_count: 0 },
    { name: 'rating', data_type: 'Numerical', missing_count: 0 },
  ];

  const mockPreview = [
    { id: 1, review: 'Great product!', rating: 5 },
    { id: 2, review: 'Not good', rating: 2 },
    { id: 3, review: 'Average', rating: 3 },
  ];

  it('renders table with columns and data', () => {
    render(
      <DataPreviewTable
        columns={mockColumns}
        preview={mockPreview}
        rowCount={3}
      />
    );

    expect(screen.getByText('id')).toBeInTheDocument();
    expect(screen.getByText('review')).toBeInTheDocument();
    expect(screen.getByText('rating')).toBeInTheDocument();
  });

  it('displays correct row count', () => {
    render(
      <DataPreviewTable
        columns={mockColumns}
        preview={mockPreview}
        rowCount={100}
      />
    );

    expect(screen.getByText(/showing 3 of 100 rows/i)).toBeInTheDocument();
  });

  it('renders data preview rows', () => {
    render(
      <DataPreviewTable
        columns={mockColumns}
        preview={mockPreview}
        rowCount={3}
      />
    );

    expect(screen.getByText('Great product!')).toBeInTheDocument();
    expect(screen.getByText('Not good')).toBeInTheDocument();
    expect(screen.getByText('Average')).toBeInTheDocument();
  });

  it('handles empty preview data', () => {
    render(
      <DataPreviewTable
        columns={mockColumns}
        preview={[]}
        rowCount={0}
      />
    );

    expect(screen.getByText('id')).toBeInTheDocument();
    expect(screen.getByText('review')).toBeInTheDocument();
  });

  it('displays correct data types for columns', () => {
    render(
      <DataPreviewTable
        columns={mockColumns}
        preview={mockPreview}
        rowCount={3}
      />
    );

    expect(screen.getByText(/Numerical/i)).toBeInTheDocument();
    expect(screen.getByText(/Text/i)).toBeInTheDocument();
  });

  it('shows missing count when present', () => {
    const columnsWithMissing = [
      { name: 'id', data_type: 'Numerical', missing_count: 0 },
      { name: 'review', data_type: 'Text', missing_count: 5 },
    ];

    render(
      <DataPreviewTable
        columns={columnsWithMissing}
        preview={mockPreview}
        rowCount={3}
      />
    );

    expect(screen.getByText(/5 missing/i)).toBeInTheDocument();
  });

  it('handles numeric values correctly', () => {
    render(
      <DataPreviewTable
        columns={mockColumns}
        preview={mockPreview}
        rowCount={3}
      />
    );

    expect(screen.getByText('1')).toBeInTheDocument();
    expect(screen.getByText('5')).toBeInTheDocument();
    expect(screen.getByText('2')).toBeInTheDocument();
  });

  it('renders table in scrollable container', () => {
    const { container } = render(
      <DataPreviewTable
        columns={mockColumns}
        preview={mockPreview}
        rowCount={3}
      />
    );

    const tableContainer = container.querySelector('.table-container');
    expect(tableContainer).toBeInTheDocument();
  });
});
