#  Equity Research Report Generator

A comprehensive, AI-powered platform for generating educational equity research reports with real-time market data, intelligent stock search, and advanced analytics.

## ✨ Key Features

### 🔍 Intelligent Stock Search
- **Smart Search**: Advanced fuzzy search with auto-suggestions
- **Format Validation**: Intelligent ticker format suggestions and corrections
- **Multi-Market Support**: US, India, UK, Canada, and international markets
- **Confidence Indicators**: Search results with match confidence scores

### 📊 Real-time Market Data
- **Live Stock Prices**: Real-time data from Yahoo Finance
- **Key Metrics**: Market cap, PE ratios, 52-week ranges, volume
- **International Markets**: Support for global stock exchanges
- **Market Information**: Exchange details and currency information

### 🤖 AI-Powered Analysis
- **Google Gemini AI**: Advanced market analysis and insights
- **Sentiment Analysis**: News sentiment with confidence scores
- **Investment Recommendations**: AI-generated buy/hold/sell recommendations
- **Target Pricing**: Intelligent price target calculations

### � Interactive Features
- **Dynamic Charts**: Real-time price and volume charts
- **Professional Dashboard**: Modern, responsive interface
- **News Integration**: Latest news with sentiment analysis
- **PDF Reports**: Comprehensive, downloadable research reports

### 🛠 Technical Excellence
- **Next.js 15**: Modern React framework with App Router
- **TypeScript**: Full type safety and better development experience
- **Flask Backend**: Robust Python API server
- **Error Handling**: Graceful error handling with helpful suggestions

## 📊 Comprehensive Educational Reports

### Report Structure (13 Sections)
1. **Header** - Company info, sector, target price, disclaimers
2. **About the Business** - Company overview, subsidiaries, global presence
3. **Financial Snapshot** - 4-year financials + projections, shareholding pattern
4. **Key Financial Metrics** - ROE, ROA, margins, dividend yield
5. **Strategic Highlights** - Growth initiatives, capex, sustainability
6. **Quarterly Performance** - Recent results and segment analysis
7. **Industry Overview** - Market position, competitive advantages
8. **Brand Portfolio** - Geographic breakdown and brand analysis
9. **Management Commentary** - Key insights from leadership
10. **Financial Ratios Table** - Complete ratio analysis (valuation, liquidity, solvency)
11. **DuPont Analysis** - ROE decomposition and component analysis
12. **Ratings Rationale** - Credit ratings and agency analysis
13. **Educational Disclaimer** - Academic purpose and risk warnings

### Key Features
- **Real-time Data Integration**: Live financial metrics and market data
- **Professional PDF Generation**: Academic-style formatting with proper citations
- **DuPont Analysis**: Complete ROE breakdown with interpretation
- **Comprehensive Ratios**: 15+ financial ratios with industry context
- **Educational Focus**: Designed for academic use with proper disclaimers

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Internet connection
- Google Gemini API key (free)

### Installation

1. **Clone or download the project**
   ```bash
   # Navigate to the project directory
   cd equity-research-generator
   ```

2. **Set up the Python virtual environment** (REQUIRED)
   ```bash
   # Option A: Use the automated setup script (RECOMMENDED)
   chmod +x activate_venv.sh
   ./activate_venv.sh
   
   # Option B: Manual setup
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Get your Gemini API key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key (free)
   - Create a `.env` file: `cp .env.example .env`
   - Add your API key to the `.env` file: `GOOGLE_API_KEY=your_api_key_here`

4. **Run the application**
   ```bash
   # Quick start (starts both frontend and backend)
   chmod +x start.sh
   ./start.sh
   
   # Then open your browser to: http://localhost:3000
   ```

## �️ Modern Next.js Frontend

This project features a modern, professional Next.js frontend with:
- 🎨 Beautiful, responsive UI with Tailwind CSS
- 📊 Interactive charts with Plotly.js and Recharts
- 🔍 Smart stock search with auto-suggestions
- 📱 Mobile-friendly design
- ⚡ Real-time data updates
- 📄 PDF report generation

## 🐍 Virtual Environment
source .venv/bin/activate

# Deactivate (when you're done)
deactivate

# Verify you're in the virtual environment
which python  # Should show .venv/bin/python

# Test all dependencies are working
python test_venv.py
```

## 📖 How to Use

1. **Open the app** in your browser (usually http://localhost:8501)
2. **Enter your Gemini API key** in the sidebar
3. **Type a stock ticker** (e.g., AAPL, GOOGL, TSLA)
4. **Click "Generate Report"** and wait for analysis
5. **Download your report** using the download button

## 📊 Sample Report Sections

The generated reports include:

## 📖 How to Use

1. **Start the application**
   ```bash
   ./start.sh
   ```

2. **Open your browser** to [http://localhost:3000](http://localhost:3000)

3. **Search for a stock**
   - Type a stock ticker (e.g., AAPL, GOOGL, TSLA)
   - Or try Indian stocks with .NS suffix (e.g., TATAMOTORS.NS)
   - Select from the auto-suggestions

4. **Choose analysis level**
   - **Basic**: Core analysis with AI insights
   - **Enhanced**: Multi-source data with charts (recommended)
   - **Comprehensive**: Full institutional-grade report

5. **Generate your report**
   - View real-time data and interactive charts
   - Read AI-powered analysis and insights
   - Download comprehensive PDF reports

## 📊 Sample Report Sections

The generated reports include:

- **Executive Summary**: Key highlights and recommendations
- **Company Overview**: Business model and market position
- **Financial Analysis**: Complete ratio analysis and DuPont breakdown
- **Investment Thesis**: Growth drivers and opportunities
- **Risks & Challenges**: Potential concerns and market risks
- **Valuation & Recommendation**: Price targets and ratings

## 🔧 Technical Architecture

### Frontend (Next.js)
- **React Components**: Modern, responsive UI components
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Plotly.js**: Interactive financial charts

### Backend (Python)
- **Flask Bridge Server**: API layer connecting frontend to Python modules
- **yfinance**: Yahoo Finance data API
- **google-generativeai**: Google Gemini API client
- **pandas**: Data manipulation and analysis

### API Limits (Free Tier)
- **Gemini API**: 15 requests per minute, 1M tokens per day
- **Yahoo Finance**: No official limits (fair use policy)

### Supported Stock Exchanges
- US stocks (NASDAQ, NYSE)
- Indian stocks (.NS suffix)
- International stocks with Yahoo Finance coverage
- Major indices and ETFs
- [x] Simple Gemini Integration
- [x] Basic Streamlit UI
- [x] Basic Output formatting
- [x] Error handling
- [x] Company ticker input
- [x] Generate report button
- [x] Display generated text
- [x] Simple text formatting
- [x] Basic error messages

**Expected Output**: ✅ Simple web app that generates basic company reports
**Time Investment**: ✅ 2-4 hours
**Skill Level Required**: ✅ Beginner Python
**Free Resources Used**: ✅ yfinance, Gemini free tier, Streamlit

## 🔄 Next Steps (Level 2)

For enhanced functionality, consider implementing:

- [ ] Multi-source data integration (Alpha Vantage, NewsAPI)
- [ ] PDF export functionality
- [ ] Basic charts and visualizations
- [ ] Sentiment analysis integration
- [ ] Enhanced UI/UX with loading indicators
- [ ] Data validation and cleaning

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure virtual environment is activated
   source .venv/bin/activate
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

2. **API Key Issues**
   - Ensure you have a valid Gemini API key
   - Check if you've exceeded rate limits (15 RPM)
   - Verify internet connection

3. **Stock Ticker Not Found**
   - Use correct ticker symbols (e.g., AAPL not Apple)
   - Check if the stock is listed on supported exchanges
   - Try different ticker formats (e.g., .NS for Indian stocks)

4. **Frontend/Backend Connection Issues**
   ```bash
   # Make sure both services are running
   ./start.sh
   
   # Check if backend is responding
   curl http://localhost:5000/api/health
   
   # Check frontend at http://localhost:3000
   ```

## 📝 License

This project is for educational purposes. Please ensure compliance with:
- Yahoo Finance Terms of Service
- Google Gemini API Terms of Service
- Financial regulations in your jurisdiction

## 🤝 Contributing

This is a Level 1 implementation from the workflow. Contributions for Level 2+ features are welcome!

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Ensure all dependencies are installed
3. Verify API keys and internet connection
4. Check the console for detailed error messages

---

**Disclaimer**: This tool is for educational and research purposes only. Not intended as financial advice. Always consult with qualified financial professionals before making investment decisions.
