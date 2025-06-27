#!/bin/bash

# Equity Research Report Generator - Setup Script
# This script helps set up the development environment

echo "🚀 Equity Research Report Generator - Setup"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

echo "✅ Python and Node.js found"

# Create Python virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install frontend dependencies
echo "📥 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Create environment file from template
if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys:"
    echo "   - GOOGLE_API_KEY (Google Gemini)"
    echo "   - ALPHA_VANTAGE_API_KEY (Alpha Vantage)"
    echo "   - NEWS_API_KEY (NewsAPI)"
else
    echo "✅ Environment file already exists"
fi

# Make scripts executable
chmod +x start-servers.sh
chmod +x test-api.sh

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: ./start-servers.sh"
echo "3. Open http://localhost:3000"
echo ""
echo "📖 For more information, see:"
echo "   - README.md for general documentation"
echo "   - docs/FAQ.md for common questions"
echo "   - docs/API.md for API documentation"
echo ""
echo "🚀 Happy coding!"
