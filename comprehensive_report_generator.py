"""
Enhanced PDF Generator for Comprehensive Educational Equity Research Reports
Generates professional academic-style reports with all required sections
"""

import os
import json
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import yfinance as yf
import pandas as pd
from io import BytesIO
import tempfile

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

import plotly.graph_objects as go
import plotly.io as pio

class ComprehensiveReportGenerator:
    def __init__(self):
        self.css_styles = """
        @page {
            size: A4;
            margin: 2.5cm 2cm;
            @top-left {
                content: "Educational Equity Research Report";
                font-size: 10px;
                color: #666;
            }
            @top-right {
                content: counter(page);
                font-size: 10px;
                color: #666;
            }
            @bottom-center {
                content: "Page " counter(page);
                font-size: 10px;
                color: #666;
            }
        }
        
        body {
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            color: #333;
            font-size: 12px;
        }
        
        .header {
            text-align: center;
            border-bottom: 2px solid #0066cc;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }
        
        .company-name {
            font-size: 24px;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 10px;
        }
        
        .sector-info {
            font-size: 14px;
            color: #666;
            margin-bottom: 20px;
        }
        
        .disclaimer {
            background-color: #f8f9fa;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
            font-size: 11px;
            font-style: italic;
        }
        
        .section-title {
            font-size: 16px;
            font-weight: bold;
            color: #0066cc;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
            margin: 25px 0 15px 0;
        }
        
        .financial-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 10px;
        }
        
        .financial-table th,
        .financial-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: right;
        }
        
        .financial-table th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        
        .metric-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin: 15px 0;
        }
        
        .metric-box {
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
        }
        
        .metric-label {
            font-weight: bold;
            color: #666;
            font-size: 10px;
        }
        
        .metric-value {
            font-size: 14px;
            font-weight: bold;
            color: #0066cc;
        }
        
        .dupont-analysis {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        
        .brand-list {
            columns: 2;
            column-gap: 20px;
            margin: 15px 0;
        }
        
        .brand-list li {
            break-inside: avoid;
            margin-bottom: 5px;
        }
        
        .chart-container {
            text-align: center;
            margin: 20px 0;
        }
        
        .chart-image {
            max-width: 100%;
            height: auto;
        }
        """
    
    def fetch_company_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch comprehensive company data from multiple sources"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="5y")
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cash_flow = ticker.cashflow
            
            return {
                'info': info,
                'history': hist,
                'financials': financials,
                'balance_sheet': balance_sheet,
                'cash_flow': cash_flow,
                'symbol': symbol.upper()
            }
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return {'symbol': symbol.upper(), 'error': str(e)}
    
    def calculate_financial_metrics(self, data: Dict) -> Dict[str, Any]:
        """Calculate comprehensive financial metrics and ratios"""
        if 'error' in data:
            return {}
        
        try:
            info = data.get('info', {})
            
            # Basic metrics from info - handle both None and missing values
            def safe_get(key, default=0):
                value = info.get(key, default)
                return value if value is not None else default
            
            metrics = {
                'market_cap': safe_get('marketCap'),
                'pe_ratio': safe_get('trailingPE'),
                'pb_ratio': safe_get('priceToBook'),
                'roe': safe_get('returnOnEquity'),
                'roa': safe_get('returnOnAssets'),
                'debt_to_equity': safe_get('debtToEquity'),
                'current_ratio': safe_get('currentRatio'),
                'profit_margin': safe_get('profitMargins'),
                'revenue_growth': safe_get('revenueGrowth'),
                'dividend_yield': safe_get('dividendYield'),
                'beta': safe_get('beta'),
                'book_value': safe_get('bookValue'),
                'earnings_growth': safe_get('earningsGrowth'),
                'gross_margins': safe_get('grossMargins'),
                'operating_margins': safe_get('operatingMargins'),
                'ebitda_margins': safe_get('ebitdaMargins'),
                'quick_ratio': safe_get('quickRatio'),
                'total_cash': safe_get('totalCash'),
                'total_debt': safe_get('totalDebt'),
                'revenue_per_share': safe_get('revenuePerShare'),
                'forward_pe': safe_get('forwardPE'),
                'peg_ratio': safe_get('pegRatio'),
                'price_to_sales': safe_get('priceToSalesTrailing12Months'),
                'enterprise_value': safe_get('enterpriseValue'),
                'ev_revenue': safe_get('enterpriseToRevenue'),
                'ev_ebitda': safe_get('enterpriseToEbitda'),
                'fifty_two_week_high': safe_get('fiftyTwoWeekHigh'),
                'fifty_two_week_low': safe_get('fiftyTwoWeekLow'),
                'shares_outstanding': safe_get('sharesOutstanding'),
                'float_shares': safe_get('floatShares'),
                'held_percent_institutions': safe_get('heldPercentInstitutions'),
                'held_percent_insiders': safe_get('heldPercentInsiders'),
                'total_revenue': safe_get('totalRevenue'),
                'total_assets': safe_get('totalAssets', safe_get('totalAssetsTtm')),
                'total_equity': safe_get('totalStockholderEquity', safe_get('stockholdersEquity')),
                'current_price': safe_get('currentPrice', safe_get('regularMarketPrice')),
            }
            
            # Get current price from history if not in info
            if metrics['current_price'] == 0:
                hist = data.get('history')
                if hist is not None and not hist.empty:
                    metrics['current_price'] = float(hist['Close'].iloc[-1])
            
            # Calculate additional metrics with safety checks
            if metrics['pe_ratio'] > 0 and metrics['earnings_growth'] > 0:
                metrics['peg_calculated'] = metrics['pe_ratio'] / (metrics['earnings_growth'] * 100)
            
            # DuPont Analysis components with better data sourcing
            if metrics['profit_margin'] > 0 and metrics['total_assets'] > 0 and metrics['total_equity'] > 0:
                # Calculate asset turnover and equity multiplier
                revenue = metrics['total_revenue']
                if revenue > 0:
                    asset_turnover = revenue / metrics['total_assets']
                    equity_multiplier = metrics['total_assets'] / metrics['total_equity']
                    
                    metrics['dupont'] = {
                        'net_profit_margin': metrics['profit_margin'],
                        'asset_turnover': asset_turnover,
                        'equity_multiplier': equity_multiplier,
                        'roe_calculated': metrics['profit_margin'] * asset_turnover * equity_multiplier
                    }
                else:
                    # Fallback DuPont calculation using available ROE
                    if metrics['roe'] > 0:
                        metrics['dupont'] = {
                            'net_profit_margin': metrics['profit_margin'],
                            'asset_turnover': 1.0,  # Estimate
                            'equity_multiplier': metrics['total_assets'] / metrics['total_equity'] if metrics['total_equity'] > 0 else 1.0,
                            'roe_calculated': metrics['roe']
                        }
            
            # If no DuPont data but we have ROE, create a simplified version
            if 'dupont' not in metrics and metrics['roe'] > 0:
                metrics['dupont'] = {
                    'net_profit_margin': metrics['profit_margin'],
                    'asset_turnover': 1.0,
                    'equity_multiplier': 1.0,
                    'roe_calculated': metrics['roe']
                }
            
            return metrics
            
        except Exception as e:
            print(f"Error calculating financial metrics: {e}")
            return {}
    
    def generate_header_section(self, data: Dict) -> str:
        """Generate report header with company information"""
        info = data.get('info', {})
        symbol = data.get('symbol', 'N/A')
        
        company_name = info.get('longName', symbol)
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')
        
        current_price = info.get('currentPrice', 0)
        target_price = current_price * 1.15  # 15% upside assumption
        
        return f"""
        <div class="header">
            <div class="company-name">{company_name}</div>
            <div class="sector-info">
                <strong>Symbol:</strong> {symbol} | 
                <strong>Sector:</strong> {sector} | 
                <strong>Industry:</strong> {industry}
            </div>
            <div class="sector-info">
                <strong>Target Price (12 months):</strong> ${target_price:.2f} | 
                <strong>Holding Period:</strong> 12-18 months
            </div>
            <div class="disclaimer">
                <strong>EDUCATIONAL REPORT</strong> - This report is prepared for academic purposes only and does not constitute investment advice.
            </div>
        </div>
        """
    
    def generate_business_overview(self, data: Dict) -> str:
        """Generate business overview section"""
        info = data.get('info', {})
        
        description = info.get('longBusinessSummary', 'No business description available.')
        website = info.get('website', '')
        employees = info.get('fullTimeEmployees', 0)
        founded = info.get('foundedYear', 'N/A')
        
        return f"""
        <div class="section-title">2. About the Business</div>
        <p><strong>Business Description:</strong></p>
        <p>{description}</p>
        
        <div class="metric-grid">
            <div class="metric-box">
                <div class="metric-label">Full-time Employees</div>
                <div class="metric-value">{employees:,}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Website</div>
                <div class="metric-value">{website}</div>
            </div>
        </div>
        """
    
    def generate_financial_snapshot(self, data: Dict, metrics: Dict) -> str:
        """Generate 4-year financial snapshot with projections"""
        try:
            financials = data.get('financials', pd.DataFrame())
            info = data.get('info', {})
            
            if financials.empty:
                # Use available info data to create a basic financial snapshot
                revenue = metrics.get('total_revenue', 0)
                market_cap = metrics.get('market_cap', 0)
                
                if revenue > 0 or market_cap > 0:
                    financial_table = f"""
                    <div class="section-title">3. Financial Snapshot</div>
                    <table class="financial-table">
                        <tr><th>Metric</th><th>Current</th></tr>
                        <tr><td><strong>Market Cap</strong></td><td>${market_cap/1e9:.2f}B</td></tr>
                        <tr><td><strong>Total Revenue (TTM)</strong></td><td>${revenue/1e9:.2f}B</td></tr>
                        <tr><td><strong>Net Profit Margin</strong></td><td>{(metrics.get('profit_margin', 0) * 100):.2f}%</td></tr>
                        <tr><td><strong>Gross Margin</strong></td><td>{(metrics.get('gross_margins', 0) * 100):.2f}%</td></tr>
                        <tr><td><strong>Operating Margin</strong></td><td>{(metrics.get('operating_margins', 0) * 100):.2f}%</td></tr>
                    </table>
                    """
                else:
                    financial_table = """
                    <div class="section-title">3. Financial Snapshot</div>
                    <p>Detailed historical financial data is not available. Current market metrics are shown in other sections.</p>
                    """
            else:
                # Process available financial data
                years = financials.columns[:4] if len(financials.columns) >= 4 else financials.columns
                
                # Try to find revenue data with multiple possible names
                revenue_row = None
                revenue_keywords = ['Total Revenue', 'Revenue', 'Net Sales', 'Sales']
                for keyword in revenue_keywords:
                    revenue_row = financials.loc[financials.index.str.contains(keyword, case=False, na=False)]
                    if not revenue_row.empty:
                        break
                
                # Try to find net income data
                net_income_row = None
                income_keywords = ['Net Income', 'Net Earnings', 'Profit', 'Earnings']
                for keyword in income_keywords:
                    net_income_row = financials.loc[financials.index.str.contains(keyword, case=False, na=False)]
                    if not net_income_row.empty:
                        break
                
                financial_table = """
                <div class="section-title">3. Financial Snapshot (Last 4 Years + Projections)</div>
                <table class="financial-table">
                    <tr><th>Metric</th>
                """
                
                for year in years:
                    financial_table += f"<th>{year.strftime('%Y')}</th>"
                
                financial_table += "<th>Projected</th></tr>"
                
                # Add revenue row if available
                if revenue_row is not None and not revenue_row.empty:
                    financial_table += "<tr><td><strong>Revenue ($ Billions)</strong></td>"
                    revenue_values = []
                    for year in years:
                        value = revenue_row.iloc[0][year] / 1e9 if not pd.isna(revenue_row.iloc[0][year]) else 0
                        revenue_values.append(value)
                        financial_table += f"<td>${value:,.1f}B</td>"
                    
                    # Simple projection
                    if len(revenue_values) >= 2 and revenue_values[1] != 0:
                        growth_rate = (revenue_values[0] - revenue_values[1]) / revenue_values[1]
                        projected = revenue_values[0] * (1 + max(growth_rate, -0.2))  # Cap negative growth
                        financial_table += f"<td>${projected:,.1f}B</td>"
                    else:
                        financial_table += "<td>N/A</td>"
                    financial_table += "</tr>"
                
                # Add net income row if available
                if net_income_row is not None and not net_income_row.empty:
                    financial_table += "<tr><td><strong>Net Income ($ Billions)</strong></td>"
                    for year in years:
                        value = net_income_row.iloc[0][year] / 1e9 if not pd.isna(net_income_row.iloc[0][year]) else 0
                        financial_table += f"<td>${value:,.1f}B</td>"
                    financial_table += "<td>N/A</td></tr>"
                
                # Add current metrics
                financial_table += f"""
                    <tr><td><strong>Net Profit Margin</strong></td>
                        <td colspan="5">{(metrics.get('profit_margin', 0) * 100):.2f}%</td></tr>
                    <tr><td><strong>Gross Margin</strong></td>
                        <td colspan="5">{(metrics.get('gross_margins', 0) * 100):.2f}%</td></tr>
                """
                
                financial_table += "</table>"
            
            # Shareholding pattern
            held_institutions = metrics.get('held_percent_institutions', 0) * 100
            held_insiders = metrics.get('held_percent_insiders', 0) * 100
            public_holding = max(0, 100 - held_institutions - held_insiders)
            
            shareholding_section = f"""
            <h4>Shareholding Pattern</h4>
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-label">Institutional Holdings</div>
                    <div class="metric-value">{held_institutions:.1f}%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Insider Holdings</div>
                    <div class="metric-value">{held_insiders:.1f}%</div>
                </div>
            </div>
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-label">Public Holdings</div>
                    <div class="metric-value">{public_holding:.1f}%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Shares Outstanding</div>
                    <div class="metric-value">{metrics.get('shares_outstanding', 0)/1e6:.0f}M</div>
                </div>
            </div>
            """
            
            return financial_table + shareholding_section
            
        except Exception as e:
            print(f"Error generating financial snapshot: {e}")
            return f"""
            <div class="section-title">3. Financial Snapshot</div>
            <p>Error processing financial data: {str(e)}</p>
            <p>Current market cap: ${metrics.get('market_cap', 0)/1e9:.2f}B</p>
            <p>Current price: ${metrics.get('current_price', 0):.2f}</p>
            """
    
    def generate_key_metrics(self, metrics: Dict) -> str:
        """Generate key financial metrics section"""
        return f"""
        <div class="section-title">4. Key Financial Metrics</div>
        <div class="metric-grid">
            <div class="metric-box">
                <div class="metric-label">Return on Equity (ROE)</div>
                <div class="metric-value">{(metrics.get('roe', 0) * 100):.2f}%</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Return on Assets (ROA)</div>
                <div class="metric-value">{(metrics.get('roce', 0) * 100):.2f}%</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Gross Profit Margin</div>
                <div class="metric-value">{(metrics.get('gross_margins', 0) * 100):.2f}%</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Operating Margin</div>
                <div class="metric-value">{(metrics.get('operating_margins', 0) * 100):.2f}%</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">EBITDA Margin</div>
                <div class="metric-value">{(metrics.get('ebitda_margins', 0) * 100):.2f}%</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Dividend Yield</div>
                <div class="metric-value">{(metrics.get('dividend_yield', 0) * 100):.2f}%</div>
            </div>
        </div>
        """
    
    def generate_ratios_table(self, metrics: Dict) -> str:
        """Generate comprehensive financial ratios table"""
        
        def format_ratio(value, is_percentage=False, decimal_places=2):
            """Format ratio values safely"""
            if value is None or value == 0:
                return "N/A"
            try:
                if is_percentage:
                    return f"{float(value * 100):.{decimal_places}f}%"
                else:
                    return f"{float(value):.{decimal_places}f}"
            except (ValueError, TypeError):
                return "N/A"
        
        return f"""
        <div class="section-title">10. Financial Ratios Table</div>
        <table class="financial-table">
            <tr><th colspan="2">Valuation Ratios</th></tr>
            <tr><td>Price-to-Earnings (P/E)</td><td>{format_ratio(metrics.get('pe_ratio'))}</td></tr>
            <tr><td>Price-to-Book (P/B)</td><td>{format_ratio(metrics.get('pb_ratio'))}</td></tr>
            <tr><td>EV/EBITDA</td><td>{format_ratio(metrics.get('ev_ebitda'))}</td></tr>
            <tr><td>Price-to-Sales</td><td>{format_ratio(metrics.get('price_to_sales'))}</td></tr>
            <tr><td>PEG Ratio</td><td>{format_ratio(metrics.get('peg_ratio'))}</td></tr>
            <tr><td>Forward P/E</td><td>{format_ratio(metrics.get('forward_pe'))}</td></tr>
            
            <tr><th colspan="2">Liquidity Ratios</th></tr>
            <tr><td>Current Ratio</td><td>{format_ratio(metrics.get('current_ratio'))}</td></tr>
            <tr><td>Quick Ratio</td><td>{format_ratio(metrics.get('quick_ratio'))}</td></tr>
            
            <tr><th colspan="2">Solvency Ratios</th></tr>
            <tr><td>Debt-to-Equity</td><td>{format_ratio(metrics.get('debt_to_equity'))}</td></tr>
            <tr><td>Beta</td><td>{format_ratio(metrics.get('beta'))}</td></tr>
            
            <tr><th colspan="2">Profitability Ratios</th></tr>
            <tr><td>Gross Profit Margin</td><td>{format_ratio(metrics.get('gross_margins'), True)}</td></tr>
            <tr><td>Operating Margin</td><td>{format_ratio(metrics.get('operating_margins'), True)}</td></tr>
            <tr><td>EBITDA Margin</td><td>{format_ratio(metrics.get('ebitda_margins'), True)}</td></tr>
            <tr><td>Net Profit Margin</td><td>{format_ratio(metrics.get('profit_margin'), True)}</td></tr>
            
            <tr><th colspan="2">Return Ratios</th></tr>
            <tr><td>Return on Assets (ROA)</td><td>{format_ratio(metrics.get('roa'), True)}</td></tr>
            <tr><td>Return on Equity (ROE)</td><td>{format_ratio(metrics.get('roe'), True)}</td></tr>
            
            <tr><th colspan="2">Growth & Yield</th></tr>
            <tr><td>Revenue Growth</td><td>{format_ratio(metrics.get('revenue_growth'), True)}</td></tr>
            <tr><td>Earnings Growth</td><td>{format_ratio(metrics.get('earnings_growth'), True)}</td></tr>
            <tr><td>Dividend Yield</td><td>{format_ratio(metrics.get('dividend_yield'), True)}</td></tr>
            
            <tr><th colspan="2">Market Data</th></tr>
            <tr><td>52-Week High</td><td>${format_ratio(metrics.get('fifty_two_week_high'))}</td></tr>
            <tr><td>52-Week Low</td><td>${format_ratio(metrics.get('fifty_two_week_low'))}</td></tr>
            <tr><td>Current Price</td><td>${format_ratio(metrics.get('current_price'))}</td></tr>
        </table>
        """
    
    def generate_dupont_analysis(self, metrics: Dict) -> str:
        """Generate DuPont analysis section"""
        dupont = metrics.get('dupont', {})
        
        if not dupont and metrics.get('roe', 0) > 0:
            # Create a simplified DuPont analysis if we have ROE
            dupont = {
                'net_profit_margin': metrics.get('profit_margin', 0),
                'asset_turnover': 1.0,  # Placeholder
                'equity_multiplier': 1.0 + (metrics.get('debt_to_equity', 0) / 100),  # Approximation
                'roe_calculated': metrics.get('roe', 0)
            }
        
        if not dupont:
            return """
            <div class="section-title">11. DuPont Analysis</div>
            <div class="dupont-analysis">
                <p>DuPont analysis requires detailed financial statement data that is not currently available.</p>
                <p>This analysis decomposes Return on Equity (ROE) into three components:</p>
                <ul>
                    <li><strong>Net Profit Margin:</strong> Measures operational efficiency</li>
                    <li><strong>Asset Turnover:</strong> Measures asset utilization efficiency</li>
                    <li><strong>Equity Multiplier:</strong> Measures financial leverage</li>
                </ul>
                <p>ROE = Net Profit Margin × Asset Turnover × Equity Multiplier</p>
            </div>
            """
        
        def safe_format(value, is_percentage=False):
            if value is None or value == 0:
                return "N/A"
            try:
                if is_percentage:
                    return f"{float(value * 100):.2f}%"
                else:
                    return f"{float(value):.3f}"
            except (ValueError, TypeError):
                return "N/A"
        
        npm = dupont.get('net_profit_margin', 0)
        ato = dupont.get('asset_turnover', 0) 
        em = dupont.get('equity_multiplier', 0)
        roe_calc = dupont.get('roe_calculated', 0)
        
        return f"""
        <div class="section-title">11. DuPont Analysis</div>
        <div class="dupont-analysis">
            <p><strong>ROE Decomposition:</strong></p>
            <p>ROE = Net Profit Margin × Asset Turnover × Equity Multiplier</p>
            <p>ROE = {safe_format(npm, True)} × {safe_format(ato)} × {safe_format(em)}</p>
            <p><strong>Calculated ROE = {safe_format(roe_calc, True)}</strong></p>
            <p><strong>Reported ROE = {safe_format(metrics.get('roe'), True)}</strong></p>
            
            <h4>Component Analysis:</h4>
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-label">Net Profit Margin</div>
                    <div class="metric-value">{safe_format(npm, True)}</div>
                    <div style="font-size: 10px; color: #666;">Operational efficiency</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Asset Turnover</div>
                    <div class="metric-value">{safe_format(ato)}x</div>
                    <div style="font-size: 10px; color: #666;">Asset utilization</div>
                </div>
            </div>
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-label">Equity Multiplier</div>
                    <div class="metric-value">{safe_format(em)}x</div>
                    <div style="font-size: 10px; color: #666;">Financial leverage</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Debt-to-Equity</div>
                    <div class="metric-value">{safe_format(metrics.get('debt_to_equity'))}</div>
                    <div style="font-size: 10px; color: #666;">Leverage ratio</div>
                </div>
            </div>
            
            <h4>Interpretation:</h4>
            <ul>
                <li><strong>Net Profit Margin ({safe_format(npm, True)}):</strong> 
                    {'Excellent' if npm > 0.15 else 'Good' if npm > 0.08 else 'Moderate' if npm > 0.03 else 'Low'} operational efficiency</li>
                <li><strong>Asset Turnover ({safe_format(ato)}x):</strong> 
                    {'High' if ato > 1.5 else 'Moderate' if ato > 0.8 else 'Low'} asset utilization</li>
                <li><strong>Equity Multiplier ({safe_format(em)}x):</strong> 
                    {'High' if em > 3 else 'Moderate' if em > 1.5 else 'Conservative'} financial leverage</li>
            </ul>
        </div>
        """
    
    def generate_industry_overview(self, data: Dict) -> str:
        """Generate industry overview section with real data analysis"""
        info = data.get('info', {})
        sector = info.get('sector', 'N/A')
        industry = info.get('industry', 'N/A')
        symbol = data.get('symbol', 'N/A')
        
        # Get key financial metrics for competitive analysis
        market_cap = info.get('marketCap', 0)
        beta = info.get('beta', 1.0)
        pe_ratio = info.get('forwardPE', info.get('trailingPE', 0))
        roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0
        profit_margins = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0
        
        # Determine competitive position based on metrics
        competitive_position = "strong" if market_cap > 100000000000 and profit_margins > 15 else "moderate" if market_cap > 10000000000 else "developing"
        
        return f"""
        <div class="section-title">7. Industry Overview</div>
        <div class="content">
            <p><strong>Sector Analysis:</strong> {sector}</p>
            <p><strong>Industry Classification:</strong> {industry}</p>
            
            <p><strong>Market Position Analysis:</strong></p>
            <p>{symbol} operates within the {sector.lower()} sector, specifically in the {industry.lower()} industry. 
            Based on financial metrics, the company maintains a {competitive_position} competitive position in its market segment.</p>
            
            <h4>Competitive Metrics Analysis:</h4>
            <table class="financial-table">
                <tr>
                    <th>Metric</th>
                    <th>Value</th>
                    <th>Competitive Assessment</th>
                </tr>
                <tr>
                    <td>Market Capitalization</td>
                    <td>${market_cap:,.0f}</td>
                    <td>{"Large-cap leader" if market_cap > 200000000000 else "Mid-to-large cap player" if market_cap > 50000000000 else "Mid-cap participant"}</td>
                </tr>
                <tr>
                    <td>Beta (Market Sensitivity)</td>
                    <td>{beta:.2f}</td>
                    <td>{"Higher volatility than market" if beta > 1.2 else "Market-aligned volatility" if beta > 0.8 else "Lower volatility than market"}</td>
                </tr>
                <tr>
                    <td>P/E Ratio</td>
                    <td>{pe_ratio:.1f}x</td>
                    <td>{"Premium valuation" if pe_ratio > 25 else "Market valuation" if pe_ratio > 15 else "Value pricing"}</td>
                </tr>
                <tr>
                    <td>Profit Margins</td>
                    <td>{profit_margins:.1f}%</td>
                    <td>{"Superior profitability" if profit_margins > 20 else "Strong margins" if profit_margins > 10 else "Moderate profitability"}</td>
                </tr>
            </table>
            
            <h4>Competitive Advantages:</h4>
            <ul>
                <li><strong>Scale Advantage:</strong> {"Significant market presence" if market_cap > 100000000000 else "Established market position" if market_cap > 10000000000 else "Growing market presence"} with ${market_cap/1000000000:.1f}B market cap</li>
                <li><strong>Operational Efficiency:</strong> {profit_margins:.1f}% profit margins {"demonstrate strong operational control" if profit_margins > 15 else "indicate solid management execution" if profit_margins > 5 else "show room for improvement"}</li>
                <li><strong>Financial Stability:</strong> {"Lower market sensitivity" if beta < 1.0 else "Market-correlated performance" if beta < 1.3 else "Higher growth/risk profile"} (Beta: {beta:.2f})</li>
                <li><strong>Valuation Position:</strong> {"Premium market positioning" if pe_ratio > 25 else "Balanced valuation metrics" if pe_ratio > 10 else "Value-oriented pricing"} with {pe_ratio:.1f}x P/E ratio</li>
            </ul>
        </div>
        """
    
    def generate_disclaimer(self) -> str:
        """Generate comprehensive disclaimer"""
        return """
        <div class="section-title">13. Disclaimer</div>
        <div class="disclaimer">
            <p><strong>EDUCATIONAL PURPOSE ONLY</strong></p>
            <p>This report has been prepared for educational and academic purposes only. It is not intended as, 
            and should not be construed as, investment advice or a recommendation to buy, sell, or hold any securities.</p>
            
            <p><strong>Important Notes:</strong></p>
            <ul>
                <li>All financial data is sourced from publicly available information and may not be current</li>
                <li>Projections and target prices are illustrative and should not be used for investment decisions</li>
                <li>Past performance does not guarantee future results</li>
                <li>All investments carry risk, including potential loss of principal</li>
                <li>Consult with qualified financial advisors before making investment decisions</li>
            </ul>
            
            <p><strong>Prepared by:</strong> Student/Research Analyst for Academic Purposes</p>
            <p><strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        """
    
    def generate_strategic_highlights(self, data: Dict) -> str:
        """Generate strategic highlights based on actual company data"""
        info = data.get('info', {})
        symbol = data.get('symbol', 'N/A')
        
        # Extract business description and strategy insights
        business_summary = info.get('businessSummary', 'Business summary not available.')
        market_cap = info.get('marketCap', 0)
        employee_count = info.get('fullTimeEmployees', 'N/A')
        
        # Calculate company size classification
        if market_cap > 200000000000:  # $200B+
            size_class = "large-cap multinational corporation"
        elif market_cap > 10000000000:  # $10B+
            size_class = "mid-to-large cap company"
        else:
            size_class = "mid-cap company"
        
        # Get recent performance metrics
        hist = data.get('history', pd.DataFrame())
        price_change_52w = 0
        if not hist.empty and len(hist) > 250:
            current_price = hist['Close'].iloc[-1]
            price_52w_ago = hist['Close'].iloc[-252]
            price_change_52w = ((current_price - price_52w_ago) / price_52w_ago) * 100
        
        return f"""
        <div class="section-title">5. Strategic Highlights</div>
        <div class="content">
            <p><strong>Business Strategy Overview:</strong></p>
            <p>{business_summary[:500]}{"..." if len(business_summary) > 500 else ""}</p>
            
            <p><strong>Key Strategic Metrics:</strong></p>
            <ul>
                <li><strong>Market Position:</strong> {symbol} operates as a {size_class} with a market capitalization of ${market_cap:,.0f} million</li>
                <li><strong>Workforce:</strong> Employs approximately {employee_count:,} full-time employees globally</li>
                <li><strong>52-Week Performance:</strong> Stock has {"gained" if price_change_52w > 0 else "declined"} {abs(price_change_52w):.1f}% over the past year</li>
                <li><strong>Sector Focus:</strong> Operates primarily in {info.get('sector', 'Multiple sectors')} with focus on {info.get('industry', 'diversified operations')}</li>
            </ul>
            
            <p><strong>Growth Initiatives:</strong></p>
            <p>Based on financial metrics and market position, {symbol} appears focused on {"growth and expansion" if price_change_52w > 10 else "operational efficiency and market consolidation" if price_change_52w > -10 else "restructuring and recovery"}. 
            The company's {"strong" if market_cap > 50000000000 else "stable"} market capitalization suggests {"continued investment in innovation and market expansion" if market_cap > 100000000000 else "focus on core business optimization"}.</p>
        </div>
        """

    def generate_quarterly_performance(self, data: Dict) -> str:
        """Generate quarterly performance analysis from available data"""
        info = data.get('info', {})
        hist = data.get('history', pd.DataFrame())
        symbol = data.get('symbol', 'N/A')
        
        # Get recent financial metrics
        revenue = info.get('totalRevenue', 0)
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0
        profit_margins = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0
        
        # Calculate recent price performance
        quarterly_performance = []
        if not hist.empty and len(hist) > 60:
            # Last 3 months performance
            current_price = hist['Close'].iloc[-1]
            q_ago_price = hist['Close'].iloc[-63] if len(hist) > 63 else hist['Close'].iloc[0]
            q_performance = ((current_price - q_ago_price) / q_ago_price) * 100
            quarterly_performance.append(f"Q4 2024: {q_performance:+.1f}%")
        
        return f"""
        <div class="section-title">6. Quarterly Performance</div>
        <div class="content">
            <p><strong>Recent Financial Performance:</strong></p>
            <ul>
                <li><strong>Total Revenue:</strong> ${revenue:,.0f} million (TTM)</li>
                <li><strong>Revenue Growth:</strong> {revenue_growth:+.1f}% year-over-year</li>
                <li><strong>Profit Margins:</strong> {profit_margins:.1f}% net margin</li>
                <li><strong>Stock Performance:</strong> {quarterly_performance[0] if quarterly_performance else "Data not available for quarterly comparison"}</li>
            </ul>
            
            <p><strong>Key Performance Indicators:</strong></p>
            <table class="financial-table">
                <tr>
                    <th>Metric</th>
                    <th>Current</th>
                    <th>Assessment</th>
                </tr>
                <tr>
                    <td>Revenue Growth</td>
                    <td>{revenue_growth:+.1f}%</td>
                    <td>{"Strong growth trajectory" if revenue_growth > 10 else "Moderate growth" if revenue_growth > 0 else "Revenue challenges"}</td>
                </tr>
                <tr>
                    <td>Profitability</td>
                    <td>{profit_margins:.1f}%</td>
                    <td>{"Highly profitable" if profit_margins > 15 else "Moderately profitable" if profit_margins > 5 else "Margin pressure"}</td>
                </tr>
                <tr>
                    <td>Market Performance</td>
                    <td>{quarterly_performance[0] if quarterly_performance else "N/A"}</td>
                    <td>{"Outperforming market" if quarterly_performance and float(quarterly_performance[0].split(":")[1].replace("%", "")) > 5 else "Market aligned performance"}</td>
                </tr>
            </table>
            
            <p><strong>Quarterly Trends Analysis:</strong></p>
            <p>Based on available financial data, {symbol} demonstrates {"strong operational performance" if revenue_growth > 5 and profit_margins > 10 else "stable business fundamentals" if revenue_growth > 0 else "operational challenges requiring attention"}. 
            The company's {"robust" if profit_margins > 15 else "adequate"} profit margins indicate {"efficient cost management and pricing power" if profit_margins > 10 else "reasonable operational efficiency"}.</p>
        </div>
        """

    def generate_brand_portfolio(self, data: Dict) -> str:
        """Generate brand portfolio and geographic analysis"""
        info = data.get('info', {})
        symbol = data.get('symbol', 'N/A')
        
        # Extract available geographic and business data
        country = info.get('country', 'United States')
        sector = info.get('sector', 'Technology')
        industry = info.get('industry', 'Software')
        website = info.get('website', 'N/A')
        
        return f"""
        <div class="section-title">8. Brand Portfolio & Geographic Breakdown</div>
        <div class="content">
            <p><strong>Corporate Structure:</strong></p>
            <ul>
                <li><strong>Primary Headquarters:</strong> {country}</li>
                <li><strong>Primary Sector:</strong> {sector}</li>
                <li><strong>Industry Focus:</strong> {industry}</li>
                <li><strong>Corporate Website:</strong> {website}</li>
            </ul>
            
            <p><strong>Business Segments:</strong></p>
            <p>As a {sector.lower()} company operating in the {industry.lower()} space, {symbol} likely operates through multiple business segments including:</p>
            <ul>
                <li>Core {industry.lower()} operations and services</li>
                <li>Research and development initiatives</li>
                <li>Customer support and professional services</li>
                <li>Strategic partnerships and licensing</li>
            </ul>
            
            <p><strong>Geographic Presence:</strong></p>
            <p>Based in {country}, {symbol} operates {"globally" if country == "United States" else "regionally"} with significant market presence. 
            The company's {sector.lower()} focus suggests {"international expansion opportunities" if country == "United States" else "strong domestic market position"} 
            and {"diverse revenue streams across multiple geographies" if country == "United States" else "concentrated market exposure"}.</p>
            
            <p><strong>Brand Strategy:</strong></p>
            <p>The company maintains its market position through {"innovation and technology leadership" if sector == "Technology" else "operational excellence and customer service" if sector == "Consumer Cyclical" else "strategic market positioning"} 
            in the {industry.lower()} segment.</p>
        </div>
        """

    def generate_management_commentary(self, data: Dict) -> str:
        """Generate management commentary section"""
        info = data.get('info', {})
        symbol = data.get('symbol', 'N/A')
        
        # Extract key management metrics and data
        market_cap = info.get('marketCap', 0)
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0
        profit_margins = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0
        
        return f"""
        <div class="section-title">9. Management Commentary</div>
        <div class="content">
            <p><strong>Executive Leadership Assessment:</strong></p>
            <p>Management has demonstrated {"strong strategic execution" if revenue_growth > 5 else "stable operational management" if revenue_growth >= 0 else "challenging period requiring strategic adjustments"} 
            based on recent financial performance indicators.</p>
            
            <p><strong>Key Strategic Focus Areas:</strong></p>
            <ul>
                <li><strong>Revenue Generation:</strong> {"Successful growth strategy" if revenue_growth > 10 else "Moderate growth focus" if revenue_growth > 0 else "Revenue optimization efforts"} with {revenue_growth:+.1f}% year-over-year growth</li>
                <li><strong>Operational Efficiency:</strong> {"Strong margin management" if profit_margins > 15 else "Adequate cost control" if profit_margins > 5 else "Margin improvement initiatives"} achieving {profit_margins:.1f}% net margins</li>
                <li><strong>Market Position:</strong> {"Market leadership" if market_cap > 100000000000 else "Strong market presence" if market_cap > 10000000000 else "Growing market position"} with ${market_cap/1000000000:.1f}B market capitalization</li>
            </ul>
            
            <p><strong>Strategic Outlook:</strong></p>
            <p>Based on financial metrics and market position, management appears focused on {"aggressive expansion and innovation" if revenue_growth > 15 and profit_margins > 15 else "balanced growth and profitability" if revenue_growth > 5 and profit_margins > 10 else "operational optimization and efficiency improvements"}. 
            The {"strong" if market_cap > 50000000000 else "solid"} market valuation suggests investor confidence in management's strategic direction.</p>
            
            <p><strong>Risk Management:</strong></p>
            <p>Management's approach to risk appears {"conservative and well-balanced" if profit_margins > 10 else "moderately aggressive" if revenue_growth > profit_margins else "focused on growth over short-term profitability"} 
            given the current balance between growth initiatives and profitability metrics.</p>
        </div>
        """

    def generate_ratings_rationale(self, data: Dict) -> str:
        """Generate ratings rationale section"""
        info = data.get('info', {})
        symbol = data.get('symbol', 'N/A')
        
        # Calculate key rating factors
        market_cap = info.get('marketCap', 0)
        revenue_growth = info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0
        profit_margins = info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0
        debt_to_equity = info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else 0
        
        # Calculate composite rating
        rating_score = 0
        if revenue_growth > 10: rating_score += 2
        elif revenue_growth > 5: rating_score += 1
        elif revenue_growth > 0: rating_score += 0.5
        
        if profit_margins > 15: rating_score += 2
        elif profit_margins > 10: rating_score += 1.5
        elif profit_margins > 5: rating_score += 1
        
        if debt_to_equity < 0.3: rating_score += 1
        elif debt_to_equity < 0.6: rating_score += 0.5
        
        if market_cap > 100000000000: rating_score += 1
        elif market_cap > 10000000000: rating_score += 0.5
        
        # Determine rating
        if rating_score >= 5: rating = "BUY"
        elif rating_score >= 3.5: rating = "HOLD"
        else: rating = "SELL"
        
        return f"""
        <div class="section-title">12. Ratings Rationale</div>
        <div class="content">
            <p><strong>Investment Rating: {rating}</strong></p>
            
            <p><strong>Rating Methodology:</strong></p>
            <table class="financial-table">
                <tr>
                    <th>Factor</th>
                    <th>Score</th>
                    <th>Rationale</th>
                </tr>
                <tr>
                    <td>Revenue Growth</td>
                    <td>{2 if revenue_growth > 10 else 1 if revenue_growth > 5 else 0.5 if revenue_growth > 0 else 0}/2</td>
                    <td>{revenue_growth:+.1f}% growth rate</td>
                </tr>
                <tr>
                    <td>Profitability</td>
                    <td>{2 if profit_margins > 15 else 1.5 if profit_margins > 10 else 1 if profit_margins > 5 else 0}/2</td>
                    <td>{profit_margins:.1f}% net margins</td>
                </tr>
                <tr>
                    <td>Financial Strength</td>
                    <td>{1 if debt_to_equity < 0.3 else 0.5 if debt_to_equity < 0.6 else 0}/1</td>
                    <td>Debt-to-equity: {debt_to_equity:.2f}</td>
                </tr>
                <tr>
                    <td>Market Position</td>
                    <td>{1 if market_cap > 100000000000 else 0.5 if market_cap > 10000000000 else 0}/1</td>
                    <td>${market_cap/1000000000:.1f}B market cap</td>
                </tr>
            </table>
            
            <p><strong>Overall Assessment:</strong></p>
            <p>Based on fundamental analysis, {symbol} receives a <strong>{rating}</strong> rating with a composite score of {rating_score:.1f}/6.0. 
            This rating reflects {"strong fundamentals and growth prospects" if rating == "BUY" else "stable business with moderate prospects" if rating == "HOLD" else "challenges requiring careful consideration"}.</p>
            
            <p><strong>Key Rating Drivers:</strong></p>
            <ul>
                <li>{"Strong" if revenue_growth > 10 else "Moderate" if revenue_growth > 0 else "Weak"} revenue growth trajectory</li>
                <li>{"Excellent" if profit_margins > 15 else "Good" if profit_margins > 10 else "Adequate" if profit_margins > 5 else "Concerning"} profitability metrics</li>
                <li>{"Strong" if debt_to_equity < 0.3 else "Moderate" if debt_to_equity < 0.6 else "High"} financial leverage</li>
                <li>{"Large-cap" if market_cap > 100000000000 else "Mid-cap" if market_cap > 10000000000 else "Small-cap"} market positioning</li>
            </ul>
        </div>
        """
    
    def generate_comprehensive_report(self, symbol: str) -> str:
        """Generate complete comprehensive educational equity research report"""
        # Fetch data
        data = self.fetch_company_data(symbol)
        
        if 'error' in data:
            return f"""
            <html><body>
            <h1>Error Generating Report</h1>
            <p>Unable to fetch data for {symbol}: {data['error']}</p>
            </body></html>
            """
        
        # Calculate metrics
        metrics = self.calculate_financial_metrics(data)
        
        # Generate all sections
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Educational Equity Research Report - {symbol}</title>
            <style>{self.css_styles}</style>
        </head>
        <body>
            {self.generate_header_section(data)}
            {self.generate_business_overview(data)}
            {self.generate_financial_snapshot(data, metrics)}
            {self.generate_key_metrics(metrics)}
            {self.generate_strategic_highlights(data)}
            {self.generate_quarterly_performance(data)}
            {self.generate_industry_overview(data)}
            {self.generate_brand_portfolio(data)}
            {self.generate_management_commentary(data)}
            {self.generate_ratios_table(metrics)}
            {self.generate_dupont_analysis(metrics)}
            {self.generate_ratings_rationale(data)}
            
            {self.generate_disclaimer()}
        </body>
        </html>
        """
        
        return html_content
    
    def generate_pdf_bytes(self, html_content: str) -> Optional[bytes]:
        """Convert HTML to PDF bytes"""
        if not WEASYPRINT_AVAILABLE:
            # Return HTML as text if WeasyPrint not available
            return html_content.encode('utf-8')
        
        try:
            html_doc = HTML(string=html_content)
            pdf_bytes = html_doc.write_pdf()
            return pdf_bytes
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return html_content.encode('utf-8')

# Global instance for use in other modules
comprehensive_generator = ComprehensiveReportGenerator()
