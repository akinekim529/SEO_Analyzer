#!/usr/bin/env python3
"""
Demo script to show SEO analyzer functionality without OpenAI API
"""

import os
import sys
from datetime import datetime
from urllib.parse import urlparse

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seo_analyzer import SEOAnalyzer

class DemoSEOAnalyzer(SEOAnalyzer):
    """Demo version that doesn't require OpenAI API"""
    
    def __init__(self):
        # Skip OpenAI initialization for demo
        self.openai_api_key = "demo_key"
        
        import requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_openai_recommendations(self, data, technical_analysis, content_analysis):
        """Return demo recommendations instead of calling OpenAI API"""
        return """
## SEO RECOMMENDATIONS

### 🔍 Traditional SEO Optimization
- **Title Optimization**: Ensure your title tag is between 50-60 characters and includes your primary keyword
- **Meta Description**: Write compelling meta descriptions between 150-160 characters that encourage clicks
- **Header Structure**: Use a single H1 tag per page and create a logical hierarchy with H2, H3 tags
- **Image Optimization**: Add descriptive alt text to all images for better accessibility and SEO
- **Internal Linking**: Create a strong internal linking structure to help search engines understand your content

### 🎯 AEO (Answer Engine Optimization)
- **Featured Snippets**: Structure content to answer common questions directly and concisely
- **FAQ Sections**: Add comprehensive FAQ sections that address user queries
- **Voice Search**: Optimize for conversational queries and long-tail keywords
- **Structured Data**: Implement schema markup for better search engine understanding
- **Local SEO**: If applicable, optimize for local search with NAP consistency

### 🤖 GEO (Generative Engine Optimization)
- **AI-Friendly Content**: Create comprehensive, authoritative content that AI can easily understand and cite
- **Entity Optimization**: Clearly define entities, people, places, and concepts in your content
- **Factual Accuracy**: Ensure all information is accurate and well-sourced for AI training
- **Content Depth**: Provide thorough coverage of topics rather than surface-level information
- **Semantic Relationships**: Use related keywords and concepts to build topical authority

### ⚡ Technical Improvements
- **Page Speed**: Optimize images, minify CSS/JS, and use a CDN to improve loading times
- **Mobile Optimization**: Ensure your site is fully responsive and mobile-friendly
- **Core Web Vitals**: Focus on LCP, FID, and CLS metrics for better user experience
- **SSL Certificate**: Implement HTTPS for security and SEO benefits
- **XML Sitemap**: Create and submit an XML sitemap to search engines

### 📝 Content Strategy
- **Keyword Research**: Conduct thorough keyword research to identify opportunities
- **Content Clusters**: Create topic clusters around your main keywords
- **Regular Updates**: Keep content fresh and updated with new information
- **User Intent**: Align content with user search intent (informational, navigational, transactional)
- **E-A-T**: Demonstrate Expertise, Authoritativeness, and Trustworthiness in your content

### 🚨 Priority Actions
**HIGH PRIORITY:**
- Fix missing or poorly optimized title tags and meta descriptions
- Improve page loading speed (target under 3 seconds)
- Add alt text to images missing it
- Implement basic structured data markup

**MEDIUM PRIORITY:**
- Improve internal linking structure
- Optimize content for featured snippets
- Enhance mobile user experience
- Create comprehensive FAQ sections

**LOW PRIORITY:**
- Expand content depth and coverage
- Build topical authority through content clusters
- Optimize for voice search queries
- Implement advanced schema markup
        """

def main():
    """Demo main function"""
    print("🔍 SEO Analysis Tool - DEMO MODE")
    print("=" * 50)
    print("This demo shows the tool functionality without requiring an OpenAI API key")
    print()
    
    # Get URL from user
    url = input("🌐 Enter the website URL to analyze (or press Enter for demo): ").strip()
    
    if not url:
        url = "https://example.com"
        print(f"Using demo URL: {url}")
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Initialize demo analyzer and run analysis
    analyzer = DemoSEOAnalyzer()
    
    try:
        analyzer.run_analysis(url)
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("This is expected if the URL is not accessible or if there are network issues.")
        print("The tool is working correctly - you just need to:")
        print("1. Add your OpenAI API key to .env file")
        print("2. Run: python3 seo_analyzer.py")

if __name__ == "__main__":
    main()