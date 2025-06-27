# 🚀 Equity Research Report Generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue.svg)](https://www.typescriptlang.org/)

A comprehensive AI-powered equity research report generator that creates institutional-grade investment analysis reports using real-time financial data and intelligent insights.

![Demo Screenshot](docs/demo-screenshot.png)

## 🌟 Features

### 📊 Comprehensive Analysis
- **13-Section Professional Reports** - Complete equity research coverage
- **Real-Time Financial Data** - Live market data and company fundamentals
- **AI-Powered Insights** - Google Gemini 2.0 Flash integration
- **Multi-Asset Support** - Global stocks across major exchanges
- **Interactive Charts** - Dynamic visualizations with Plotly.js

### 🔧 Technical Capabilities
- **Modern Tech Stack** - Next.js 15, Python 3.8+, TypeScript
- **Multi-Source Data** - Yahoo Finance, Alpha Vantage, NewsAPI
- **Professional PDF Generation** - WeasyPrint formatting
- **Responsive Design** - Mobile-friendly interface
- **API-First Architecture** - RESTful endpoints for integration

### 🎯 Report Sections
1. **Executive Summary** - Key metrics and investment thesis
2. **Business Overview** - Company fundamentals and operations
3. **Financial Snapshot** - 4-year financial history with projections
4. **Key Metrics** - Profitability, efficiency, and growth ratios
5. **Strategic Highlights** - Business strategy and competitive advantages
6. **Quarterly Performance** - Recent quarterly financial analysis
7. **Industry Overview** - Sector analysis and market positioning
8. **Brand Portfolio** - Geographic and business segment breakdown
9. **Management Commentary** - Leadership assessment and strategy
10. **Financial Ratios** - Comprehensive ratio analysis
11. **DuPont Analysis** - ROE decomposition and efficiency metrics
12. **Ratings Rationale** - Investment recommendation methodology
13. **Educational Disclaimer** - Academic purpose statements

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** with Flask framework
- **yfinance** for real-time financial data
- **pandas & numpy** for data processing
- **WeasyPrint** for professional PDF generation
- **Google Gemini API** for AI-powered analysis

### Frontend
- **Next.js 15** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for modern styling
- **Plotly.js** for interactive charts
- **Framer Motion** for smooth animations

### APIs & Data Sources
- **Yahoo Finance** - Primary financial data
- **Alpha Vantage** - Additional market metrics
- **NewsAPI** - Sentiment analysis
- **Google Gemini 2.0 Flash** - AI insights

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- API keys for Google Gemini, Alpha Vantage, NewsAPI

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/equity-research-generator.git
cd equity-research-generator

# Backend setup
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cd ..

# Environment configuration
cp .env.example .env
# Edit .env with your API keys
```

### Environment Variables
Create a `.env` file in the root directory:

```env
GOOGLE_API_KEY=your_gemini_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
NEWS_API_KEY=your_news_api_key
FRONTEND_PORT=3000
BACKEND_PORT=5001
```

### Run the Application

```bash
# Start both servers (recommended)
./start-servers.sh

# Or start individually:
# Backend: python bridge_server.py
# Frontend: cd frontend && npm run dev
```

Visit `http://localhost:3000` to access the application.

## 📖 Usage

### Web Interface
1. Open `http://localhost:3000`
2. Search for any stock symbol (e.g., AAPL, MSFT, GOOGL)
3. Click "Generate Report" to create a comprehensive analysis
4. Download the PDF or view the interactive report

### API Usage
```bash
# Generate PDF report
curl -X POST http://localhost:5001/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}' \
  -o "apple_report.pdf"

# Get stock data
curl "http://localhost:5001/api/stock-data/AAPL"

# Search stocks
curl "http://localhost:5001/api/search-stocks?q=apple"
```

### Python Script
```python
from comprehensive_report_generator import comprehensive_generator

# Generate HTML report
html_content = comprehensive_generator.generate_comprehensive_report('AAPL')

# Generate PDF
pdf_bytes = comprehensive_generator.generate_pdf_bytes(html_content)
with open('report.pdf', 'wb') as f:
    f.write(pdf_bytes)
```

## 🧪 Testing

```bash
# Test all API endpoints
./test-api.sh

# Verify report content quality
python verify_report_content.py

# Run comprehensive tests
python -m pytest tests/
```

## 📁 Project Structure

```
equity-research-generator/
├── 📄 bridge_server.py              # Flask API server
├── 📄 comprehensive_report_generator.py  # Core report engine  
├── 📄 data_aggregator.py            # Data collection & processing
├── 📄 advanced_visualizer.py        # Chart generation
├── 📄 requirements.txt              # Python dependencies
├── 📄 start-servers.sh              # Launch script
├── 📁 frontend/                     # Next.js application
│   ├── 📁 src/
│   │   ├── 📁 app/                  # App router pages
│   │   ├── 📁 components/           # React components
│   │   └── 📁 api/                  # API route handlers
│   ├── 📄 package.json
│   ├── 📄 next.config.ts
│   └── 📄 tailwind.config.ts
├── 📁 docs/                         # Documentation
├── 📄 .env.example                  # Environment template
├── 📄 .gitignore
└── 📄 README.md
```

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/stock-data/{symbol}` | GET | Get comprehensive stock data |
| `/api/generate-pdf` | POST | Generate PDF report |
| `/api/search-stocks` | GET | Search stock symbols |
| `/api/news/{symbol}` | GET | Get financial news |
| `/api/analysis/{symbol}` | GET | Get AI analysis |
| `/api/chart-data/{symbol}` | GET | Get chart data |
| `/api/status` | GET | Check service status |

## 🎨 Sample Reports

The generator produces professional reports with:
- **Executive Summary** with key investment metrics
- **Detailed Financial Analysis** with 4-year trends
- **Industry Positioning** and competitive analysis  
- **Management Assessment** and strategic outlook
- **Investment Rating** with supporting rationale
- **Risk Analysis** and market positioning

[View Sample Report](docs/sample-report.pdf)

## 🤝 Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md).

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**EDUCATIONAL PURPOSE ONLY** - This application is designed exclusively for educational and academic purposes. It is not intended as investment advice, financial guidance, or a recommendation to buy, sell, or hold any securities. All investment decisions should be made in consultation with qualified financial advisors.

## 🆘 Support

- 📋 [Create an Issue](https://github.com/yourusername/equity-research-generator/issues)
- 📖 [Read the Docs](docs/)
- 💬 [Discussions](https://github.com/yourusername/equity-research-generator/discussions)

## 🗺️ Roadmap

- [ ] **ESG Analysis** - Environmental, Social, Governance metrics
- [ ] **Sector Comparison** - Peer analysis and benchmarking
- [ ] **International Markets** - Additional exchange support
- [ ] **Mobile App** - React Native application
- [ ] **Real-time Alerts** - Price and news notifications
- [ ] **Portfolio Analysis** - Multi-stock portfolio reports
- [ ] **Options Analysis** - Derivatives and options data
- [ ] **Crypto Support** - Digital asset analysis

---

⭐ **Star this repo if you find it useful!** ⭐

Built with ❤️ by [Your Name]
