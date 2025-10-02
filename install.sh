#!/bin/bash

echo "🚀 Installing Ultimate SEO Analysis Tool"
echo "========================================"
echo "The most comprehensive free and open-source SEO analysis tool"
echo ""

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
echo "📋 Next Steps:"
echo "1. Edit .env file and add your OpenAI API key:"
echo "   OPENAI_API_KEY=your_actual_api_key_here"
echo ""
echo "2. Run the Ultimate SEO Analyzer:"
echo "   python3 ultimate_seo_analyzer.py https://example.com"
echo ""
echo "3. Or run in interactive mode:"
echo "   python3 ultimate_seo_analyzer.py"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Complete feature overview"
echo "   - USAGE.md - Detailed usage guide"
echo "   - CONTRIBUTING.md - How to contribute"
echo ""
echo "🆘 Need help? Check the troubleshooting guide in README.md"
echo "🐛 Found a bug? Report it at: https://github.com/yourusername/ultimate-seo-analyzer/issues"
echo ""
echo "⭐ If this tool helps you, please give it a star on GitHub!"