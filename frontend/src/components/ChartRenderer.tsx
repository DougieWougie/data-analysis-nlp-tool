/**
 * ChartRenderer component for rendering various chart types using Recharts
 */
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  ScatterChart,
  Scatter,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface VisualizationSuggestion {
  type: 'BAR' | 'LINE' | 'SCATTER' | 'PIE' | 'HISTOGRAM';
  title: string;
  x_axis?: string;
  y_axis?: string;
  description: string;
}

interface ChartRendererProps {
  suggestion: VisualizationSuggestion;
  data: any[];
  width?: number;
  height?: number;
  className?: string;
}

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#fee140', '#30cfd0'];

const ChartRenderer = ({ suggestion, data, width, height, className }: ChartRendererProps) => {
  const renderChart = () => {
    const chartHeight = height || 400;
    const chartWidth = width || 600;

    switch (suggestion.type) {
      case 'BAR':
        return (
          <ResponsiveContainer width="100%" height={chartHeight}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={suggestion.x_axis || 'name'} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey={suggestion.y_axis || 'value'} fill="#667eea" />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'LINE':
        return (
          <ResponsiveContainer width="100%" height={chartHeight}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={suggestion.x_axis || 'name'} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey={suggestion.y_axis || 'value'}
                stroke="#667eea"
                strokeWidth={2}
              />
            </LineChart>
          </ResponsiveContainer>
        );

      case 'SCATTER':
        return (
          <ResponsiveContainer width="100%" height={chartHeight}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={suggestion.x_axis || 'x'} name={suggestion.x_axis || 'X'} />
              <YAxis dataKey={suggestion.y_axis || 'y'} name={suggestion.y_axis || 'Y'} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Legend />
              <Scatter name={suggestion.title} data={data} fill="#667eea" />
            </ScatterChart>
          </ResponsiveContainer>
        );

      case 'PIE':
        return (
          <ResponsiveContainer width="100%" height={chartHeight}>
            <PieChart>
              <Pie
                data={data}
                dataKey={suggestion.y_axis || 'value'}
                nameKey={suggestion.x_axis || 'name'}
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        );

      case 'HISTOGRAM':
        return (
          <ResponsiveContainer width="100%" height={chartHeight}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={suggestion.x_axis || 'bin'} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey={suggestion.y_axis || 'count'} fill="#764ba2" />
            </BarChart>
          </ResponsiveContainer>
        );

      default:
        return <div>Unsupported chart type: {suggestion.type}</div>;
    }
  };

  return (
    <div className={`chart-container ${className || ''}`}>
      <div className="chart-header">
        <h3 className="chart-title">{suggestion.title}</h3>
        <p className="chart-description">{suggestion.description}</p>
      </div>
      <div className="chart-body">{renderChart()}</div>

      <style>{`
        .chart-container {
          background: white;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .chart-header {
          margin-bottom: 1.5rem;
        }

        .chart-title {
          font-size: 1.25rem;
          font-weight: 600;
          color: #2d3748;
          margin: 0 0 0.5rem 0;
        }

        .chart-description {
          font-size: 0.9rem;
          color: #718096;
          margin: 0;
        }

        .chart-body {
          min-height: 300px;
        }
      `}</style>
    </div>
  );
};

export default ChartRenderer;
