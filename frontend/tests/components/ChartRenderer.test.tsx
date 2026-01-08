/**
 * Component tests for ChartRenderer
 */
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import ChartRenderer from '../../src/components/ChartRenderer';

describe('ChartRenderer', () => {
  const mockData = [
    { name: 'A', value: 100 },
    { name: 'B', value: 200 },
    { name: 'C', value: 150 },
  ];

  it('renders bar chart with provided data', () => {
    const suggestion = {
      type: 'BAR' as const,
      title: 'Sales by Category',
      x_axis: 'name',
      y_axis: 'value',
      description: 'Bar chart showing sales',
    };

    render(<ChartRenderer suggestion={suggestion} data={mockData} />);

    expect(screen.getByText('Sales by Category')).toBeInTheDocument();
  });

  it('renders line chart with provided data', () => {
    const suggestion = {
      type: 'LINE' as const,
      title: 'Sales Over Time',
      x_axis: 'name',
      y_axis: 'value',
      description: 'Line chart showing trend',
    };

    render(<ChartRenderer suggestion={suggestion} data={mockData} />);

    expect(screen.getByText('Sales Over Time')).toBeInTheDocument();
  });

  it('renders scatter chart with provided data', () => {
    const scatterData = [
      { x: 10, y: 20 },
      { x: 15, y: 25 },
      { x: 20, y: 30 },
    ];

    const suggestion = {
      type: 'SCATTER' as const,
      title: 'Correlation Analysis',
      x_axis: 'x',
      y_axis: 'y',
      description: 'Scatter plot',
    };

    render(<ChartRenderer suggestion={suggestion} data={scatterData} />);

    expect(screen.getByText('Correlation Analysis')).toBeInTheDocument();
  });

  it('renders pie chart with provided data', () => {
    const suggestion = {
      type: 'PIE' as const,
      title: 'Distribution',
      x_axis: 'name',
      y_axis: 'value',
      description: 'Pie chart showing distribution',
    };

    render(<ChartRenderer suggestion={suggestion} data={mockData} />);

    expect(screen.getByText('Distribution')).toBeInTheDocument();
  });

  it('renders histogram with provided data', () => {
    const histogramData = [
      { bin: '0-10', count: 5 },
      { bin: '10-20', count: 10 },
      { bin: '20-30', count: 8 },
    ];

    const suggestion = {
      type: 'HISTOGRAM' as const,
      title: 'Value Distribution',
      x_axis: 'bin',
      y_axis: 'count',
      description: 'Histogram',
    };

    render(<ChartRenderer suggestion={suggestion} data={histogramData} />);

    expect(screen.getByText('Value Distribution')).toBeInTheDocument();
  });

  it('handles empty data gracefully', () => {
    const suggestion = {
      type: 'BAR' as const,
      title: 'Empty Chart',
      x_axis: 'name',
      y_axis: 'value',
      description: 'No data available',
    };

    render(<ChartRenderer suggestion={suggestion} data={[]} />);

    expect(screen.getByText('Empty Chart')).toBeInTheDocument();
  });

  it('displays chart description', () => {
    const suggestion = {
      type: 'BAR' as const,
      title: 'Test Chart',
      x_axis: 'name',
      y_axis: 'value',
      description: 'This is a test description',
    };

    render(<ChartRenderer suggestion={suggestion} data={mockData} />);

    expect(screen.getByText('This is a test description')).toBeInTheDocument();
  });

  it('renders with correct dimensions', () => {
    const suggestion = {
      type: 'BAR' as const,
      title: 'Test Chart',
      x_axis: 'name',
      y_axis: 'value',
      description: 'Test',
    };

    const { container } = render(
      <ChartRenderer suggestion={suggestion} data={mockData} width={600} height={400} />
    );

    // Check that the chart container exists
    expect(container.querySelector('.chart-container')).toBeInTheDocument();
  });

  it('applies custom styling when provided', () => {
    const suggestion = {
      type: 'BAR' as const,
      title: 'Styled Chart',
      x_axis: 'name',
      y_axis: 'value',
      description: 'Custom styled chart',
    };

    const { container } = render(
      <ChartRenderer
        suggestion={suggestion}
        data={mockData}
        className="custom-chart-class"
      />
    );

    expect(container.querySelector('.custom-chart-class')).toBeInTheDocument();
  });
});
