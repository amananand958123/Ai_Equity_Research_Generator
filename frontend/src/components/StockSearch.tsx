'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, TrendingUp, Building2, X } from 'lucide-react';

interface StockSuggestion {
  symbol: string;
  name: string;
  type: string;
  region: string;
  market?: string;
  confidence?: number;
  match_type?: string;
  reason?: string;
  highlight?: string;
}

// Extend the interface for search results with additional properties
interface SearchStockSuggestion extends StockSuggestion {
  confidence?: number;
  match_type?: string;
  reason?: string;
  market?: string;
  highlight?: string;
}

interface StockSearchProps {
  onStockSelect: (symbol: string) => void;
}

export default function StockSearch({ onStockSelect }: StockSearchProps) {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState<SearchStockSuggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);
  
  const inputRef = useRef<HTMLInputElement>(null);
  const debounceRef = useRef<NodeJS.Timeout | null>(null);

  // Popular stocks for quick access
  const popularStocks: StockSuggestion[] = [
    { symbol: 'AAPL', name: 'Apple Inc.', type: 'Equity', region: 'United States' },
    { symbol: 'GOOGL', name: 'Alphabet Inc.', type: 'Equity', region: 'United States' },
    { symbol: 'MSFT', name: 'Microsoft Corporation', type: 'Equity', region: 'United States' },
    { symbol: 'TSLA', name: 'Tesla, Inc.', type: 'Equity', region: 'United States' },
    { symbol: 'RELIANCE.NS', name: 'Reliance Industries Limited', type: 'Equity', region: 'India' },
    { symbol: 'TCS.NS', name: 'Tata Consultancy Services Limited', type: 'Equity', region: 'India' },
    { symbol: 'TATAMOTORS.NS', name: 'Tata Motors Limited', type: 'Equity', region: 'India' },
    { symbol: 'HDFCBANK.NS', name: 'HDFC Bank Limited', type: 'Equity', region: 'India' },
  ];

  const searchStocks = async (searchQuery: string) => {
    if (searchQuery.length < 1) {
      setSuggestions([]);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`/api/search-stocks?q=${encodeURIComponent(searchQuery)}`);
      if (response.ok) {
        const data = await response.json();
        let allSuggestions = data.suggestions || [];
        
        // Add format suggestions if available
        if (data.format_suggestions) {
          allSuggestions = [...allSuggestions, ...data.format_suggestions];
        }
        
        // Add validation suggestions if no regular suggestions
        if (allSuggestions.length === 0 && data.validation?.suggestions) {
          allSuggestions = data.validation.suggestions.slice(0, 5);
        }
        
        setSuggestions(allSuggestions);
      } else {
        throw new Error('API not available');
      }
    } catch {
      console.log('Using filtered popular stocks - API not available');
      // Fallback to mock suggestions for demo
      const mockSuggestions = popularStocks.filter(
        stock => 
          stock.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
          stock.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setSuggestions(mockSuggestions);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setSelectedIndex(-1);

    if (debounceRef.current) {
      clearTimeout(debounceRef.current);
    }

    debounceRef.current = setTimeout(() => {
      searchStocks(value);
    }, 300);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!showSuggestions) return;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => 
          prev < suggestions.length - 1 ? prev + 1 : prev
        );
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => prev > 0 ? prev - 1 : -1);
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && suggestions[selectedIndex]) {
          handleStockSelect(suggestions[selectedIndex].symbol);
        } else if (query.trim()) {
          handleStockSelect(query.trim().toUpperCase());
        }
        break;
      case 'Escape':
        setShowSuggestions(false);
        setSelectedIndex(-1);
        break;
    }
  };

  const handleStockSelect = (symbol: string) => {
    setQuery(symbol);
    setShowSuggestions(false);
    setSuggestions([]);
    setSelectedIndex(-1);
    onStockSelect(symbol);
  };

  const clearSearch = () => {
    setQuery('');
    setSuggestions([]);
    setShowSuggestions(false);
    setSelectedIndex(-1);
    inputRef.current?.focus();
  };

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (inputRef.current && !inputRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative">
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <Search className="h-4 w-4 text-gray-400" />
        </div>
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onFocus={() => setShowSuggestions(true)}
          placeholder="Search stocks... (e.g., AAPL, TATAMOTORS.NS, SHEL.L)"
          className="block w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg bg-white text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        {query && (
          <button
            onClick={clearSearch}
            className="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <X className="h-4 w-4 text-gray-400 hover:text-gray-600" />
          </button>
        )}
      </div>

      {/* Ticker format help */}
      <div className="mt-2 text-xs text-gray-500">
        <p>
          <strong>Ticker Format Examples:</strong> US: AAPL, MSFT | India: RELIANCE.NS, TCS.NS | UK: SHEL.L | Canada: SHOP.TO
        </p>
      </div>

      <AnimatePresence>
        {showSuggestions && (suggestions.length > 0 || query.length === 0) && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
            className="absolute z-10 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg max-h-60 overflow-auto"
          >
            {query.length === 0 && (
              <div className="px-4 py-2 text-sm text-gray-500 border-b">
                Popular Stocks
              </div>
            )}
            
            {(query.length === 0 ? popularStocks : suggestions).map((stock, index) => {
              // Type guard to handle both basic and extended stock suggestions
              const isExtended = 'confidence' in stock || 'match_type' in stock || 'reason' in stock;
              
              return (
                <motion.button
                  key={`${stock.symbol}-${index}`}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: index * 0.05 }}
                  onClick={() => handleStockSelect(stock.symbol)}
                  className={`w-full px-4 py-3 text-left hover:bg-gray-50 flex items-center gap-3 ${
                    selectedIndex === index ? 'bg-blue-50 border-l-2 border-blue-500' : ''
                  }`}
                >
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                      {stock.type === 'Equity' ? (
                        <TrendingUp className="h-4 w-4 text-blue-600" />
                      ) : (
                        <Building2 className="h-4 w-4 text-blue-600" />
                      )}
                    </div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-gray-900">{stock.symbol}</span>
                      {isExtended && (stock as SearchStockSuggestion).confidence && (stock as SearchStockSuggestion).confidence! < 1.0 && (
                        <span className="text-xs px-2 py-1 bg-yellow-100 text-yellow-800 rounded">
                          {(stock as SearchStockSuggestion).match_type === 'fuzzy' ? 'Similar' : 'Match'}
                        </span>
                      )}
                      {isExtended && (stock as SearchStockSuggestion).reason && (
                        <span className="text-xs text-gray-500">({(stock as SearchStockSuggestion).reason})</span>
                      )}
                    </div>
                    <div className="text-sm text-gray-500 truncate">{stock.name}</div>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-xs text-gray-400">{stock.region}</span>
                      {stock.market && (
                        <>
                          <span className="text-xs text-gray-400">•</span>
                          <span className="text-xs text-gray-400">{stock.market}</span>
                        </>
                      )}
                      {isExtended && (stock as SearchStockSuggestion).confidence && (stock as SearchStockSuggestion).confidence! < 1.0 && (
                        <>
                          <span className="text-xs text-gray-400">•</span>
                          <span className="text-xs text-blue-600">
                            {Math.round((stock as SearchStockSuggestion).confidence! * 100)}% match
                          </span>
                        </>
                      )}
                    </div>
                  </div>
                </motion.button>
              );
            })}

            {loading && (
              <div className="px-4 py-3 text-center text-sm text-gray-500">
                <div className="inline-flex items-center gap-2">
                  <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                  Searching...
                </div>
              </div>
            )}

            {!loading && suggestions.length === 0 && query.length >= 2 && (
              <div className="px-4 py-3 text-center text-sm text-gray-500">
                No results found for &quot;{query}&quot;
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
