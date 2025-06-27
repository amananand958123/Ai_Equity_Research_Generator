"""
Bridge Server for Next.js Frontend to Python Backend Integration
This server provides a simple HTTP API that the Next.js frontend can call
to access all the advanced features from the Python backend.

IMPORTANT: This server should be run from within the .venv virtual environment
to ensure all dependencies are available.
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import sys
import json
from datetime import datetime
import yfinance as yf
import pandas as pd
import re
from difflib import SequenceMatcher

# Verify we're running in the virtual environment
def check_virtual_env():
    """Check if we're running in the expected virtual environment."""
    venv_path = os.path.join(os.getcwd(), '.venv')
    if '.venv' not in sys.executable:
        print("⚠️  WARNING: Not running in virtual environment!")
        print(f"   Current Python: {sys.executable}")
        print(f"   Expected: {venv_path}/bin/python")
        print("   Please activate the virtual environment first:")
        print("   source .venv/bin/activate")
        print()
    else:
        print(f"✅ Running in virtual environment: {sys.executable}")

check_virtual_env()

# Add the current directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from data_aggregator import AdvancedDataAggregator
    from advanced_visualizer import AdvancedVisualizer
    from pdf_generator import AdvancedPDFGenerator
    from comprehensive_report_generator import comprehensive_generator
    import google.generativeai as genai
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Configure Gemini AI
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some backend modules not available: {e}")
    BACKEND_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Initialize backend components if available
if BACKEND_AVAILABLE:
    try:
        data_aggregator = AdvancedDataAggregator()
        visualizer = AdvancedVisualizer()
        pdf_generator = AdvancedPDFGenerator()
    except Exception as e:
        print(f"Warning: Could not initialize backend components: {e}")
        BACKEND_AVAILABLE = False

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'backend_available': BACKEND_AVAILABLE
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get status of all backend services"""
    status = {
        'gemini': bool(os.getenv('GOOGLE_API_KEY')),
        'alphaVantage': bool(os.getenv('ALPHA_VANTAGE_API_KEY')),
        'newsApi': bool(os.getenv('NEWSAPI_KEY')),
        'advancedCharts': BACKEND_AVAILABLE,
        'pdfGeneration': BACKEND_AVAILABLE,
    }
    return jsonify(status)

@app.route('/api/search-stocks', methods=['GET'])
def search_stocks():
    """Enhanced search for stock symbols with format suggestions"""
    query = request.args.get('q', '').strip()
    
    if len(query) < 1:
        return jsonify({'suggestions': []})
    
    try:
        # Use enhanced search
        suggestions = search_stocks_enhanced(query, limit=10)
        
        # Add ticker validation for the exact query
        validation = validate_ticker_format(query)
        
        response = {
            'suggestions': suggestions,
            'validation': validation,
            'query': query
        }
        
        # If no exact matches but we have suggestions from validation, include them
        if not suggestions and validation.get('suggestions'):
            response['format_suggestions'] = validation['suggestions'][:5]
        
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate-ticker', methods=['GET'])
def validate_ticker():
    """Validate ticker format and suggest corrections"""
    symbol = request.args.get('symbol', '').strip()
    
    if not symbol:
        return jsonify({'error': 'Symbol parameter required'}), 400
    
    try:
        validation = validate_ticker_format(symbol)
        return jsonify(validation)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stock-data', methods=['GET'])
def get_stock_data():
    """Get basic stock data with enhanced validation and error handling"""
    symbol = request.args.get('symbol', '').strip()
    
    if not symbol:
        return jsonify({'error': 'Symbol parameter required'}), 400
    
    # Validate ticker format first
    validation = validate_ticker_format(symbol)
    original_symbol = symbol
    symbol = symbol.upper()
    
    try:
        # Get data using yfinance
        stock = yf.Ticker(symbol)
        info = stock.info
        hist = stock.history(period='5d')
        
        # Check if we got valid data
        if hist.empty or len(hist) == 0:
            # If no data found, provide suggestions
            error_response = {
                'error': f'No data found for symbol "{symbol}"',
                'validation': validation,
                'suggestions': validation.get('suggestions', [])[:5] if validation.get('suggestions') else [],
                'help': {
                    'message': 'Try one of these formats:',
                    'examples': [
                        'AAPL (US stocks)',
                        'RELIANCE.NS (Indian stocks)',
                        'SHEL.L (UK stocks)',
                        'SHOP.TO (Canadian stocks)'
                    ]
                }
            }
            return jsonify(error_response), 404
        
        # Check if this looks like valid stock data
        if info.get('regularMarketPrice') is None and info.get('previousClose') is None:
            # Might be a valid ticker but no market data available
            error_response = {
                'error': f'No market data available for symbol "{symbol}"',
                'validation': validation,
                'note': 'Symbol may be valid but market is closed or data unavailable'
            }
            return jsonify(error_response), 404
        
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
        change = current_price - prev_price
        change_percent = (change / prev_price) * 100
        
        # Determine market from symbol
        market_info = None
        if '.' in symbol:
            suffix = '.' + symbol.split('.', 1)[1]
            market_info = MARKET_SUFFIXES.get(suffix, 'Unknown Market')
        else:
            market_info = 'United States'
        
        data = {
            'symbol': symbol,
            'originalQuery': original_symbol,
            'price': round(float(current_price), 2),
            'change': round(float(change), 2),
            'changePercent': round(float(change_percent), 2),
            'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist and not pd.isna(hist['Volume'].iloc[-1]) else 0,
            'marketCap': info.get('marketCap', 'N/A'),
            'pe': round(float(info.get('trailingPE', 0)), 2) if info.get('trailingPE') and info.get('trailingPE') != 'N/A' else 'N/A',
            'beta': round(float(info.get('beta', 0)), 3) if info.get('beta') and info.get('beta') != 'N/A' else 'N/A',
            'week52High': round(float(info.get('fiftyTwoWeekHigh', 0)), 2) if info.get('fiftyTwoWeekHigh') else 'N/A',
            'week52Low': round(float(info.get('fiftyTwoWeekLow', 0)), 2) if info.get('fiftyTwoWeekLow') else 'N/A',
            'marketInfo': market_info,
            'companyName': info.get('longName', info.get('shortName', 'N/A')),
            'currency': info.get('currency', 'USD'),
            'validation': {
                'isValid': validation.get('is_valid', True),
                'formatCorrect': True,
                'dataAvailable': True
            }
        }
        
        return jsonify(data)
    except Exception as e:
        # Enhanced error handling with suggestions
        error_response = {
            'error': f'Failed to fetch data for "{symbol}": {str(e)}',
            'validation': validation,
            'suggestions': validation.get('suggestions', [])[:3] if validation.get('suggestions') else [],
            'help': {
                'common_issues': [
                    'Symbol may be misspelled',
                    'May need market suffix (e.g., .NS for India, .L for UK)',
                    'Stock may be delisted or not publicly traded',
                    'Market may be closed'
                ]
            }
        }
        return jsonify(error_response), 500

@app.route('/api/chart-data', methods=['GET'])
def get_chart_data():
    """Get historical chart data"""
    symbol = request.args.get('symbol', '').upper()
    period = request.args.get('period', '1y')
    
    if not symbol:
        return jsonify({'error': 'Symbol parameter required'}), 400
    
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        
        chart_data = []
        for date, row in hist.iterrows():
            chart_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'price': round(float(row['Close']), 2),
                'volume': int(row['Volume']) if 'Volume' in row else 0,
            })
        
        return jsonify({'chartData': chart_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/news', methods=['GET'])
def get_news():
    """Get news and sentiment data"""
    symbol = request.args.get('symbol', '').upper()
    
    if not symbol:
        return jsonify({'error': 'Symbol parameter required'}), 400
    
    try:
        # For now, return mock news data since the data aggregator requires company name
        # which we don't have readily available in this context
        mock_news = [
            {
                'title': f'{symbol} Reports Strong Quarterly Results',
                'description': f'{symbol} exceeded analyst expectations with strong revenue growth.',
                'url': '#',
                'publishedAt': datetime.now().isoformat(),
                'sentiment': 'positive',
                'score': 0.8,
            },
            {
                'title': f'Market Analysis: {symbol} Maintains Strong Position',
                'description': f'Analysts remain optimistic about {symbol}\'s market performance and growth prospects.',
                'url': '#',
                'publishedAt': (datetime.now() - pd.Timedelta(hours=6)).isoformat(),
                'sentiment': 'positive',
                'score': 0.6,
            },
            {
                'title': f'Industry Watch: {symbol} Sector Trends',
                'description': f'Latest trends affecting {symbol} and similar companies in the sector.',
                'url': '#',
                'publishedAt': (datetime.now() - pd.Timedelta(hours=12)).isoformat(),
                'sentiment': 'neutral',
                'score': 0.2,
            }
        ]
        return jsonify({'news': mock_news})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    """Get AI analysis"""
    symbol = request.args.get('symbol', '').upper()
    level = request.args.get('level', 'basic')
    
    if not symbol:
        return jsonify({'error': 'Symbol parameter required'}), 400
    
    try:
        # For now, return mock analysis data as the Gemini integration needs refinement
        analysis = {
            'summary': f'{symbol} shows solid fundamentals with consistent growth prospects and strong market position in its sector.',
            'strengths': [
                'Strong market position',
                'Consistent revenue growth',
                'Solid balance sheet',
                'Innovation leadership',
                'Diverse product portfolio'
            ],
            'weaknesses': [
                'Market competition',
                'Economic sensitivity',
                'Valuation concerns'
            ],
            'recommendation': 'Buy' if symbol in ['AAPL', 'MSFT', 'GOOGL'] else 'Hold',
            'targetPrice': 200.0 if symbol == 'AAPL' else 180.0,
            'confidence': 0.75
        }
        
        # Customize based on analysis level
        if level == 'enhanced':
            analysis['strengths'].append('Strong brand recognition')
            analysis['weaknesses'].append('Regulatory challenges')
        elif level == 'comprehensive':
            analysis['strengths'].extend(['Strong brand recognition', 'Global market presence'])
            analysis['weaknesses'].extend(['Regulatory challenges', 'Supply chain dependencies'])
            analysis['confidence'] = 0.85
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    """Generate comprehensive educational equity research PDF report"""
    symbol = request.json.get('symbol', '').upper()
    level = request.json.get('level', 'comprehensive')
    
    if not symbol:
        return jsonify({'error': 'Symbol parameter required'}), 400
    
    try:
        # Use the comprehensive report generator
        html_content = comprehensive_generator.generate_comprehensive_report(symbol)
        pdf_bytes = comprehensive_generator.generate_pdf_bytes(html_content)
        
        if pdf_bytes:
            # Create a temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(pdf_bytes)
                tmp_file_path = tmp_file.name
            
            return send_file(
                tmp_file_path, 
                as_attachment=True, 
                download_name=f"{symbol}_Educational_Research_Report.pdf",
                mimetype='application/pdf'
            )
        else:
            return jsonify({'error': 'Failed to generate PDF'}), 500
            
    except Exception as e:
        print(f"PDF generation error: {e}")
        return jsonify({'error': str(e)}), 500

# Comprehensive stock ticker database and validation
MARKET_SUFFIXES = {
    '.NS': 'India (National Stock Exchange)',
    '.BO': 'India (Bombay Stock Exchange)', 
    '.L': 'UK (London Stock Exchange)',
    '.TO': 'Canada (Toronto Stock Exchange)',
    '.V': 'Canada (TSX Venture Exchange)',
    '.AX': 'Australia (Australian Securities Exchange)',
    '.NZ': 'New Zealand',
    '.HK': 'Hong Kong',
    '.SI': 'Singapore',
    '.KS': 'South Korea',
    '.T': 'Japan (Tokyo Stock Exchange)',
    '.DE': 'Germany (Xetra)',
    '.PA': 'France (Euronext Paris)',
    '.AS': 'Netherlands (Euronext Amsterdam)',
    '.MI': 'Italy (Borsa Italiana)',
    '.MC': 'Spain (Bolsa de Madrid)',
    '.SW': 'Switzerland (SIX Swiss Exchange)',
    '.ST': 'Sweden (Nasdaq Stockholm)',
    '.OL': 'Norway (Oslo Børs)',
    '.BR': 'Belgium (Euronext Brussels)',
    '.LS': 'Portugal (Euronext Lisbon)',
    '.VI': 'Austria (Wiener Börse)',
    '.PR': 'Czech Republic (Prague Stock Exchange)',
    '.WA': 'Poland (Warsaw Stock Exchange)',
    '.BD': 'Hungary (Budapest Stock Exchange)',
    '.RG': 'Latvia (Nasdaq Riga)',
    '.TL': 'Estonia (Nasdaq Tallinn)',
    '.VS': 'Lithuania (Nasdaq Vilnius)',
    '.IC': 'Iceland (Nasdaq Iceland)',
    '.CO': 'Denmark (Nasdaq Copenhagen)',
    '.HE': 'Finland (Nasdaq Helsinki)',
    '.SA': 'Brazil (B3)',
    '.MX': 'Mexico (Bolsa Mexicana)',
    '.BA': 'Argentina (Bolsa de Comercio)',
    '.SN': 'Chile (Bolsa de Santiago)',
    '.JO': 'South Africa (Johannesburg Stock Exchange)',
    '.TA': 'Israel (Tel Aviv Stock Exchange)',
    '.IS': 'Turkey (Borsa Istanbul)',
    '.ME': 'Russia (Moscow Exchange)',
}

POPULAR_STOCKS = [
    # US Stocks (no suffix needed)
    {'symbol': 'AAPL', 'name': 'Apple Inc.', 'type': 'Equity', 'region': 'United States', 'market': 'NASDAQ'},
    {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'type': 'Equity', 'region': 'United States', 'market': 'NASDAQ'},
    {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'type': 'Equity', 'region': 'United States', 'market': 'NASDAQ'},
    {'symbol': 'TSLA', 'name': 'Tesla, Inc.', 'type': 'Equity', 'region': 'United States', 'market': 'NASDAQ'},
    {'symbol': 'AMZN', 'name': 'Amazon.com, Inc.', 'type': 'Equity', 'region': 'United States', 'market': 'NASDAQ'},
    {'symbol': 'NVDA', 'name': 'NVIDIA Corporation', 'type': 'Equity', 'region': 'United States', 'market': 'NASDAQ'},
    {'symbol': 'META', 'name': 'Meta Platforms, Inc.', 'type': 'Equity', 'region': 'United States', 'market': 'NASDAQ'},
    {'symbol': 'BRK-B', 'name': 'Berkshire Hathaway Inc.', 'type': 'Equity', 'region': 'United States', 'market': 'NYSE'},
    {'symbol': 'JPM', 'name': 'JPMorgan Chase & Co.', 'type': 'Equity', 'region': 'United States', 'market': 'NYSE'},
    {'symbol': 'JNJ', 'name': 'Johnson & Johnson', 'type': 'Equity', 'region': 'United States', 'market': 'NYSE'},
    {'symbol': 'V', 'name': 'Visa Inc.', 'type': 'Equity', 'region': 'United States', 'market': 'NYSE'},
    {'symbol': 'PG', 'name': 'Procter & Gamble Company', 'type': 'Equity', 'region': 'United States', 'market': 'NYSE'},
    {'symbol': 'UNH', 'name': 'UnitedHealth Group Inc.', 'type': 'Equity', 'region': 'United States', 'market': 'NYSE'},
    {'symbol': 'HD', 'name': 'Home Depot, Inc.', 'type': 'Equity', 'region': 'United States', 'market': 'NYSE'},
    {'symbol': 'MA', 'name': 'Mastercard Incorporated', 'type': 'Equity', 'region': 'United States', 'market': 'NYSE'},
    
    # Indian Stocks
    {'symbol': 'RELIANCE.NS', 'name': 'Reliance Industries Ltd.', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    {'symbol': 'TCS.NS', 'name': 'Tata Consultancy Services Ltd.', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    {'symbol': 'HDFCBANK.NS', 'name': 'HDFC Bank Ltd.', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    {'symbol': 'INFY.NS', 'name': 'Infosys Ltd.', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    {'symbol': 'ICICIBANK.NS', 'name': 'ICICI Bank Ltd.', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    {'symbol': 'HINDUNILVR.NS', 'name': 'Hindustan Unilever Ltd.', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    {'symbol': 'SBIN.NS', 'name': 'State Bank of India', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    {'symbol': 'BHARTIARTL.NS', 'name': 'Bharti Airtel Ltd.', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    {'symbol': 'ASIANPAINT.NS', 'name': 'Asian Paints Ltd.', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    {'symbol': 'MARUTI.NS', 'name': 'Maruti Suzuki India Ltd.', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    {'symbol': 'TATAMOTORS.NS', 'name': 'Tata Motors Ltd.', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    {'symbol': 'WIPRO.NS', 'name': 'Wipro Ltd.', 'type': 'Equity', 'region': 'India', 'market': 'NSE'},
    
    # UK Stocks
    {'symbol': 'SHEL.L', 'name': 'Shell plc', 'type': 'Equity', 'region': 'United Kingdom', 'market': 'LSE'},
    {'symbol': 'AZN.L', 'name': 'AstraZeneca PLC', 'type': 'Equity', 'region': 'United Kingdom', 'market': 'LSE'},
    {'symbol': 'BP.L', 'name': 'BP p.l.c.', 'type': 'Equity', 'region': 'United Kingdom', 'market': 'LSE'},
    {'symbol': 'ULVR.L', 'name': 'Unilever PLC', 'type': 'Equity', 'region': 'United Kingdom', 'market': 'LSE'},
    
    # Canadian Stocks
    {'symbol': 'SHOP.TO', 'name': 'Shopify Inc.', 'type': 'Equity', 'region': 'Canada', 'market': 'TSX'},
    {'symbol': 'RY.TO', 'name': 'Royal Bank of Canada', 'type': 'Equity', 'region': 'Canada', 'market': 'TSX'},
    {'symbol': 'TD.TO', 'name': 'Toronto-Dominion Bank', 'type': 'Equity', 'region': 'Canada', 'market': 'TSX'},
    
    # European Stocks
    {'symbol': 'ASML.AS', 'name': 'ASML Holding N.V.', 'type': 'Equity', 'region': 'Netherlands', 'market': 'Euronext'},
    {'symbol': 'SAP.DE', 'name': 'SAP SE', 'type': 'Equity', 'region': 'Germany', 'market': 'XETRA'},
    {'symbol': 'NESN.SW', 'name': 'Nestlé S.A.', 'type': 'Equity', 'region': 'Switzerland', 'market': 'SIX'},
]

def validate_ticker_format(symbol):
    """
    Validate and suggest proper ticker format for different markets.
    Returns dict with validation result and suggestions.
    """
    if not symbol:
        return {
            'is_valid': False,
            'original': symbol,
            'suggestions': [],
            'error': 'Symbol cannot be empty'
        }
    
    symbol = symbol.strip().upper()
    original_symbol = symbol
    
    # Check if it's already a valid format
    if '.' in symbol:
        base, suffix = symbol.split('.', 1)
        if '.' + suffix in MARKET_SUFFIXES:
            return {
                'is_valid': True,
                'original': original_symbol,
                'corrected': symbol,
                'market': MARKET_SUFFIXES['.' + suffix],
                'suggestions': []
            }
    
    # For symbols without suffix, assume US market first
    suggestions = []
    
    # Check if it matches any known stocks
    exact_matches = [stock for stock in POPULAR_STOCKS if stock['symbol'].split('.')[0] == symbol]
    if exact_matches:
        for match in exact_matches:
            suggestions.append({
                'symbol': match['symbol'],
                'name': match['name'],
                'region': match['region'],
                'market': match['market'],
                'confidence': 1.0,
                'reason': 'Exact match found'
            })
    else:
        # Look for partial matches
        partial_matches = []
        for stock in POPULAR_STOCKS:
            base_symbol = stock['symbol'].split('.')[0]
            # Check similarity
            similarity = SequenceMatcher(None, symbol, base_symbol).ratio()
            if similarity > 0.6:  # 60% similarity threshold
                partial_matches.append({
                    'symbol': stock['symbol'],
                    'name': stock['name'],
                    'region': stock['region'],
                    'market': stock['market'],
                    'confidence': similarity,
                    'reason': f'Similar to {base_symbol}'
                })
        
        # Sort by confidence
        partial_matches.sort(key=lambda x: x['confidence'], reverse=True)
        suggestions.extend(partial_matches[:5])  # Top 5 matches
    
    # If no suffix provided, suggest common market variants
    if '.' not in symbol and not exact_matches:
        market_suggestions = [
            {'symbol': symbol, 'name': f'{symbol} (US Market)', 'region': 'United States', 'market': 'US', 'confidence': 0.8, 'reason': 'US market (default)'},
            {'symbol': f'{symbol}.NS', 'name': f'{symbol} (India NSE)', 'region': 'India', 'market': 'NSE', 'confidence': 0.7, 'reason': 'India National Stock Exchange'},
            {'symbol': f'{symbol}.L', 'name': f'{symbol} (London)', 'region': 'United Kingdom', 'market': 'LSE', 'confidence': 0.6, 'reason': 'London Stock Exchange'},
            {'symbol': f'{symbol}.TO', 'name': f'{symbol} (Toronto)', 'region': 'Canada', 'market': 'TSX', 'confidence': 0.6, 'reason': 'Toronto Stock Exchange'},
        ]
        suggestions.extend(market_suggestions)
    
    return {
        'is_valid': len(exact_matches) > 0,
        'original': original_symbol,
        'corrected': symbol if len(exact_matches) > 0 else None,
        'suggestions': suggestions[:8],  # Limit to 8 suggestions
        'market_info': {
            'available_markets': list(MARKET_SUFFIXES.keys()),
            'format_help': 'Use format: SYMBOL.SUFFIX (e.g., RELIANCE.NS for Indian stocks, AAPL for US stocks)'
        }
    }

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def search_stocks_enhanced(query, limit=10):
    """
    Enhanced stock search with fuzzy matching and market-specific suggestions
    """
    if not query or len(query) < 1:
        return []
    
    query = query.strip()
    results = []
    
    # Search in popular stocks database
    for stock in POPULAR_STOCKS:
        symbol_base = stock['symbol'].split('.')[0]
        name_lower = stock['name'].lower()
        query_lower = query.lower()
        
        # Exact symbol match (highest priority)
        if symbol_base.lower() == query_lower:
            results.append({
                **stock,
                'match_type': 'exact_symbol',
                'confidence': 1.0,
                'highlight': stock['symbol']
            })
        # Symbol starts with query
        elif symbol_base.lower().startswith(query_lower):
            results.append({
                **stock,
                'match_type': 'symbol_prefix',
                'confidence': 0.9,
                'highlight': stock['symbol']
            })
        # Query is in symbol
        elif query_lower in symbol_base.lower():
            results.append({
                **stock,
                'match_type': 'symbol_contains',
                'confidence': 0.8,
                'highlight': stock['symbol']
            })
        # Company name starts with query
        elif name_lower.startswith(query_lower):
            results.append({
                **stock,
                'match_type': 'name_prefix',
                'confidence': 0.7,
                'highlight': stock['name']
            })
        # Query is in company name
        elif query_lower in name_lower:
            results.append({
                **stock,
                'match_type': 'name_contains',
                'confidence': 0.6,
                'highlight': stock['name']
            })
        # Fuzzy match for typos
        elif (similarity(query_lower, symbol_base.lower()) > 0.7 or 
              similarity(query_lower, name_lower) > 0.5):
            results.append({
                **stock,
                'match_type': 'fuzzy',
                'confidence': max(similarity(query_lower, symbol_base.lower()), 
                                 similarity(query_lower, name_lower)),
                'highlight': stock['symbol'] if similarity(query_lower, symbol_base.lower()) > 0.7 else stock['name']
            })
    
    # Remove duplicates and sort by confidence
    seen = set()
    unique_results = []
    for result in results:
        if result['symbol'] not in seen:
            seen.add(result['symbol'])
            unique_results.append(result)
    
    # Sort by confidence (descending) and then by match type priority
    match_type_priority = {
        'exact_symbol': 1,
        'symbol_prefix': 2,
        'symbol_contains': 3,
        'name_prefix': 4,
        'name_contains': 5,
        'fuzzy': 6
    }
    
    unique_results.sort(key=lambda x: (match_type_priority[x['match_type']], -x['confidence']))
    
    return unique_results[:limit]

if __name__ == '__main__':
    print("🚀 Starting Bridge Server for Next.js Frontend")
    print(f"Backend modules available: {BACKEND_AVAILABLE}")
    print("Server will run on http://localhost:5001")
    print("Make sure your Next.js app is configured to proxy API calls to this server")
    
    app.run(debug=True, port=5001, host='0.0.0.0')
