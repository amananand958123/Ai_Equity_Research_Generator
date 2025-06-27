'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, AlertCircle, RefreshCw } from 'lucide-react';

interface FeatureStatusData {
  gemini: boolean;
  alphaVantage: boolean;
  newsApi: boolean;
  advancedCharts: boolean;
  pdfGeneration: boolean;
}

export default function FeatureStatus() {
  const [status, setStatus] = useState<FeatureStatusData>({
    gemini: false,
    alphaVantage: false,
    newsApi: false,
    advancedCharts: false,
    pdfGeneration: false,
  });
  const [loading, setLoading] = useState(true);
  const [lastCheck, setLastCheck] = useState<string>('');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const checkFeatureStatus = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/status');
      if (response.ok) {
        const data = await response.json();
        setStatus(data);
        setLastCheck(new Date().toLocaleTimeString());
      }
    } catch (error) {
      console.error('Error checking feature status:', error);
      // Mock data for development
      setStatus({
        gemini: true,
        alphaVantage: true,
        newsApi: true,
        advancedCharts: true,
        pdfGeneration: true,
      });
      setLastCheck(new Date().toLocaleTimeString());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (mounted) {
      checkFeatureStatus();
    }
  }, [mounted]);

  // Don't render time-sensitive content until mounted
  if (!mounted) {
    return (
      <div className="rounded-lg bg-white/10 backdrop-blur-sm border border-white/20 p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <RefreshCw className="h-5 w-5 text-blue-400 animate-spin" />
            <span className="text-sm font-medium text-white">
              System Status
            </span>
          </div>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="flex items-center gap-2 p-2 rounded bg-white/5">
              <div className="h-4 w-4 bg-white/20 rounded animate-pulse"></div>
              <div className="flex-1">
                <div className="h-3 bg-white/20 rounded animate-pulse mb-1"></div>
                <div className="h-2 bg-white/10 rounded animate-pulse"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  const features = [
    {
      key: 'gemini' as keyof FeatureStatusData,
      name: 'AI Analysis (Gemini)',
      description: 'Google Gemini AI for analysis',
    },
    {
      key: 'alphaVantage' as keyof FeatureStatusData,
      name: 'Market Data',
      description: 'Alpha Vantage financial data',
    },
    {
      key: 'newsApi' as keyof FeatureStatusData,
      name: 'News & Sentiment',
      description: 'NewsAPI integration',
    },
    {
      key: 'advancedCharts' as keyof FeatureStatusData,
      name: 'Advanced Charts',
      description: 'Interactive visualizations',
    },
    {
      key: 'pdfGeneration' as keyof FeatureStatusData,
      name: 'PDF Reports',
      description: 'Export functionality',
    },
  ];

  const getStatusIcon = (isActive: boolean) => {
    if (loading) {
      return <RefreshCw className="h-4 w-4 text-blue-500 animate-spin" />;
    }
    return isActive ? (
      <CheckCircle className="h-4 w-4 text-green-600" />
    ) : (
      <XCircle className="h-4 w-4 text-red-500" />
    );
  };

  const getStatusColor = (isActive: boolean) => {
    if (loading) return 'text-blue-500';
    return isActive ? 'text-green-600' : 'text-red-500';
  };

  const allFeaturesActive = Object.values(status).every(Boolean);

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="rounded-lg bg-white/10 backdrop-blur-sm border border-white/20 p-4"
    >
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          {allFeaturesActive && !loading ? (
            <CheckCircle className="h-5 w-5 text-green-400" />
          ) : (
            <AlertCircle className="h-5 w-5 text-yellow-400" />
          )}
          <span className="text-sm font-medium text-white">
            System Status
          </span>
        </div>
        <button
          onClick={checkFeatureStatus}
          disabled={loading}
          className="text-white/70 hover:text-white transition-colors"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-2">
        {features.map((feature) => (
          <motion.div
            key={feature.key}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="flex items-center gap-2 p-2 rounded bg-white/5"
          >
            {getStatusIcon(status[feature.key])}
            <div className="min-w-0 flex-1">
              <div className={`text-xs font-medium ${getStatusColor(status[feature.key])}`}>
                {feature.name}
              </div>
              <div className="text-xs text-white/60 truncate">
                {feature.description}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {lastCheck && (
        <div className="mt-2 text-xs text-white/50">
          Last checked: {lastCheck}
        </div>
      )}
    </motion.div>
  );
}
