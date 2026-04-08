#!/bin/bash
# FitHub CRM - Startup Script for macOS/Linux

echo ""
echo "================================================"
echo "  FitHub CRM - Fitness Center Management"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 from https://www.python.org"
    exit 1
fi

echo "[1/4] Checking Python installation..."
python3 --version

echo "[2/4] Installing dependencies..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "[3/4] Checking database..."
if [ ! -f "fitness_crm.db" ]; then
    echo "Database not found. It will be created on startup."
fi

echo "[4/4] Starting FitHub CRM Server..."
echo ""
echo "================================================"
echo "  Server starting..."
echo "  Open: http://localhost:5000"
echo "================================================"
echo ""

python3 run.py
