#!/bin/bash

echo "🚀 Installing Comprehensive Keyword Analysis Tool"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    echo "Please install pip3 and try again."
    exit 1
fi

echo "✅ pip3 found"

# Install required packages
echo "📦 Installing required packages..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ All packages installed successfully"
else
    echo "❌ Failed to install some packages"
    echo "Please check your internet connection and try again."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "Creating sample .env file..."
    echo "OPENAI_API_KEY=your_api_key_here" > .env
    echo "📝 Please edit .env file and add your OpenAI API key"
    echo "   You can get an API key from: https://platform.openai.com/api-keys"
else
    echo "✅ .env file found"
fi

# Make scripts executable
chmod +x comprehensive_keyword_tool.py
chmod +x demo_keyword_analysis.py

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file and add your OpenAI API key"
echo "2. Run demo: python3 demo_keyword_analysis.py"
echo "3. Or analyze a URL: python3 comprehensive_keyword_tool.py https://example.com"
echo ""
echo "📚 For detailed usage instructions, see README_KEYWORD_ANALYSIS.md"
echo ""