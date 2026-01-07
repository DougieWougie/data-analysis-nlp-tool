/**
 * Component tests for FileUpload component
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import FileUpload from '../../src/components/FileUpload';

describe('FileUpload Component', () => {
  it('should render upload zone', () => {
    const mockOnUpload = vi.fn();
    render(<FileUpload onUpload={mockOnUpload} />);

    expect(screen.getByText(/drag.*drop/i)).toBeInTheDocument();
  });

  it('should accept CSV files', async () => {
    const mockOnUpload = vi.fn();
    const user = userEvent.setup();
    render(<FileUpload onUpload={mockOnUpload} />);

    const file = new File(['name,age\nAlice,25'], 'test.csv', { type: 'text/csv' });
    const input = screen.getByLabelText(/upload/i) || screen.getByRole('button');

    await user.upload(input, file);

    expect(mockOnUpload).toHaveBeenCalled();
  });

  it('should accept Excel files', async () => {
    const mockOnUpload = vi.fn();
    const user = userEvent.setup();
    render(<FileUpload onUpload={mockOnUpload} />);

    const file = new File(['dummy'], 'test.xlsx', {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    });
    const input = screen.getByLabelText(/upload/i) || screen.getByRole('button');

    await user.upload(input, file);

    expect(mockOnUpload).toHaveBeenCalled();
  });

  it('should show error for invalid file type', async () => {
    const mockOnUpload = vi.fn();
    const mockOnError = vi.fn();
    const user = userEvent.setup();
    render(<FileUpload onUpload={mockOnUpload} onError={mockOnError} />);

    const file = new File(['content'], 'test.txt', { type: 'text/plain' });
    const input = screen.getByLabelText(/upload/i) || screen.getByRole('button');

    await user.upload(input, file);

    expect(mockOnError).toHaveBeenCalled();
    expect(mockOnUpload).not.toHaveBeenCalled();
  });

  it('should show loading state during upload', async () => {
    const mockOnUpload = vi.fn(() => new Promise((resolve) => setTimeout(resolve, 100)));
    const user = userEvent.setup();
    render(<FileUpload onUpload={mockOnUpload} />);

    const file = new File(['name,age\nAlice,25'], 'test.csv', { type: 'text/csv' });
    const input = screen.getByLabelText(/upload/i) || screen.getByRole('button');

    await user.upload(input, file);

    expect(screen.getByText(/uploading|loading/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.queryByText(/uploading|loading/i)).not.toBeInTheDocument();
    });
  });

  it('should display error message when upload fails', async () => {
    const mockOnUpload = vi.fn(() => Promise.reject(new Error('Upload failed')));
    const user = userEvent.setup();
    render(<FileUpload onUpload={mockOnUpload} />);

    const file = new File(['name,age\nAlice,25'], 'test.csv', { type: 'text/csv' });
    const input = screen.getByLabelText(/upload/i) || screen.getByRole('button');

    await user.upload(input, file);

    await waitFor(() => {
      expect(screen.getByText(/error|failed/i)).toBeInTheDocument();
    });
  });
});
