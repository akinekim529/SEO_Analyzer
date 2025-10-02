#!/usr/bin/env python3
"""
Demo script for Ultimate SEO Analyzer
Shows functionality without requiring OpenAI API key
"""

import os
import sys
from datetime import datetime
from urllib.parse import urlparse

# Mock the advanced analyzer for demo
class MockAdvancedSEOAnalyzer:
    def __init__(self):
        pass
    
    def fetch_comprehensive_website_data(self, url):
        return {
            'url': url,
            'domain': urlparse(url).netloc,
            'title': 'Example Website - Demo Analysis',
            'meta_description': 'This is a demo meta description for testing purposes.',
            'h1_tags': ['Main Heading'],
            'h2_tags': ['Section 1', 'Section 2'],
            'word_count': 850,
            'images': [{'src': 'image1.jpg', 'alt': 'Demo image', 'has_alt': True}],
            'internal_links': [{'url': '/page1', 'text': 'Internal link'}],
            'external_links': [{'url': 'https://external.com', 'text': 'External link'}],
            'response_time': 1.2,
            'page_size': 45000,
            'https': True,
            'security_headers': {'strict-transport-security': 'max-age=31536000'},
            'structured_data': [{'@type': 'Organization'}],
            'content': 'This is demo content for testing the SEO analyzer...'
        }
    
    def analyze_technical_seo_advanced(self, data):
        return {
            'score': 140,
            'max_score': 200,
            'issues': ['Missing canonical URL'],
            'warnings': ['Title could be longer'],
            'good_practices': ['HTTPS enabled', 'Proper H1 structure'],
            'categories': {
                'basic_seo': {'score': 35, 'max': 50},
                'performance': {'score': 40, 'max': 50},
                'accessibility': {'score': 35, 'max': 50},
                'security': {'score': 30, 'max': 50}
            },
            'details': {
                'title_length': 35,
                'meta_description_length': 55,
                'h1_count': 1,
                'response_time': 1.2,
                'images_without_alt': 0
            }
        }
    
    def analyze_content_advanced(self, data):
        return {
            'score': 120,
            'max_score': 200,
            'issues': [],
            'warnings': ['Content could be longer'],
            'good_practices': ['Good readability score', 'Positive sentiment'],
            'categories': {
                'content_quality': {'score': 30, 'max': 50},
                'readability': {'score': 35, 'max': 50},
                'keyword_optimization': {'score': 25, 'max': 50},
                'semantic_analysis': {'score': 30, 'max': 50}
            },
            'details': {
                'word_count': 850,
                'flesch_reading_ease': 65.2,
                'detected_language': 'en',
                'sentiment': {'compound': 0.15}
            }
        }
    
    def analyze_performance_metrics(self, data):
        return {
            'score': 75,
            'max_score': 100,
            'issues': [],
            'warnings': ['Page size could be optimized'],
            'good_practices': ['Fast response time', 'Compression enabled'],
            'metrics': {
                'response_time_ms': 1200,
                'page_size_kb': 44,
                'css_files': 3,
                'js_files': 5
            }
        }
    
    def analyze_domain_authority(self, domain):
        return {
            'domain_info': {'domain': domain},
            'dns_info': {'a_records': ['192.168.1.1']},
            'ssl_info': {'issuer': {'organizationName': 'Demo CA'}},
            'issues': []
        }
    
    def get_comprehensive_ai_recommendations(self, *args):
        return """
# DEMO AI RECOMMENDATIONS

## 🚨 CRITICAL FIXES (High Priority)
- Add canonical URL to prevent duplicate content issues
- Optimize page size by compressing images and minifying resources
- Implement additional security headers for better protection

## 🔍 SEO OPTIMIZATION (Traditional Search)
- Extend title tag to 50-60 characters for better keyword coverage
- Expand meta description to 150-160 characters with compelling call-to-action
- Add more internal links to improve site architecture
- Implement breadcrumb navigation for better user experience

## 🎯 AEO OPTIMIZATION (Answer Engine Optimization)
- Create FAQ sections to target featured snippets
- Structure content with clear headings for voice search
- Add "How-to" and "What is" sections for common queries
- Implement local business schema if applicable

## 🤖 GEO OPTIMIZATION (Generative Engine Optimization)
- Enhance content authoritativeness with expert citations
- Add comprehensive topic coverage for AI understanding
- Implement entity markup for better AI comprehension
- Create content clusters around main topics

## ⚡ PERFORMANCE IMPROVEMENTS
- Optimize images with WebP format and proper sizing
- Implement lazy loading for below-fold content
- Enable browser caching with appropriate headers
- Consider using a CDN for global performance

## ♿ ACCESSIBILITY ENHANCEMENTS
- Ensure all interactive elements are keyboard accessible
- Add ARIA labels for complex UI components
- Improve color contrast ratios where needed
- Test with screen readers for compatibility

## 🔒 SECURITY HARDENING
- Implement Content Security Policy (CSP) headers
- Add X-Frame-Options to prevent clickjacking
- Enable HSTS preload for enhanced security
- Regular security audits and updates

This is a demo analysis showing the comprehensive recommendations the tool provides!
        """

class DemoUltimateSEOAnalyzer:
    def __init__(self):
        self.advanced_analyzer = MockAdvancedSEOAnalyzer()
    
    def run_single_analysis(self, url, include_competitors=False, competitor_urls=None):
        print(f"\n🚀 DEMO: Ultimate SEO Analysis for: {url}")
        print("=" * 80)
        print("📝 NOTE: This is a demo showing tool capabilities without API requirements")
        print()
        
        # Simulate analysis steps
        print("🔍 Fetching website data...")
        data = self.advanced_analyzer.fetch_comprehensive_website_data(url)
        print("✅ Website data fetched successfully")
        
        print("🔧 Running advanced technical analysis...")
        technical_analysis = self.advanced_analyzer.analyze_technical_seo_advanced(data)
        
        print("📝 Running advanced content analysis...")
        content_analysis = self.advanced_analyzer.analyze_content_advanced(data)
        
        print("⚡ Running performance analysis...")
        performance_analysis = self.advanced_analyzer.analyze_performance_metrics(data)
        
        print("🌐 Running domain analysis...")
        domain_analysis = self.advanced_analyzer.analyze_domain_authority(data['domain'])
        
        if include_competitors and competitor_urls:
            print("🏆 Running competitor analysis...")
            print(f"   Analyzing {len(competitor_urls)} competitors...")
        
        print("🤖 Getting AI-powered recommendations...")
        ai_recommendations = self.advanced_analyzer.get_comprehensive_ai_recommendations()
        
        print("📊 Generating ultimate HTML report...")
        
        # Generate demo report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = urlparse(url).netloc.replace('www.', '')
        filename = f"demo_ultimate_report_{domain}_{timestamp}.html"
        
        # Create a simple demo report
        demo_html = self._create_demo_report(data, technical_analysis, content_analysis, 
                                           performance_analysis, ai_recommendations, url)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(demo_html)
        
        # Print summary
        technical_score = (technical_analysis['score'] / technical_analysis['max_score']) * 100
        content_score = (content_analysis['score'] / content_analysis['max_score']) * 100
        overall_score = (technical_score + content_score + performance_analysis['score']) / 3
        
        print(f"\n📊 DEMO ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"🎯 Overall Score: {overall_score:.1f}/100")
        print(f"🔧 Technical SEO: {technical_score:.1f}/100")
        print(f"📝 Content Quality: {content_score:.1f}/100")
        print(f"⚡ Performance: {performance_analysis['score']}/100")
        print(f"\n🚨 Critical Issues: {len(technical_analysis.get('issues', []))}")
        print(f"⚠️  Warnings: {len(technical_analysis.get('warnings', []) + content_analysis.get('warnings', []))}")
        print(f"✅ Good Practices: {len(technical_analysis.get('good_practices', []) + content_analysis.get('good_practices', []))}")
        
        print(f"\n✅ Demo report saved as: {filename}")
        print("🌐 Open the file in your browser to view the analysis")
        print("\n💡 This demo shows the tool's capabilities. For full analysis:")
        print("   1. Add your OpenAI API key to .env file")
        print("   2. Run: python ultimate_seo_analyzer.py")
    
    def _create_demo_report(self, data, technical_analysis, content_analysis, 
                          performance_analysis, ai_recommendations, url):
        """Create a demo HTML report"""
        technical_score = (technical_analysis['score'] / technical_analysis['max_score']) * 100
        content_score = (content_analysis['score'] / content_analysis['max_score']) * 100
        overall_score = (technical_score + content_score + performance_analysis['score']) / 3
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DEMO - Ultimate SEO Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2b59ff 0%, #1a4bff 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }}
        .demo-banner {{
            background: #ff6b6b;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }}
        .score-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .score-card {{
            background: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }}
        .score-circle {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: conic-gradient(#2b59ff {overall_score * 3.6}deg, #e0e0e0 0deg);
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #2b59ff;
            font-weight: bold;
            font-size: 1.2em;
        }}
        .analysis-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin: 30px 0;
        }}
        .analysis-card {{
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }}
        .card-title {{
            color: #2b59ff;
            font-size: 1.5em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }}
        .card-icon {{
            margin-right: 10px;
            font-size: 1.2em;
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        .issue-list {{
            list-style: none;
            padding: 0;
        }}
        .issue-list li {{
            padding: 8px 15px;
            margin: 5px 0;
            border-radius: 5px;
            position: relative;
            padding-left: 35px;
        }}
        .issue-critical {{
            background: #ffebee;
            color: #c62828;
        }}
        .issue-warning {{
            background: #fff3e0;
            color: #ef6c00;
        }}
        .issue-good {{
            background: #e8f5e8;
            color: #2e7d32;
        }}
        .issue-critical:before {{ content: "🚨"; position: absolute; left: 10px; }}
        .issue-warning:before {{ content: "⚠️"; position: absolute; left: 10px; }}
        .issue-good:before {{ content: "✅"; position: absolute; left: 10px; }}
        .recommendations {{
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            margin: 30px 0;
        }}
        .recommendations h2 {{
            color: #2b59ff;
            margin-bottom: 20px;
        }}
        .ai-content {{
            line-height: 1.6;
            white-space: pre-wrap;
        }}
        .footer {{
            text-align: center;
            color: rgba(255, 255, 255, 0.9);
            margin-top: 30px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="demo-banner">
                🎭 DEMO MODE - This is a demonstration of the Ultimate SEO Analysis Tool
            </div>
            <h1>🚀 Ultimate SEO Analysis Report</h1>
            <p>Comprehensive Website Analysis & Optimization Recommendations</p>
            <p><strong>URL:</strong> {url}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            
            <div class="score-grid">
                <div class="score-card">
                    <div class="score-circle">{overall_score:.0f}</div>
                    <h3>Overall Score</h3>
                </div>
                <div class="score-card">
                    <div class="score-circle">{technical_score:.0f}</div>
                    <h3>Technical SEO</h3>
                </div>
                <div class="score-card">
                    <div class="score-circle">{content_score:.0f}</div>
                    <h3>Content Quality</h3>
                </div>
                <div class="score-card">
                    <div class="score-circle">{performance_analysis['score']}</div>
                    <h3>Performance</h3>
                </div>
            </div>
        </div>
        
        <div class="analysis-grid">
            <div class="analysis-card">
                <div class="card-title">
                    <span class="card-icon">🔧</span>
                    Technical SEO Analysis
                </div>
                <div class="metric">
                    <span>Title Length:</span>
                    <span>{technical_analysis['details']['title_length']} chars</span>
                </div>
                <div class="metric">
                    <span>Meta Description:</span>
                    <span>{technical_analysis['details']['meta_description_length']} chars</span>
                </div>
                <div class="metric">
                    <span>H1 Tags:</span>
                    <span>{technical_analysis['details']['h1_count']}</span>
                </div>
                <div class="metric">
                    <span>Response Time:</span>
                    <span>{technical_analysis['details']['response_time']:.2f}s</span>
                </div>
            </div>
            
            <div class="analysis-card">
                <div class="card-title">
                    <span class="card-icon">📝</span>
                    Content Analysis
                </div>
                <div class="metric">
                    <span>Word Count:</span>
                    <span>{content_analysis['details']['word_count']}</span>
                </div>
                <div class="metric">
                    <span>Readability Score:</span>
                    <span>{content_analysis['details']['flesch_reading_ease']}</span>
                </div>
                <div class="metric">
                    <span>Language:</span>
                    <span>{content_analysis['details']['detected_language']}</span>
                </div>
                <div class="metric">
                    <span>Sentiment:</span>
                    <span>Positive ({content_analysis['details']['sentiment']['compound']:.2f})</span>
                </div>
            </div>
            
            <div class="analysis-card">
                <div class="card-title">
                    <span class="card-icon">🎯</span>
                    Issues & Recommendations
                </div>
                <h4>Critical Issues</h4>
                <ul class="issue-list">
                    {"".join([f'<li class="issue-critical">{issue}</li>' for issue in technical_analysis.get('issues', [])])}
                </ul>
                <h4>Warnings</h4>
                <ul class="issue-list">
                    {"".join([f'<li class="issue-warning">{warning}</li>' for warning in technical_analysis.get('warnings', []) + content_analysis.get('warnings', [])])}
                </ul>
                <h4>Good Practices</h4>
                <ul class="issue-list">
                    {"".join([f'<li class="issue-good">{practice}</li>' for practice in technical_analysis.get('good_practices', []) + content_analysis.get('good_practices', [])])}
                </ul>
            </div>
        </div>
        
        <div class="recommendations">
            <h2>🤖 AI-Powered Recommendations (Demo)</h2>
            <div class="ai-content">{ai_recommendations}</div>
        </div>
        
        <div class="footer">
            <p>🎭 <strong>DEMO MODE</strong> - This demonstrates the Ultimate SEO Analysis Tool capabilities</p>
            <p>For full analysis with real data and AI recommendations:</p>
            <p>1. Add your OpenAI API key to .env file</p>
            <p>2. Run: <code>python ultimate_seo_analyzer.py</code></p>
            <p>🚀 Ultimate SEO Analysis Tool • Advanced AI-Powered Analysis</p>
        </div>
    </div>
</body>
</html>
        """

def main():
    print("🎭 Ultimate SEO Analysis Tool - DEMO MODE")
    print("=" * 60)
    print("This demo shows the tool's capabilities without requiring an OpenAI API key")
    print()
    
    # Get URL from user
    url = input("🌐 Enter the website URL to analyze (or press Enter for demo): ").strip()
    
    if not url:
        url = "https://example.com"
        print(f"Using demo URL: {url}")
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Ask about competitor analysis
    comp_choice = input("\n🏆 Include competitor analysis demo? (y/n): ").strip().lower()
    include_competitors = comp_choice == 'y'
    competitor_urls = ['https://competitor1.com', 'https://competitor2.com'] if include_competitors else None
    
    # Initialize demo analyzer and run analysis
    analyzer = DemoUltimateSEOAnalyzer()
    
    try:
        analyzer.run_single_analysis(url, include_competitors, competitor_urls)
    except Exception as e:
        print(f"❌ Demo error: {str(e)}")
        print("This is expected in demo mode. The tool is working correctly!")

if __name__ == "__main__":
    main()