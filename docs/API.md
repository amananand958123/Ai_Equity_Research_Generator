# API Documentation

## Overview

The Equity Research Report Generator provides a RESTful API for generating comprehensive equity research reports. The API is built with Flask and offers endpoints for data retrieval, analysis, and report generation.

## Base URL

```
http://localhost:5001/api
```

## Authentication

Currently, the API does not require authentication for local development. API keys are configured through environment variables for external services.

## Endpoints

### Stock Data

#### Get Stock Data
```http
GET /api/stock-data/{symbol}
```

Retrieves comprehensive stock data including current price, financial metrics, and company information.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol (e.g., "AAPL", "MSFT")

**Response:**
```json
{
  "symbol": "AAPL",
  "currentPrice": 175.43,
  "marketCap": 2800000000000,
  "peRatio": 28.5,
  "dividendYield": 0.015,
  "52WeekHigh": 198.23,
  "52WeekLow": 164.08,
  "companyName": "Apple Inc.",
  "sector": "Technology",
  "industry": "Consumer Electronics"
}
```

#### Search Stocks
```http
GET /api/search-stocks?q={query}
```

Searches for stock symbols based on company name or ticker.

**Parameters:**
- `q` (string, required): Search query

**Response:**
```json
{
  "results": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "exchange": "NASDAQ",
      "confidence": 0.98
    }
  ]
}
```

### Report Generation

#### Generate PDF Report
```http
POST /api/generate-pdf
```

Generates a comprehensive PDF equity research report.

**Request Body:**
```json
{
  "symbol": "AAPL",
  "analysisType": "comprehensive"
}
```

**Response:**
- Content-Type: `application/pdf`
- Binary PDF data

#### Get Chart Data
```http
GET /api/chart-data/{symbol}
```

Retrieves chart data for stock price visualization.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol
- `period` (string, optional): Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

**Response:**
```json
{
  "symbol": "AAPL",
  "data": [
    {
      "date": "2025-01-01",
      "open": 170.25,
      "high": 175.43,
      "low": 169.87,
      "close": 174.32,
      "volume": 52467800
    }
  ]
}
```

### News and Analysis

#### Get Financial News
```http
GET /api/news/{symbol}
```

Retrieves recent financial news for a stock with sentiment analysis.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol
- `limit` (integer, optional): Number of articles to return (default: 10)

**Response:**
```json
{
  "symbol": "AAPL",
  "articles": [
    {
      "title": "Apple Reports Strong Q4 Earnings",
      "description": "Apple Inc. reported better-than-expected earnings...",
      "url": "https://example.com/article",
      "publishedAt": "2025-01-15T10:30:00Z",
      "sentiment": "positive",
      "sentimentScore": 0.75
    }
  ]
}
```

#### Get AI Analysis
```http
GET /api/analysis/{symbol}
```

Retrieves AI-powered analysis and insights for a stock.

**Parameters:**
- `symbol` (string, required): Stock ticker symbol

**Response:**
```json
{
  "symbol": "AAPL",
  "recommendation": "BUY",
  "targetPrice": 195.00,
  "confidence": 0.85,
  "analysis": "Strong fundamentals with solid growth prospects...",
  "keyPoints": [
    "Strong revenue growth",
    "Excellent profit margins", 
    "Market leadership position"
  ]
}
```

### System Status

#### Check Status
```http
GET /api/status
```

Checks the health and status of the API service.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-01-15T10:30:00Z",
  "services": {
    "dataProvider": "operational",
    "aiService": "operational",
    "pdfGenerator": "operational"
  }
}
```

## Error Handling

The API uses standard HTTP status codes and returns error information in JSON format.

### Error Response Format
```json
{
  "error": {
    "code": "INVALID_SYMBOL",
    "message": "The provided stock symbol is not valid",
    "details": "Symbol 'XYZ123' could not be found"
  }
}
```

### Common Status Codes
- `200` - Success
- `400` - Bad Request
- `404` - Not Found
- `429` - Rate Limit Exceeded
- `500` - Internal Server Error
- `503` - Service Unavailable

## Rate Limiting

The API implements rate limiting to ensure fair usage:
- **Public endpoints**: 100 requests per minute per IP
- **Report generation**: 10 requests per minute per IP
- **News/Analysis**: 50 requests per minute per IP

## Examples

### Generate Report for Apple
```bash
curl -X POST http://localhost:5001/api/generate-pdf \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}' \
  -o "apple_report.pdf"
```

### Get Microsoft Stock Data
```bash
curl "http://localhost:5001/api/stock-data/MSFT"
```

### Search for Tesla
```bash
curl "http://localhost:5001/api/search-stocks?q=tesla"
```

## SDKs and Libraries

### Python
```python
import requests

# Generate report
response = requests.post(
    'http://localhost:5001/api/generate-pdf',
    json={'symbol': 'AAPL'}
)

with open('report.pdf', 'wb') as f:
    f.write(response.content)
```

### JavaScript/Node.js
```javascript
// Get stock data
const response = await fetch('http://localhost:5001/api/stock-data/AAPL');
const data = await response.json();
console.log(data);
```

## Changelog

### v1.0.0
- Initial API release
- Basic stock data endpoints
- PDF report generation
- News and sentiment analysis
- AI-powered insights
