'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, Search, BarChart3, FileText, Globe, Zap } from 'lucide-react';
import StockSearch from '@/components/StockSearch';
import Dashboard from '@/components/Dashboard';
import Header from '@/components/Header';

export default function Home() {
  const [selectedStock, setSelectedStock] = useState<string>('');
  const [analysisLevel, setAnalysisLevel] = useState<'basic' | 'enhanced' | 'comprehensive'>('enhanced');

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <Header />
      
      {/* Hero Section */}
      <motion.section 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative overflow-hidden bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 text-white"
      >
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative mx-auto max-w-7xl px-6 py-24 sm:py-32 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-4xl font-bold tracking-tight sm:text-6xl"
            >
              📊 Equity Research Report Generator
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="mt-6 text-lg leading-8 text-blue-100"
            >
              AI-Powered Financial Analysis & Comprehensive Research Reports
            </motion.p>
          </div>
        </div>
      </motion.section>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-6 py-12 lg:px-8">
        <div className="grid gap-8 lg:grid-cols-3">
          {/* Left Column - Search & Config */}
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.8, duration: 0.6 }}
            className="lg:col-span-1"
          >
            <div className="sticky top-8 space-y-6">
              {/* Stock Search */}
              <div className="rounded-xl bg-white p-6 shadow-lg border border-gray-100">
                <div className="flex items-center gap-2 mb-4">
                  <Search className="h-5 w-5 text-blue-600" />
                  <h2 className="text-lg font-semibold text-gray-900">Stock Search</h2>
                </div>
                <StockSearch onStockSelect={setSelectedStock} />
              </div>

              {/* Analysis Level */}
              <div className="rounded-xl bg-white p-6 shadow-lg border border-gray-100">
                <div className="flex items-center gap-2 mb-4">
                  <BarChart3 className="h-5 w-5 text-purple-600" />
                  <h2 className="text-lg font-semibold text-gray-900">Analysis Level</h2>
                </div>
                <div className="space-y-2">
                  {[
                    { key: 'basic', label: 'Basic (Level 1)', desc: 'Core analysis with AI' },
                    { key: 'enhanced', label: 'Enhanced (Level 2)', desc: 'Multi-source + charts' },
                    { key: 'comprehensive', label: 'Comprehensive (Level 3)', desc: 'Institutional-grade' }
                  ].map((level) => (
                    <label key={level.key} className="flex items-start gap-3 cursor-pointer">
                      <input
                        type="radio"
                        name="analysisLevel"
                        value={level.key}
                        checked={analysisLevel === level.key}
                        onChange={(e) => setAnalysisLevel(e.target.value as 'basic' | 'enhanced' | 'comprehensive')}
                        className="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500"
                      />
                      <div>
                        <div className="font-medium text-gray-900">{level.label}</div>
                        <div className="text-sm text-gray-500">{level.desc}</div>
                      </div>
                    </label>
                  ))}
                </div>
              </div>

              {/* Features Overview */}
              <div className="rounded-xl bg-white p-6 shadow-lg border border-gray-100">
                <div className="flex items-center gap-2 mb-4">
                  <Zap className="h-5 w-5 text-green-600" />
                  <h2 className="text-lg font-semibold text-gray-900">Features</h2>
                </div>
                <div className="space-y-3">
                  {[
                    { icon: TrendingUp, text: 'Real-time Data', color: 'text-green-600' },
                    { icon: BarChart3, text: 'Interactive Charts', color: 'text-blue-600' },
                    { icon: FileText, text: 'AI Analysis', color: 'text-purple-600' },
                    { icon: Globe, text: 'Global Markets', color: 'text-orange-600' }
                  ].map((feature, index) => (
                    <div key={index} className="flex items-center gap-3">
                      <feature.icon className={`h-4 w-4 ${feature.color}`} />
                      <span className="text-sm text-gray-600">{feature.text}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>

          {/* Right Column - Dashboard */}
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 1.0, duration: 0.6 }}
            className="lg:col-span-2"
          >
            {selectedStock ? (
              <Dashboard 
                ticker={selectedStock} 
                analysisLevel={analysisLevel}
              />
            ) : (
              <div className="rounded-xl bg-white p-12 shadow-lg border border-gray-100 text-center">
                <div className="mx-auto h-24 w-24 rounded-full bg-gray-100 flex items-center justify-center mb-6">
                  <Search className="h-12 w-12 text-gray-400" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  Select a Stock to Analyze
                </h3>
                <p className="text-gray-500 mb-8">
                  Search for any stock ticker to get started with comprehensive analysis
                </p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                  {['AAPL', 'GOOGL', 'TSLA', 'MSFT'].map((ticker) => (
                    <button
                      key={ticker}
                      onClick={() => setSelectedStock(ticker)}
                      className="rounded-lg bg-blue-50 px-4 py-3 text-sm font-medium text-blue-700 hover:bg-blue-100 transition-colors"
                    >
                      {ticker}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </main>
    </div>
  );
}
