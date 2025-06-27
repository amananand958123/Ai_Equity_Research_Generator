#!/bin/bash

# Equity Research Report Generator - Startup Script
# This script starts both the backend Python server and frontend Next.js server

set -e

echo "🚀 Starting Equity Research Report Generator"
echo "==========================================="

# Check if we're in the right directory
if [ ! -f "bridge_server.py" ]; then
    echo "❌ Error: bridge_server.py not found. Please run this script from the project root."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found. Please set up the Python environment first."
    echo "   Run: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo -e "\n🛑 Shutting down servers..."
    # Kill backend server
    pkill -f bridge_server.py 2>/dev/null || true
    # Kill frontend server
    pkill -f "next dev" 2>/dev/null || true
    echo "✅ Cleanup complete"
    exit 0
}

# Set up signal handlers for clean shutdown
trap cleanup SIGINT SIGTERM

echo "📦 Installing/updating dependencies..."

# Install Python dependencies
echo "   - Installing Python packages..."
.venv/bin/pip install -q -r requirements.txt

# Install Node.js dependencies for frontend
echo "   - Installing Node.js packages..."
cd frontend
npm install --silent
cd ..

echo "🔧 Starting backend server..."
.venv/bin/python bridge_server.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

echo "🌐 Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
sleep 3

echo ""
echo "✅ Both servers are running!"
echo "   🐍 Backend:  http://localhost:5001"
echo "   🌐 Frontend: http://localhost:3000"
echo ""
echo "📖 Open http://localhost:3000 in your browser to use the application"
echo "🛑 Press Ctrl+C to stop both servers"
echo ""

# Wait for either process to exit
wait $BACKEND_PID $FRONTEND_PID
