"""
Advanced Data Aggregator for Level 2 & 3 Implementation
Handles multiple data sources: yfinance, Alpha Vantage, NewsAPI, Reddit
"""

import yfinance as yf
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from typing import Dict, List, Optional, Tuple
import time
import asyncio
import aiohttp
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

class AdvancedDataAggregator:
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.newsapi_key = os.getenv('NEWSAPI_KEY')
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        
        # Sentiment analyzers
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize FinBERT for financial sentiment (will download on first use)
        try:
            self.finbert_analyzer = pipeline("sentiment-analysis", 
                                            model="ProsusAI/finbert",
                                            return_all_scores=True)
        except:
            self.finbert_analyzer = None
        
        # Rate limiting trackers
        self.last_alpha_vantage_call = 0
        self.last_newsapi_call = 0
        self.alpha_vantage_calls_today = 0
        self.newsapi_calls_today = 0
        self.call_date = datetime.now().date()
    
    def check_rate_limits(self):
        """Reset daily counters if new day"""
        current_date = datetime.now().date()
        if current_date != self.call_date:
            self.alpha_vantage_calls_today = 0
            self.newsapi_calls_today = 0
            self.call_date = current_date
    
    async def get_enhanced_financial_data(self, ticker: str) -> Dict:
        """Get comprehensive financial data from multiple sources"""
        self.check_rate_limits()
        
        data = {
            'yfinance_data': {},
            'alpha_vantage_data': {},
            'financial_ratios': {},
            'technical_indicators': {},
            'error_log': []
        }
        
        # Yahoo Finance data (primary source)
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get historical data
            hist_1y = stock.history(period="1y")
            hist_5y = stock.history(period="5y")
            
            # Get financial statements
            financials = stock.financials
            balance_sheet = stock.balance_sheet
            cashflow = stock.cashflow
            
            data['yfinance_data'] = {
                'info': info,
                'historical_1y': hist_1y,
                'historical_5y': hist_5y,
                'financials': financials,
                'balance_sheet': balance_sheet,
                'cashflow': cashflow,
                'recommendations': stock.recommendations,
                'calendar': stock.calendar,
                'institutional_holders': stock.institutional_holders,
                'major_holders': stock.major_holders
            }
            
        except Exception as e:
            data['error_log'].append(f"YFinance error: {str(e)}")
        
        # Alpha Vantage data (if API key available and under limits)
        if (self.alpha_vantage_key and 
            self.alpha_vantage_calls_today < 25 and 
            time.time() - self.last_alpha_vantage_call > 12):  # 5 calls per minute max
            
            try:
                # Get overview data
                overview_url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={self.alpha_vantage_key}"
                response = requests.get(overview_url, timeout=10)
                
                if response.status_code == 200:
                    overview_data = response.json()
                    if 'Symbol' in overview_data:
                        data['alpha_vantage_data']['overview'] = overview_data
                        self.alpha_vantage_calls_today += 1
                        self.last_alpha_vantage_call = time.time()
                
                # Get technical indicators if we have calls left
                if self.alpha_vantage_calls_today < 24:
                    time.sleep(12)  # Rate limit compliance
                    
                    # RSI
                    rsi_url = f"https://www.alphavantage.co/query?function=RSI&symbol={ticker}&interval=daily&time_period=14&series_type=close&apikey={self.alpha_vantage_key}"
                    rsi_response = requests.get(rsi_url, timeout=10)
                    
                    if rsi_response.status_code == 200:
                        rsi_data = rsi_response.json()
                        if 'Technical Analysis: RSI' in rsi_data:
                            data['technical_indicators']['rsi'] = rsi_data['Technical Analysis: RSI']
                            self.alpha_vantage_calls_today += 1
                
            except Exception as e:
                data['error_log'].append(f"Alpha Vantage error: {str(e)}")
        
        # Calculate enhanced financial ratios
        try:
            data['financial_ratios'] = self.calculate_enhanced_ratios(data['yfinance_data'])
        except Exception as e:
            data['error_log'].append(f"Financial ratios calculation error: {str(e)}")
        
        return data
    
    def calculate_enhanced_ratios(self, yf_data: Dict) -> Dict:
        """Calculate comprehensive financial ratios"""
        info = yf_data.get('info', {})
        financials = yf_data.get('financials', pd.DataFrame())
        balance_sheet = yf_data.get('balance_sheet', pd.DataFrame())
        cashflow = yf_data.get('cashflow', pd.DataFrame())
        
        ratios = {}
        
        try:
            # Basic ratios from info
            ratios['valuation'] = {
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'peg_ratio': info.get('pegRatio'),
                'price_to_book': info.get('priceToBook'),
                'price_to_sales': info.get('priceToSalesTrailing12Months'),
                'ev_to_ebitda': info.get('enterpriseToEbitda'),
                'ev_to_revenue': info.get('enterpriseToRevenue')
            }
            
            ratios['profitability'] = {
                'gross_margin': info.get('grossMargins'),
                'operating_margin': info.get('operatingMargins'),
                'profit_margin': info.get('profitMargins'),
                'roe': info.get('returnOnEquity'),
                'roa': info.get('returnOnAssets'),
                'roic': info.get('returnOnAssets')  # Approximation
            }
            
            ratios['liquidity'] = {
                'current_ratio': info.get('currentRatio'),
                'quick_ratio': info.get('quickRatio'),
                'cash_ratio': info.get('totalCashPerShare')
            }
            
            ratios['leverage'] = {
                'debt_to_equity': info.get('debtToEquity'),
                'debt_to_assets': None,  # Calculate from balance sheet
                'interest_coverage': None  # Calculate from financials
            }
            
            # Calculate ratios from financial statements if available
            if not financials.empty and len(financials.columns) > 0:
                latest_year = financials.columns[0]
                
                # Interest coverage ratio
                operating_income = financials.loc['Operating Income', latest_year] if 'Operating Income' in financials.index else None
                interest_expense = financials.loc['Interest Expense', latest_year] if 'Interest Expense' in financials.index else None
                
                if operating_income and interest_expense and interest_expense != 0:
                    ratios['leverage']['interest_coverage'] = abs(operating_income / interest_expense)
            
            # Growth ratios (calculate from historical data)
            if not financials.empty and len(financials.columns) >= 2:
                try:
                    current_revenue = financials.loc['Total Revenue', financials.columns[0]]
                    previous_revenue = financials.loc['Total Revenue', financials.columns[1]]
                    
                    ratios['growth'] = {
                        'revenue_growth_yoy': ((current_revenue - previous_revenue) / previous_revenue) if previous_revenue != 0 else None,
                        'revenue_growth_cagr': self.calculate_cagr(financials.loc['Total Revenue']) if len(financials.columns) >= 3 else None
                    }
                except:
                    ratios['growth'] = {'revenue_growth_yoy': None, 'revenue_growth_cagr': None}
            
        except Exception as e:
            ratios['calculation_error'] = str(e)
        
        return ratios
    
    def calculate_cagr(self, series: pd.Series) -> Optional[float]:
        """Calculate Compound Annual Growth Rate"""
        try:
            values = series.dropna()
            if len(values) >= 2:
                start_value = values.iloc[-1]  # Oldest value
                end_value = values.iloc[0]     # Most recent value
                periods = len(values) - 1
                
                if start_value > 0:
                    cagr = (end_value / start_value) ** (1/periods) - 1
                    return cagr
        except:
            pass
        return None
    
    async def get_news_sentiment(self, company_name: str, ticker: str) -> Dict:
        """Get news and sentiment analysis from multiple sources"""
        self.check_rate_limits()
        
        sentiment_data = {
            'news_articles': [],
            'sentiment_summary': {},
            'source_breakdown': {},
            'error_log': []
        }
        
        # NewsAPI data (if available and under limits)
        if (self.newsapi_key and 
            self.newsapi_calls_today < 1000 and 
            time.time() - self.last_newsapi_call > 1):
            
            try:
                # Search for company news
                from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
                
                url = f"https://newsapi.org/v2/everything?q={company_name}&from={from_date}&sortBy=relevancy&language=en&apikey={self.newsapi_key}"
                
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    news_data = response.json()
                    articles = news_data.get('articles', [])[:20]  # Limit to 20 articles
                    
                    for article in articles:
                        sentiment_data['news_articles'].append({
                            'title': article.get('title', ''),
                            'description': article.get('description', ''),
                            'url': article.get('url', ''),
                            'source': article.get('source', {}).get('name', ''),
                            'published_at': article.get('publishedAt', ''),
                            'content': article.get('content', '')
                        })
                    
                    self.newsapi_calls_today += 1
                    self.last_newsapi_call = time.time()
                
            except Exception as e:
                sentiment_data['error_log'].append(f"NewsAPI error: {str(e)}")
        
        # Analyze sentiment of collected articles
        if sentiment_data['news_articles']:
            try:
                sentiment_data['sentiment_summary'] = self.analyze_sentiment(sentiment_data['news_articles'])
            except Exception as e:
                sentiment_data['error_log'].append(f"Sentiment analysis error: {str(e)}")
        
        return sentiment_data
    
    def analyze_sentiment(self, articles: List[Dict]) -> Dict:
        """Analyze sentiment using VADER and FinBERT"""
        vader_scores = []
        finbert_scores = []
        
        for article in articles:
            text = f"{article.get('title', '')} {article.get('description', '')}"
            
            if text.strip():
                # VADER sentiment
                vader_score = self.vader_analyzer.polarity_scores(text)
                vader_scores.append(vader_score)
                
                # FinBERT sentiment (if available)
                if self.finbert_analyzer:
                    try:
                        finbert_result = self.finbert_analyzer(text[:512])  # Limit text length
                        finbert_scores.append(finbert_result[0])
                    except:
                        pass
        
        # Calculate summary statistics
        summary = {
            'total_articles': len(articles),
            'vader_sentiment': self.summarize_vader_scores(vader_scores),
            'finbert_sentiment': self.summarize_finbert_scores(finbert_scores) if finbert_scores else None
        }
        
        return summary
    
    def summarize_vader_scores(self, scores: List[Dict]) -> Dict:
        """Summarize VADER sentiment scores"""
        if not scores:
            return {}
        
        compound_scores = [score['compound'] for score in scores]
        
        avg_compound = sum(compound_scores) / len(compound_scores)
        
        # Classify overall sentiment
        if avg_compound >= 0.05:
            overall_sentiment = "Positive"
        elif avg_compound <= -0.05:
            overall_sentiment = "Negative"
        else:
            overall_sentiment = "Neutral"
        
        return {
            'average_compound_score': avg_compound,
            'overall_sentiment': overall_sentiment,
            'positive_articles': len([s for s in compound_scores if s >= 0.05]),
            'negative_articles': len([s for s in compound_scores if s <= -0.05]),
            'neutral_articles': len([s for s in compound_scores if -0.05 < s < 0.05])
        }
    
    def summarize_finbert_scores(self, scores: List[List[Dict]]) -> Dict:
        """Summarize FinBERT sentiment scores"""
        if not scores:
            return {}
        
        # Extract dominant sentiments
        sentiments = []
        for score_list in scores:
            max_score = max(score_list, key=lambda x: x['score'])
            sentiments.append(max_score['label'])
        
        positive_count = sentiments.count('positive')
        negative_count = sentiments.count('negative')
        neutral_count = sentiments.count('neutral')
        
        total = len(sentiments)
        
        return {
            'positive_percentage': (positive_count / total) * 100 if total > 0 else 0,
            'negative_percentage': (negative_count / total) * 100 if total > 0 else 0,
            'neutral_percentage': (neutral_count / total) * 100 if total > 0 else 0,
            'dominant_sentiment': max(['positive', 'negative', 'neutral'], 
                                    key=lambda x: sentiments.count(x))
        }
    
    async def get_sec_filings_summary(self, ticker: str) -> Dict:
        """Get recent SEC filings summary (free API)"""
        try:
            # Use SEC's EDGAR API (free)
            headers = {'User-Agent': 'equity-research-app contact@example.com'}
            
            # Search for company CIK
            search_url = f"https://www.sec.gov/files/company_tickers.json"
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                companies = response.json()
                
                # Find company by ticker
                cik = None
                for company_data in companies.values():
                    if company_data.get('ticker', '').upper() == ticker.split('.')[0].upper():
                        cik = str(company_data['cik_str']).zfill(10)
                        break
                
                if cik:
                    # Get recent filings
                    filings_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
                    filings_response = requests.get(filings_url, headers=headers, timeout=10)
                    
                    if filings_response.status_code == 200:
                        filings_data = filings_response.json()
                        recent_filings = filings_data.get('filings', {}).get('recent', {})
                        
                        # Extract last 5 filings
                        forms = recent_filings.get('form', [])[:5]
                        filing_dates = recent_filings.get('filingDate', [])[:5]
                        accession_numbers = recent_filings.get('accessionNumber', [])[:5]
                        
                        filings_summary = []
                        for i in range(min(len(forms), 5)):
                            filings_summary.append({
                                'form': forms[i],
                                'filing_date': filing_dates[i],
                                'accession_number': accession_numbers[i]
                            })
                        
                        return {
                            'company_name': filings_data.get('name', ''),
                            'cik': cik,
                            'recent_filings': filings_summary
                        }
            
            return {'error': 'Company not found in SEC database'}
            
        except Exception as e:
            return {'error': f'SEC filings error: {str(e)}'}
    
    async def get_comprehensive_data(self, ticker: str, company_name: str) -> Dict:
        """Get all data from multiple sources"""
        
        # Start all data collection tasks
        tasks = [
            self.get_enhanced_financial_data(ticker),
            self.get_news_sentiment(company_name, ticker),
            self.get_sec_filings_summary(ticker)
        ]
        
        try:
            financial_data, sentiment_data, sec_data = await asyncio.gather(*tasks, return_exceptions=True)
            
            return {
                'financial_data': financial_data if not isinstance(financial_data, Exception) else {'error': str(financial_data)},
                'sentiment_data': sentiment_data if not isinstance(sentiment_data, Exception) else {'error': str(sentiment_data)},
                'sec_data': sec_data if not isinstance(sec_data, Exception) else {'error': str(sec_data)},
                'collection_timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {'error': f'Data collection failed: {str(e)}'}
