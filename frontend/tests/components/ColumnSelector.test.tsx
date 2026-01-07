/**
 * Component tests for ColumnSelector component
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ColumnSelector from '../../src/components/ColumnSelector';

const mockColumns = [
  { name: 'name', data_type: 'Text', missing_count: 0 },
  { name: 'age', data_type: 'Numerical', missing_count: 1 },
  { name: 'score', data_type: 'Numerical', missing_count: 0 },
  { name: 'city', data_type: 'Categorical', missing_count: 0 },
];

describe('ColumnSelector Component', () => {
  it('should render all columns', () => {
    const mockOnDrop = vi.fn();
    const mockOnRename = vi.fn();

    render(<ColumnSelector columns={mockColumns} onDropColumn={mockOnDrop} onRenameColumn={mockOnRename} />);

    expect(screen.getByText('name')).toBeInTheDocument();
    expect(screen.getByText('age')).toBeInTheDocument();
    expect(screen.getByText('score')).toBeInTheDocument();
    expect(screen.getByText('city')).toBeInTheDocument();
  });

  it('should show data types for each column', () => {
    const mockOnDrop = vi.fn();
    const mockOnRename = vi.fn();

    render(<ColumnSelector columns={mockColumns} onDropColumn={mockOnDrop} onRenameColumn={mockOnRename} />);

    expect(screen.getByText(/text/i)).toBeInTheDocument();
    expect(screen.getAllByText(/numerical/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/categorical/i)).toBeInTheDocument();
  });

  it('should show missing count for columns with missing values', () => {
    const mockOnDrop = vi.fn();
    const mockOnRename = vi.fn();

    render(<ColumnSelector columns={mockColumns} onDropColumn={mockOnDrop} onRenameColumn={mockOnRename} />);

    expect(screen.getByText(/1 missing/i)).toBeInTheDocument();
  });

  it('should call onDropColumn when drop button is clicked', async () => {
    const mockOnDrop = vi.fn();
    const mockOnRename = vi.fn();
    const user = userEvent.setup();

    render(<ColumnSelector columns={mockColumns} onDropColumn={mockOnDrop} onRenameColumn={mockOnRename} />);

    const dropButtons = screen.getAllByRole('button', { name: /drop|delete|remove/i });
    await user.click(dropButtons[0]);

    expect(mockOnDrop).toHaveBeenCalledWith('name');
  });

  it('should call onRenameColumn when rename is submitted', async () => {
    const mockOnDrop = vi.fn();
    const mockOnRename = vi.fn();
    const user = userEvent.setup();

    render(<ColumnSelector columns={mockColumns} onDropColumn={mockOnDrop} onRenameColumn={mockOnRename} />);

    // Find and click rename button
    const renameButtons = screen.getAllByRole('button', { name: /rename|edit/i });
    await user.click(renameButtons[0]);

    // Find input and type new name
    const input = screen.getByRole('textbox');
    await user.clear(input);
    await user.type(input, 'full_name');

    // Submit
    const submitButton = screen.getByRole('button', { name: /save|confirm|ok/i });
    await user.click(submitButton);

    expect(mockOnRename).toHaveBeenCalledWith('name', 'full_name');
  });

  it('should show column count', () => {
    const mockOnDrop = vi.fn();
    const mockOnRename = vi.fn();

    render(<ColumnSelector columns={mockColumns} onDropColumn={mockOnDrop} onRenameColumn={mockOnRename} />);

    expect(screen.getByText(/4 columns/i)).toBeInTheDocument();
  });

  it('should handle empty columns list', () => {
    const mockOnDrop = vi.fn();
    const mockOnRename = vi.fn();

    render(<ColumnSelector columns={[]} onDropColumn={mockOnDrop} onRenameColumn={mockOnRename} />);

    expect(screen.getByText(/no columns|0 columns/i)).toBeInTheDocument();
  });
});
