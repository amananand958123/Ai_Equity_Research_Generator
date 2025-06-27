"""
Advanced Visualization Module for Level 2 & 3 Implementation
Creates interactive charts and dashboards using Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import streamlit as st

class AdvancedVisualizer:
    def __init__(self):
        self.color_palette = {
            'primary': '#1f77b4',
            'secondary': '#ff7f0e',
            'success': '#2ca02c',
            'danger': '#d62728',
            'warning': '#ff9800',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }
    
    def create_financial_dashboard(self, financial_data: Dict) -> go.Figure:
        """Create comprehensive financial dashboard"""
        
        yf_data = financial_data.get('yfinance_data', {})
        ratios = financial_data.get('financial_ratios', {})
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Stock Price Trend (1 Year)', 'Volume Analysis',
                'Financial Ratios Overview', 'Profitability Metrics',
                'Price vs Moving Averages', 'Volatility Analysis'
            ),
            specs=[
                [{"secondary_y": True}, {"secondary_y": False}],
                [{"type": "bar"}, {"type": "bar"}],
                [{"secondary_y": True}, {"type": "scatter"}]
            ]
        )
        
        # 1. Stock Price Trend
        hist_data = yf_data.get('historical_1y', pd.DataFrame())
        if not hist_data.empty:
            fig.add_trace(
                go.Scatter(
                    x=hist_data.index,
                    y=hist_data['Close'],
                    name='Close Price',
                    line=dict(color=self.color_palette['primary'], width=2)
                ),
                row=1, col=1
            )
            
            # Add volume on secondary y-axis
            fig.add_trace(
                go.Bar(
                    x=hist_data.index,
                    y=hist_data['Volume'],
                    name='Volume',
                    marker_color=self.color_palette['secondary'],
                    opacity=0.3
                ),
                row=1, col=2
            )
        
        # 2. Financial Ratios
        if ratios.get('valuation'):
            valuation_ratios = ratios['valuation']
            ratio_names = []
            ratio_values = []
            
            for key, value in valuation_ratios.items():
                if value is not None and isinstance(value, (int, float)):
                    ratio_names.append(key.replace('_', ' ').title())
                    ratio_values.append(value)
            
            if ratio_names:
                fig.add_trace(
                    go.Bar(
                        x=ratio_names,
                        y=ratio_values,
                        name='Valuation Ratios',
                        marker_color=self.color_palette['success']
                    ),
                    row=2, col=1
                )
        
        # 3. Profitability Metrics
        if ratios.get('profitability'):
            prof_ratios = ratios['profitability']
            prof_names = []
            prof_values = []
            
            for key, value in prof_ratios.items():
                if value is not None and isinstance(value, (int, float)):
                    prof_names.append(key.replace('_', ' ').title())
                    prof_values.append(value * 100 if value < 1 else value)  # Convert to percentage
            
            if prof_names:
                fig.add_trace(
                    go.Bar(
                        x=prof_names,
                        y=prof_values,
                        name='Profitability %',
                        marker_color=self.color_palette['info']
                    ),
                    row=2, col=2
                )
        
        # 4. Moving Averages
        if not hist_data.empty:
            hist_data['MA20'] = hist_data['Close'].rolling(window=20).mean()
            hist_data['MA50'] = hist_data['Close'].rolling(window=50).mean()
            
            fig.add_trace(
                go.Scatter(
                    x=hist_data.index,
                    y=hist_data['Close'],
                    name='Price',
                    line=dict(color=self.color_palette['dark'])
                ),
                row=3, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=hist_data.index,
                    y=hist_data['MA20'],
                    name='MA20',
                    line=dict(color=self.color_palette['warning'])
                ),
                row=3, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=hist_data.index,
                    y=hist_data['MA50'],
                    name='MA50',
                    line=dict(color=self.color_palette['danger'])
                ),
                row=3, col=1
            )
        
        # 5. Volatility Analysis
        if not hist_data.empty:
            returns = hist_data['Close'].pct_change().dropna()
            volatility_30d = returns.rolling(window=30).std() * np.sqrt(252)  # Annualized
            
            fig.add_trace(
                go.Scatter(
                    x=volatility_30d.index,
                    y=volatility_30d * 100,  # Convert to percentage
                    name='30-Day Volatility %',
                    line=dict(color=self.color_palette['danger']),
                    mode='lines'
                ),
                row=3, col=2
            )
        
        # Update layout
        fig.update_layout(
            title_text="Comprehensive Financial Dashboard",
            showlegend=True,
            height=1000,
            title_font_size=20
        )
        
        return fig
    
    def create_sentiment_analysis_chart(self, sentiment_data: Dict) -> go.Figure:
        """Create sentiment analysis visualization"""
        
        sentiment_summary = sentiment_data.get('sentiment_summary', {})
        
        if not sentiment_summary:
            # Create empty chart
            fig = go.Figure()
            fig.add_annotation(
                text="No sentiment data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            return fig
        
        # Create subplots for sentiment analysis
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Sentiment Distribution (VADER)', 'Sentiment Over Time',
                'News Source Breakdown', 'Sentiment Confidence'
            ),
            specs=[
                [{"type": "pie"}, {"type": "scatter"}],
                [{"type": "bar"}, {"type": "bar"}]
            ]
        )
        
        # VADER Sentiment Distribution
        vader_sentiment = sentiment_summary.get('vader_sentiment', {})
        if vader_sentiment:
            sentiments = ['Positive', 'Neutral', 'Negative']
            values = [
                vader_sentiment.get('positive_articles', 0),
                vader_sentiment.get('neutral_articles', 0),
                vader_sentiment.get('negative_articles', 0)
            ]
            colors = [self.color_palette['success'], self.color_palette['info'], self.color_palette['danger']]
            
            fig.add_trace(
                go.Pie(
                    labels=sentiments,
                    values=values,
                    name="VADER Sentiment",
                    marker_colors=colors
                ),
                row=1, col=1
            )
        
        # FinBERT Sentiment (if available)
        finbert_sentiment = sentiment_summary.get('finbert_sentiment', {})
        if finbert_sentiment:
            fb_sentiments = ['Positive', 'Neutral', 'Negative']
            fb_values = [
                finbert_sentiment.get('positive_percentage', 0),
                finbert_sentiment.get('neutral_percentage', 0),
                finbert_sentiment.get('negative_percentage', 0)
            ]
            
            fig.add_trace(
                go.Bar(
                    x=fb_sentiments,
                    y=fb_values,
                    name='FinBERT Sentiment %',
                    marker_color=[self.color_palette['success'], self.color_palette['info'], self.color_palette['danger']]
                ),
                row=2, col=1
            )
        
        # News articles timeline (mock data for demonstration)
        articles = sentiment_data.get('news_articles', [])
        if articles:
            # Group articles by date for timeline
            dates = []
            sentiment_scores = []
            
            for article in articles[:10]:  # Limit to 10 for visualization
                if article.get('published_at'):
                    dates.append(article['published_at'][:10])  # Extract date
                    # Mock sentiment score for visualization
                    sentiment_scores.append(np.random.uniform(-1, 1))
            
            if dates:
                fig.add_trace(
                    go.Scatter(
                        x=dates,
                        y=sentiment_scores,
                        mode='markers+lines',
                        name='Article Sentiment',
                        marker=dict(
                            size=8,
                            color=sentiment_scores,
                            colorscale='RdYlGn',
                            cmin=-1,
                            cmax=1
                        )
                    ),
                    row=1, col=2
                )
        
        # Overall sentiment score
        overall_score = vader_sentiment.get('average_compound_score', 0)
        fig.add_trace(
            go.Bar(
                x=['Overall Sentiment'],
                y=[overall_score],
                name='Compound Score',
                marker_color=self.color_palette['success'] if overall_score > 0 else self.color_palette['danger']
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="News Sentiment Analysis Dashboard",
            showlegend=True,
            height=800
        )
        
        return fig
    
    def create_financial_ratios_heatmap(self, ratios_data: Dict) -> go.Figure:
        """Create a heatmap of financial ratios"""
        
        # Prepare data for heatmap
        categories = []
        metrics = []
        values = []
        
        for category, ratios in ratios_data.items():
            if isinstance(ratios, dict):
                for metric, value in ratios.items():
                    if value is not None and isinstance(value, (int, float)):
                        categories.append(category.replace('_', ' ').title())
                        metrics.append(metric.replace('_', ' ').title())
                        # Normalize values for better visualization
                        normalized_value = min(max(value, -5), 5) if abs(value) > 1 else value
                        values.append(normalized_value)
        
        if not values:
            fig = go.Figure()
            fig.add_annotation(
                text="No ratio data available for heatmap",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False, font_size=16
            )
            return fig
        
        # Create DataFrame for heatmap
        df = pd.DataFrame({
            'Category': categories,
            'Metric': metrics,
            'Value': values
        })
        
        # Pivot for heatmap
        heatmap_data = df.pivot_table(index='Metric', columns='Category', values='Value', fill_value=0)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='RdYlGn',
            text=heatmap_data.values,
            texttemplate="%{text:.2f}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Financial Ratios Heatmap",
            xaxis_title="Categories",
            yaxis_title="Metrics",
            height=600
        )
        
        return fig
    
    def create_comparison_chart(self, company_data: Dict, peer_data: List[Dict] = None) -> go.Figure:
        """Create peer comparison chart"""
        
        if not peer_data:
            # Create single company metrics chart
            ratios = company_data.get('financial_ratios', {})
            profitability = ratios.get('profitability', {})
            
            metrics = []
            values = []
            
            for metric, value in profitability.items():
                if value is not None and isinstance(value, (int, float)):
                    metrics.append(metric.replace('_', ' ').title())
                    values.append(value * 100 if value < 1 else value)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=metrics,
                y=values,
                name='Company Metrics',
                marker_color=self.color_palette['primary']
            ))
            
            fig.update_layout(
                title="Company Financial Metrics",
                xaxis_title="Metrics",
                yaxis_title="Values (%)",
                height=400
            )
            
            return fig
        
        # Peer comparison logic would go here
        # For now, return placeholder
        fig = go.Figure()
        fig.add_annotation(
            text="Peer comparison feature coming soon",
            xref="paper", yref="paper",
            x=0.5, y=0.5, xanchor='center', yanchor='middle',
            showarrow=False, font_size=16
        )
        
        return fig
    
    def create_risk_assessment_chart(self, financial_data: Dict) -> go.Figure:
        """Create risk assessment visualization"""
        
        ratios = financial_data.get('financial_ratios', {})
        
        # Risk factors
        risk_factors = {
            'Liquidity Risk': self.assess_liquidity_risk(ratios.get('liquidity', {})),
            'Leverage Risk': self.assess_leverage_risk(ratios.get('leverage', {})),
            'Profitability Risk': self.assess_profitability_risk(ratios.get('profitability', {})),
            'Valuation Risk': self.assess_valuation_risk(ratios.get('valuation', {}))
        }
        
        # Create radar chart
        categories = list(risk_factors.keys())
        values = list(risk_factors.values())
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Risk Assessment',
            line_color=self.color_palette['warning']
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            title="Risk Assessment Radar Chart",
            height=500
        )
        
        return fig
    
    def assess_liquidity_risk(self, liquidity_ratios: Dict) -> float:
        """Assess liquidity risk (0-10 scale, 10 being highest risk)"""
        current_ratio = liquidity_ratios.get('current_ratio')
        quick_ratio = liquidity_ratios.get('quick_ratio')
        
        if current_ratio is None:
            return 5.0  # Neutral risk
        
        if current_ratio > 2.0:
            return 2.0  # Low risk
        elif current_ratio > 1.5:
            return 4.0  # Medium-low risk
        elif current_ratio > 1.0:
            return 6.0  # Medium risk
        else:
            return 9.0  # High risk
    
    def assess_leverage_risk(self, leverage_ratios: Dict) -> float:
        """Assess leverage risk"""
        debt_to_equity = leverage_ratios.get('debt_to_equity')
        
        if debt_to_equity is None:
            return 5.0
        
        if debt_to_equity < 0.3:
            return 2.0
        elif debt_to_equity < 0.6:
            return 4.0
        elif debt_to_equity < 1.0:
            return 6.0
        else:
            return 8.0
    
    def assess_profitability_risk(self, profitability_ratios: Dict) -> float:
        """Assess profitability risk"""
        roe = profitability_ratios.get('roe')
        profit_margin = profitability_ratios.get('profit_margin')
        
        if roe is None and profit_margin is None:
            return 5.0
        
        # Use ROE as primary indicator
        if roe is not None:
            if roe > 0.15:
                return 2.0
            elif roe > 0.10:
                return 4.0
            elif roe > 0.05:
                return 6.0
            else:
                return 8.0
        
        return 5.0
    
    def assess_valuation_risk(self, valuation_ratios: Dict) -> float:
        """Assess valuation risk"""
        pe_ratio = valuation_ratios.get('pe_ratio')
        
        if pe_ratio is None:
            return 5.0
        
        if pe_ratio < 15:
            return 3.0
        elif pe_ratio < 25:
            return 5.0
        elif pe_ratio < 35:
            return 7.0
        else:
            return 9.0

    def create_price_chart(self, ticker: str) -> Optional[go.Figure]:
        """Create a comprehensive price chart with technical indicators"""
        try:
            import yfinance as yf
            
            # Fetch stock data
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            
            if hist.empty:
                return None
            
            # Create subplots with secondary y-axis
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=[f'{ticker} Stock Price', 'Volume'],
                specs=[[{"secondary_y": True}], [{"secondary_y": False}]],
                vertical_spacing=0.3,
                row_heights=[0.7, 0.3]
            )
            
            # Add candlestick chart
            fig.add_trace(
                go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close'],
                    name=f'{ticker} Price',
                    increasing_line_color=self.color_palette['success'],
                    decreasing_line_color=self.color_palette['danger']
                ),
                row=1, col=1
            )
            
            # Add moving averages
            hist['MA20'] = hist['Close'].rolling(window=20).mean()
            hist['MA50'] = hist['Close'].rolling(window=50).mean()
            hist['MA200'] = hist['Close'].rolling(window=200).mean()
            
            fig.add_trace(
                go.Scatter(
                    x=hist.index,
                    y=hist['MA20'],
                    mode='lines',
                    name='MA 20',
                    line=dict(color=self.color_palette['primary'], width=1)
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=hist.index,
                    y=hist['MA50'],
                    mode='lines',
                    name='MA 50',
                    line=dict(color=self.color_palette['secondary'], width=1)
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=hist.index,
                    y=hist['MA200'],
                    mode='lines',
                    name='MA 200',
                    line=dict(color=self.color_palette['warning'], width=2)
                ),
                row=1, col=1
            )
            
            # Add volume bars
            fig.add_trace(
                go.Bar(
                    x=hist.index,
                    y=hist['Volume'],
                    name='Volume',
                    marker_color=self.color_palette['info'],
                    opacity=0.7
                ),
                row=2, col=1
            )
            
            # Update layout
            fig.update_layout(
                title=f'{ticker} Stock Analysis',
                template='plotly_white',
                height=600,
                showlegend=True,
                xaxis_rangeslider_visible=False
            )
            
            # Update x-axis
            fig.update_xaxes(title_text="Date", row=2, col=1)
            
            # Update y-axis
            fig.update_yaxes(title_text="Price ($)", row=1, col=1)
            fig.update_yaxes(title_text="Volume", row=2, col=1)
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating price chart: {e}")
            return None

    def create_financial_ratios_chart(self, financial_metrics: Dict) -> Optional[go.Figure]:
        """Create a financial ratios visualization chart"""
        try:
            if not financial_metrics:
                return None
            
            # Extract key ratios
            ratios = {}
            basic_info = financial_metrics.get('basic_info', {})
            
            # Add key financial ratios
            if 'trailingPE' in basic_info:
                ratios['P/E Ratio'] = basic_info['trailingPE']
            if 'priceToBook' in basic_info:
                ratios['P/B Ratio'] = basic_info['priceToBook']
            if 'debtToEquity' in basic_info:
                ratios['Debt/Equity'] = basic_info['debtToEquity']
            if 'returnOnEquity' in basic_info:
                ratios['ROE (%)'] = basic_info['returnOnEquity'] * 100
            if 'grossMargins' in basic_info:
                ratios['Gross Margin (%)'] = basic_info['grossMargins'] * 100
            if 'operatingMargins' in basic_info:
                ratios['Operating Margin (%)'] = basic_info['operatingMargins'] * 100
            
            if not ratios:
                return None
            
            # Create bar chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=list(ratios.keys()),
                y=list(ratios.values()),
                marker_color=[
                    self.color_palette['primary'],
                    self.color_palette['secondary'],
                    self.color_palette['danger'],
                    self.color_palette['success'],
                    self.color_palette['info'],
                    self.color_palette['warning']
                ][:len(ratios)],
                text=[f"{v:.2f}" for v in ratios.values()],
                textposition='auto'
            ))
            
            fig.update_layout(
                title='Key Financial Ratios',
                template='plotly_white',
                height=400,
                showlegend=False,
                yaxis_title='Value'
            )
            
            return fig
            
        except Exception as e:
            st.error(f"Error creating financial ratios chart: {e}")
            return None
