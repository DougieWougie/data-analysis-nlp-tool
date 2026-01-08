/**
 * SentimentDistributionChart component for visualizing sentiment analysis results
 */
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface SentimentDistributionChartProps {
  data: Record<string, any>[];
  sentimentColumn: string;
}

const SENTIMENT_COLORS = {
  POSITIVE: '#48bb78',
  NEGATIVE: '#f56565',
  NEUTRAL: '#a0aec0',
};

const SentimentDistributionChart = ({ data, sentimentColumn }: SentimentDistributionChartProps) => {
  // Count sentiment occurrences
  const sentimentCounts = data.reduce((acc, row) => {
    const sentiment = row[sentimentColumn];
    if (sentiment) {
      acc[sentiment] = (acc[sentiment] || 0) + 1;
    }
    return acc;
  }, {} as Record<string, number>);

  // Convert to chart data format
  const chartData = Object.entries(sentimentCounts).map(([name, value]) => ({
    name,
    value,
    percentage: ((value / data.length) * 100).toFixed(1),
  }));

  if (chartData.length === 0) {
    return (
      <div className="sentiment-chart-container">
        <h3>Sentiment Distribution</h3>
        <p className="empty-state">No sentiment data available</p>
      </div>
    );
  }

  return (
    <div className="sentiment-chart-container">
      <h3 className="chart-title">Sentiment Distribution</h3>
      <p className="chart-subtitle">
        Analyzing {data.length} entries from column: <strong>{sentimentColumn.replace('_sentiment', '')}</strong>
      </p>

      <ResponsiveContainer width="100%" height={350}>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label={({ name, percentage }) => `${name}: ${percentage}%`}
          >
            {chartData.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={SENTIMENT_COLORS[entry.name as keyof typeof SENTIMENT_COLORS] || '#cbd5e0'}
              />
            ))}
          </Pie>
          <Tooltip
            formatter={(value: number, name: string, props: any) => [
              `${value} (${props.payload.percentage}%)`,
              name,
            ]}
          />
          <Legend />
        </PieChart>
      </ResponsiveContainer>

      <div className="sentiment-summary">
        {chartData.map((item) => (
          <div key={item.name} className="sentiment-stat">
            <div
              className="stat-indicator"
              style={{ backgroundColor: SENTIMENT_COLORS[item.name as keyof typeof SENTIMENT_COLORS] }}
            />
            <div className="stat-content">
              <span className="stat-label">{item.name}</span>
              <span className="stat-value">
                {item.value} ({item.percentage}%)
              </span>
            </div>
          </div>
        ))}
      </div>

      <style>{`
        .sentiment-chart-container {
          background: white;
          border-radius: 8px;
          padding: 1.5rem;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          margin: 2rem 0;
        }

        .chart-title {
          font-size: 1.25rem;
          font-weight: 600;
          color: #2d3748;
          margin: 0 0 0.5rem 0;
        }

        .chart-subtitle {
          font-size: 0.9rem;
          color: #718096;
          margin: 0 0 1.5rem 0;
        }

        .chart-subtitle strong {
          color: #2d3748;
        }

        .empty-state {
          text-align: center;
          padding: 2rem;
          color: #a0aec0;
        }

        .sentiment-summary {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 1rem;
          margin-top: 1.5rem;
          padding-top: 1.5rem;
          border-top: 1px solid #e2e8f0;
        }

        .sentiment-stat {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }

        .stat-indicator {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          flex-shrink: 0;
        }

        .stat-content {
          display: flex;
          flex-direction: column;
        }

        .stat-label {
          font-size: 0.85rem;
          color: #718096;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .stat-value {
          font-size: 1.1rem;
          font-weight: 600;
          color: #2d3748;
        }

        @media (max-width: 768px) {
          .sentiment-chart-container {
            padding: 1rem;
          }

          .sentiment-summary {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default SentimentDistributionChart;
