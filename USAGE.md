# SEO Analysis Tool - Usage Guide

## 🚀 Quick Start

### 1. Installation
```bash
# Install dependencies
pip3 install -r requirements.txt

# Or use the installation script
./install.sh
```

### 2. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

### 3. Run Analysis
```bash
# Run the main analyzer
python3 seo_analyzer.py

# Or try the demo version (no API key needed)
python3 demo.py
```

## 📊 Features

### Comprehensive SEO Analysis
- **Technical SEO**: Title tags, meta descriptions, headers, images, response time
- **Content Analysis**: Word count, keyword density, internal/external links
- **Structured Data**: JSON-LD schema detection
- **Performance Metrics**: Page load time, content size

### AI-Powered Recommendations
- **SEO**: Traditional search engine optimization
- **AEO**: Answer Engine Optimization for voice search and featured snippets
- **GEO**: Generative Engine Optimization for AI search engines
- **Priority Actions**: High, medium, and low priority recommendations

### Beautiful HTML Reports
- **Modern Design**: Clean, professional layout with #2b59ff color scheme
- **Animations**: Smooth transitions and loading effects
- **Responsive**: Works on desktop and mobile devices
- **Interactive Elements**: Hover effects and progress indicators

## 🎯 What Gets Analyzed

### Technical SEO Factors
- Page title optimization (length, keywords)
- Meta description quality and length
- Header structure (H1, H2, H3 hierarchy)
- Image optimization (alt text, file sizes)
- Page loading speed
- Content length and quality
- Internal and external link structure
- Structured data implementation

### Content Quality Metrics
- Word count analysis
- Keyword density evaluation
- Content readability
- Link distribution
- Schema markup detection

### AI-Enhanced Insights
- SEO best practices recommendations
- AEO optimization for voice search
- GEO strategies for AI search engines
- Technical improvement suggestions
- Content strategy advice
- Prioritized action items

## 📋 Report Sections

### 1. Overall SEO Score
- Visual score circle with percentage
- Color-coded performance indicator
- Generated timestamp

### 2. Technical SEO Card
- Title and meta description analysis
- Response time metrics
- Header tag structure
- Image optimization status

### 3. Content Analysis Card
- Word count evaluation
- Link analysis (internal/external)
- Structured data detection

### 4. Issues Found Card
- Critical issues highlighted
- Warning indicators
- Success confirmations

### 5. AI Recommendations
- Comprehensive optimization strategies
- Specific, actionable advice
- Priority-based action items

## 🔧 Troubleshooting

### Common Issues

**"OPENAI_API_KEY not found"**
- Make sure you've created the `.env` file
- Add your actual OpenAI API key to the file
- Don't use quotes around the key value

**"Module not found" errors**
- Run `pip3 install -r requirements.txt`
- Make sure you're using Python 3.7 or higher

**Network/timeout errors**
- Check your internet connection
- Some websites may block automated requests
- Try with a different URL

**OpenAI API errors**
- Verify your API key is valid and has credits
- Check OpenAI service status
- The tool will still generate reports without AI recommendations

### Testing Your Setup
```bash
# Test if all dependencies are installed
python3 test_setup.py

# Run demo without API key
python3 demo.py
```

## 🌐 Supported Websites

The tool works with most public websites that:
- Are accessible via HTTP/HTTPS
- Don't require authentication
- Allow automated requests
- Have standard HTML structure

## 📈 Understanding Your Report

### SEO Score Calculation
- **Technical SEO**: 50 points maximum
- **Content Quality**: 50 points maximum
- **Total Score**: 0-100 scale

### Color Coding
- **Green**: Good performance
- **Orange**: Needs improvement
- **Red**: Critical issues

### Priority Levels
- **High**: Critical issues affecting SEO performance
- **Medium**: Important optimizations for better rankings
- **Low**: Advanced optimizations for competitive advantage

## 🤖 AI Recommendations Explained

### SEO (Search Engine Optimization)
Traditional optimization for Google, Bing, and other search engines

### AEO (Answer Engine Optimization)
Optimization for voice assistants, featured snippets, and answer boxes

### GEO (Generative Engine Optimization)
Optimization for AI-powered search engines like ChatGPT, Bard, and future AI systems

## 📞 Support

If you encounter issues:
1. Check this usage guide
2. Run the test setup script
3. Try the demo version first
4. Verify your OpenAI API key and credits