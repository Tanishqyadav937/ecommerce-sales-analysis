#!/bin/bash

# E-Commerce Analytics Pro - Installation Script

echo "🚀 Installing E-Commerce Analytics Pro..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment (optional but recommended)
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Installation complete!"
echo ""
echo "🎯 To run the dashboard:"
echo "   1. Activate the virtual environment: source venv/bin/activate"
echo "   2. Run the app: streamlit run app.py"
echo ""
echo "📖 For more information, see QUICKSTART.md"
