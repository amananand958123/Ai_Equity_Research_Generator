# Frequently Asked Questions

## General Questions

### What is the Equity Research Report Generator?
The Equity Research Report Generator is an AI-powered platform that creates comprehensive equity research reports for educational purposes. It combines real-time financial data with intelligent analysis to produce institutional-grade investment research reports.

### Is this tool free to use?
Yes, the tool is open-source and free to use for educational purposes. However, you'll need to obtain API keys from third-party services (Google Gemini, Alpha Vantage, NewsAPI) which may have their own pricing structures.

### Can I use this for actual investment decisions?
**No.** This tool is designed exclusively for educational and academic purposes. It should not be used for actual investment decisions. Always consult with qualified financial advisors before making investment choices.

## Technical Questions

### What programming languages and frameworks are used?
- **Backend**: Python 3.8+ with Flask
- **Frontend**: Next.js 15 with TypeScript
- **Data Processing**: pandas, numpy
- **AI Analysis**: Google Gemini API
- **PDF Generation**: WeasyPrint
- **Charts**: Plotly.js

### What data sources does the tool use?
- **Yahoo Finance**: Primary financial data and stock prices
- **Alpha Vantage**: Additional financial metrics
- **NewsAPI**: Financial news and sentiment analysis
- **Google Gemini**: AI-powered insights and analysis

### How accurate is the financial data?
The tool uses publicly available financial data from reputable sources like Yahoo Finance. However, data accuracy depends on the source providers and may have delays. Always verify critical information from official company filings.

## Setup and Installation

### What are the system requirements?
- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.8 or higher
- **Node.js**: Version 16 or higher
- **Memory**: At least 4GB RAM recommended
- **Storage**: 2GB free space for dependencies

### How do I get the required API keys?
1. **Google Gemini**: Visit [Google AI Studio](https://aistudio.google.com/)
2. **Alpha Vantage**: Sign up at [Alpha Vantage](https://www.alphavantage.co/)
3. **NewsAPI**: Register at [NewsAPI](https://newsapi.org/)

Follow the setup instructions in each service's documentation.

### The installation fails. What should I do?
1. **Check Python version**: Ensure you're using Python 3.8+
2. **Update pip**: Run `pip install --upgrade pip`
3. **Virtual environment**: Always use a virtual environment
4. **Dependencies**: Install requirements with `pip install -r requirements.txt`
5. **Permissions**: Ensure you have write permissions in the directory

### How do I update the application?
```bash
git pull origin main
pip install -r requirements.txt
cd frontend && npm install
```

## Usage Questions

### Which stock markets are supported?
The tool supports major global markets including:
- **United States**: NYSE, NASDAQ
- **India**: NSE, BSE
- **United Kingdom**: LSE
- **Canada**: TSX
- **Europe**: Various European exchanges

### How long does it take to generate a report?
Report generation typically takes 30-60 seconds, depending on:
- Data availability for the stock
- AI analysis complexity
- Network speed for API calls
- System performance

### Can I generate reports for multiple stocks at once?
Currently, the tool generates reports for one stock at a time. Batch processing is planned for future versions.

### What if a stock symbol isn't found?
- **Check the symbol**: Ensure you're using the correct ticker
- **Try different formats**: Some stocks may require exchange suffixes (e.g., "RELIANCE.NS" for NSE)
- **Use search**: Try the search function to find the correct symbol
- **Check market**: Ensure the stock is from a supported market

## Report Questions

### What sections are included in the reports?
Each report contains 13 comprehensive sections:
1. Executive Summary
2. Business Overview
3. Financial Snapshot
4. Key Metrics
5. Strategic Highlights
6. Quarterly Performance
7. Industry Overview
8. Brand Portfolio
9. Management Commentary
10. Financial Ratios
11. DuPont Analysis
12. Ratings Rationale
13. Educational Disclaimer

### Can I customize the reports?
Currently, reports use a standard template. Customization features are planned for future releases. You can modify the code directly if you have programming experience.

### How are the investment ratings determined?
Ratings are based on a scoring system that evaluates:
- Revenue growth trends
- Profitability metrics
- Financial strength indicators
- Market position factors

The system assigns a composite score that translates to BUY, HOLD, or SELL recommendations.

### Are the AI insights reliable?
AI insights are generated using Google's Gemini model based on available financial data. While sophisticated, these should be considered as supplementary information rather than definitive investment advice.

## Troubleshooting

### The backend server won't start
1. **Check Python environment**: Ensure virtual environment is activated
2. **Verify dependencies**: Run `pip install -r requirements.txt`
3. **Check ports**: Ensure port 5001 isn't in use by another application
4. **Environment variables**: Verify your `.env` file is properly configured

### The frontend won't load
1. **Check Node.js version**: Ensure you're using Node.js 16+
2. **Install dependencies**: Run `npm install` in the frontend directory
3. **Check ports**: Ensure port 3000 isn't in use
4. **Clear cache**: Try `npm run build` and restart

### API calls are failing
1. **Check API keys**: Verify all keys are properly set in `.env`
2. **Check internet connection**: Ensure you can reach external APIs
3. **Check rate limits**: You may have exceeded API rate limits
4. **Check service status**: External APIs may be temporarily down

### PDF generation isn't working
1. **Check WeasyPrint**: Ensure WeasyPrint is properly installed
2. **System dependencies**: WeasyPrint may require additional system libraries
3. **Font issues**: Some systems may need additional font packages
4. **Memory**: Large reports may require more available memory

## Contributing

### How can I contribute to the project?
See our [Contributing Guidelines](../CONTRIBUTING.md) for detailed information on:
- Reporting issues
- Suggesting enhancements
- Submitting pull requests
- Development setup

### I found a bug. How do I report it?
1. **Search existing issues** first to avoid duplicates
2. **Create a new issue** on GitHub
3. **Provide details**: Include steps to reproduce, expected vs actual behavior
4. **Include environment info**: OS, Python version, Node.js version

### Can I suggest new features?
Absolutely! Check our [roadmap](../README.md#roadmap) and create an issue with the "enhancement" label to suggest new features.

## Support

### Where can I get help?
- **Documentation**: Check the [docs/](.) directory
- **GitHub Issues**: Create an issue for bugs or questions
- **GitHub Discussions**: Use for general questions and community support

### Is commercial support available?
This is an open-source project maintained by volunteers. Commercial support is not currently available, but the community is active and helpful.

---

**Don't see your question here?** [Create an issue](https://github.com/yourusername/equity-research-generator/issues) and we'll add it to the FAQ!
