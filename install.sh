#!/bin/bash

echo "🚀 Installing SEO Analysis Tool"
echo "================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Install pip if not available
if ! command -v pip3 &> /dev/null; then
    echo "Installing pip..."
    python3 -m ensurepip --default-pip
fi

echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

echo "📝 Setting up environment file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo "⚠️  Please edit .env file and add your OpenAI API key"
else
    echo "✅ .env file already exists"
fi

echo "🧪 Testing installation..."
python3 test_setup.py

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📋 Usage:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run: python3 seo_analyzer.py"
echo "3. Enter website URL when prompted"