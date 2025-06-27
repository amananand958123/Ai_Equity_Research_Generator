'use client';

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { Loader2 } from 'lucide-react';
import { PlotParams } from 'react-plotly.js';

// Dynamically import Plot to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), {
  ssr: false,
  loading: () => (
    <div className="h-96 bg-gray-50 rounded-lg flex items-center justify-center">
      <div className="flex items-center gap-2 text-gray-500">
        <Loader2 className="h-5 w-5 animate-spin" />
        Loading chart...
      </div>
    </div>
  ),
}) as React.ComponentType<PlotParams>;

interface ChartData {
  date: string;
  price: number;
  volume: number;
}

interface InteractiveChartProps {
  symbol: string;
  data: ChartData[];
}

export default function InteractiveChart({ symbol, data }: InteractiveChartProps) {
  const [chartType, setChartType] = useState<'line' | 'candlestick' | 'volume'>('line');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted || !data || data.length === 0) {
    return (
      <div className="h-96 bg-gray-50 rounded-lg flex items-center justify-center">
        <div className="text-gray-500">
          {!mounted ? 'Loading chart...' : 'No chart data available'}
        </div>
      </div>
    );
  }

  // Prepare data for different chart types
  const dates = data.map(item => item.date);
  const prices = data.map(item => item.price);
  const volumes = data.map(item => item.volume);

  const getPlotData = () => {
    switch (chartType) {
      case 'line':
        return [
          {
            x: dates,
            y: prices,
            type: 'scatter' as const,
            mode: 'lines' as const,
            line: { color: '#3B82F6', width: 2 },
            name: 'Price',
            hovertemplate: '<b>%{y:.2f}</b><br>%{x}<extra></extra>',
          },
        ];
      
      case 'candlestick':
        // For candlestick, we'll simulate OHLC data from the price
        const ohlcData = data.map((item, index) => {
          const basePrice = item.price;
          const volatility = basePrice * 0.02; // 2% volatility
          return {
            open: index > 0 ? data[index - 1].price : basePrice,
            high: basePrice + Math.random() * volatility,
            low: basePrice - Math.random() * volatility,
            close: basePrice,
          };
        });

        return [
          {
            x: dates,
            open: ohlcData.map(d => d.open),
            high: ohlcData.map(d => d.high),
            low: ohlcData.map(d => d.low),
            close: ohlcData.map(d => d.close),
            type: 'candlestick' as const,
            name: symbol,
            increasing: { line: { color: '#10B981' } },
            decreasing: { line: { color: '#EF4444' } },
          },
        ];
      
      case 'volume':
        return [
          {
            x: dates,
            y: volumes,
            type: 'bar' as const,
            marker: { color: '#8B5CF6' },
            name: 'Volume',
            hovertemplate: '<b>%{y:,.0f}</b><br>%{x}<extra></extra>',
          },
        ];
      
      default:
        return [];
    }
  };

  const layout = {
    title: {
      text: `${symbol} - ${chartType.charAt(0).toUpperCase() + chartType.slice(1)} Chart`,
      font: { size: 18, color: '#1F2937' },
    },
    xaxis: {
      title: 'Date',
      type: 'date' as const,
      showgrid: true,
      gridcolor: '#E5E7EB',
    },
    yaxis: {
      title: chartType === 'volume' ? 'Volume' : 'Price ($)',
      showgrid: true,
      gridcolor: '#E5E7EB',
    },
    plot_bgcolor: '#FAFAFA',
    paper_bgcolor: '#FFFFFF',
    font: { family: 'Inter, sans-serif', color: '#374151' },
    margin: { l: 60, r: 40, t: 60, b: 60 },
    hovermode: 'closest' as const,
    showlegend: true,
    legend: {
      orientation: 'h' as const,
      x: 0,
      y: -0.2,
    },
  };

  const config = {
    displayModeBar: true,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
    displaylogo: false,
    responsive: true,
  } as Partial<Plotly.Config>;

  return (
    <div className="space-y-4">
      {/* Chart Type Selector */}
      <div className="flex items-center gap-2">
        <span className="text-sm font-medium text-gray-700">Chart Type:</span>
        <div className="flex rounded-lg border border-gray-300 bg-white">
          {[
            { key: 'line', label: 'Line' },
            { key: 'candlestick', label: 'Candlestick' },
            { key: 'volume', label: 'Volume' },
          ].map((type) => (
            <button
              key={type.key}
              onClick={() => setChartType(type.key as 'line' | 'candlestick' | 'volume')}
              className={`px-3 py-1.5 text-sm font-medium transition-colors ${
                chartType === type.key
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-700 hover:bg-gray-50'
              } ${
                type.key === 'line' ? 'rounded-l-lg' : 
                type.key === 'volume' ? 'rounded-r-lg' : ''
              }`}
            >
              {type.label}
            </button>
          ))}
        </div>
      </div>

      {/* Chart Container */}
      <div className="bg-white rounded-lg border border-gray-200 p-4">
        <Plot
          data={getPlotData()}
          layout={layout}
          config={config}
          style={{ width: '100%', height: '400px' }}
        />
      </div>

      {/* Chart Statistics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
        <div className="bg-white rounded-lg border border-gray-200 p-3">
          <div className="text-gray-500">Current Price</div>
          <div className="font-semibold">${prices[prices.length - 1]?.toFixed(2)}</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-3">
          <div className="text-gray-500">Day Change</div>
          <div className={`font-semibold ${
            prices[prices.length - 1] > prices[prices.length - 2] 
              ? 'text-green-600' : 'text-red-600'
          }`}>
            {prices.length > 1 
              ? ((prices[prices.length - 1] - prices[prices.length - 2]) / prices[prices.length - 2] * 100).toFixed(2) 
              : '0.00'}%
          </div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-3">
          <div className="text-gray-500">High</div>
          <div className="font-semibold">${Math.max(...prices).toFixed(2)}</div>
        </div>
        <div className="bg-white rounded-lg border border-gray-200 p-3">
          <div className="text-gray-500">Low</div>
          <div className="font-semibold">${Math.min(...prices).toFixed(2)}</div>
        </div>
      </div>
    </div>
  );
}
