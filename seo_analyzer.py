#!/usr/bin/env python3
"""
Comprehensive SEO Analysis Tool
Analyzes websites for SEO, AEO, and GEO optimization using OpenAI API
"""

import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import openai
from dotenv import load_dotenv
from datetime import datetime
import re
import time
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

class SEOAnalyzer:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            print("❌ Error: OPENAI_API_KEY not found in .env file")
            sys.exit(1)
        
        self.client = openai.OpenAI(api_key=self.openai_api_key)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def fetch_website_data(self, url: str) -> Dict[str, Any]:
        """Fetch and parse website data"""
        try:
            print(f"🔍 Fetching website data from: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic data
            data = {
                'url': url,
                'status_code': response.status_code,
                'content_length': len(response.content),
                'response_time': response.elapsed.total_seconds(),
                'title': soup.find('title').get_text().strip() if soup.find('title') else '',
                'meta_description': '',
                'meta_keywords': '',
                'h1_tags': [h1.get_text().strip() for h1 in soup.find_all('h1')],
                'h2_tags': [h2.get_text().strip() for h2 in soup.find_all('h2')],
                'h3_tags': [h3.get_text().strip() for h3 in soup.find_all('h3')],
                'images': [],
                'links': [],
                'meta_tags': {},
                'structured_data': [],
                'content': soup.get_text()[:5000],  # First 5000 chars
                'html_content': str(soup)[:10000]  # First 10000 chars of HTML
            }
            
            # Extract meta tags
            for meta in soup.find_all('meta'):
                if meta.get('name') == 'description':
                    data['meta_description'] = meta.get('content', '')
                elif meta.get('name') == 'keywords':
                    data['meta_keywords'] = meta.get('content', '')
                elif meta.get('name'):
                    data['meta_tags'][meta.get('name')] = meta.get('content', '')
                elif meta.get('property'):
                    data['meta_tags'][meta.get('property')] = meta.get('content', '')
            
            # Extract images
            for img in soup.find_all('img'):
                img_data = {
                    'src': img.get('src', ''),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'width': img.get('width', ''),
                    'height': img.get('height', '')
                }
                data['images'].append(img_data)
            
            # Extract links
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http') or href.startswith('/'):
                    data['links'].append({
                        'url': urljoin(url, href),
                        'text': link.get_text().strip(),
                        'title': link.get('title', '')
                    })
            
            # Extract structured data (JSON-LD)
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    structured = json.loads(script.string)
                    data['structured_data'].append(structured)
                except:
                    pass
            
            return data
            
        except Exception as e:
            print(f"❌ Error fetching website data: {str(e)}")
            return None

    def analyze_technical_seo(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical SEO aspects"""
        analysis = {
            'score': 0,
            'issues': [],
            'recommendations': [],
            'details': {}
        }
        
        # Title analysis
        title = data.get('title', '')
        if not title:
            analysis['issues'].append('Missing page title')
        elif len(title) < 30:
            analysis['issues'].append('Title too short (less than 30 characters)')
        elif len(title) > 60:
            analysis['issues'].append('Title too long (more than 60 characters)')
        else:
            analysis['score'] += 10
        
        # Meta description analysis
        meta_desc = data.get('meta_description', '')
        if not meta_desc:
            analysis['issues'].append('Missing meta description')
        elif len(meta_desc) < 120:
            analysis['issues'].append('Meta description too short (less than 120 characters)')
        elif len(meta_desc) > 160:
            analysis['issues'].append('Meta description too long (more than 160 characters)')
        else:
            analysis['score'] += 10
        
        # Heading structure analysis
        h1_count = len(data.get('h1_tags', []))
        if h1_count == 0:
            analysis['issues'].append('Missing H1 tag')
        elif h1_count > 1:
            analysis['issues'].append(f'Multiple H1 tags found ({h1_count})')
        else:
            analysis['score'] += 10
        
        # Image optimization
        images_without_alt = [img for img in data.get('images', []) if not img.get('alt')]
        if images_without_alt:
            analysis['issues'].append(f'{len(images_without_alt)} images missing alt text')
        
        # Response time
        response_time = data.get('response_time', 0)
        if response_time > 3:
            analysis['issues'].append(f'Slow response time: {response_time:.2f}s')
        elif response_time < 1:
            analysis['score'] += 10
        
        analysis['details'] = {
            'title_length': len(title),
            'meta_description_length': len(meta_desc),
            'h1_count': h1_count,
            'h2_count': len(data.get('h2_tags', [])),
            'h3_count': len(data.get('h3_tags', [])),
            'total_images': len(data.get('images', [])),
            'images_without_alt': len(images_without_alt),
            'response_time': response_time,
            'content_length': data.get('content_length', 0)
        }
        
        return analysis

    def analyze_content_seo(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content SEO aspects"""
        analysis = {
            'score': 0,
            'issues': [],
            'recommendations': [],
            'details': {}
        }
        
        content = data.get('content', '')
        word_count = len(content.split())
        
        # Content length analysis
        if word_count < 300:
            analysis['issues'].append(f'Content too short ({word_count} words)')
        elif word_count > 2000:
            analysis['score'] += 10
        
        # Keyword density analysis (basic)
        title_words = data.get('title', '').lower().split()
        if title_words:
            main_keyword = max(title_words, key=len) if title_words else ''
            keyword_count = content.lower().count(main_keyword.lower())
            keyword_density = (keyword_count / word_count * 100) if word_count > 0 else 0
            
            if keyword_density < 0.5:
                analysis['issues'].append(f'Low keyword density for "{main_keyword}" ({keyword_density:.1f}%)')
            elif keyword_density > 3:
                analysis['issues'].append(f'High keyword density for "{main_keyword}" ({keyword_density:.1f}%)')
            else:
                analysis['score'] += 10
        
        # Internal/External links
        internal_links = [link for link in data.get('links', []) if urlparse(link['url']).netloc == urlparse(data['url']).netloc]
        external_links = [link for link in data.get('links', []) if urlparse(link['url']).netloc != urlparse(data['url']).netloc]
        
        analysis['details'] = {
            'word_count': word_count,
            'internal_links': len(internal_links),
            'external_links': len(external_links),
            'total_links': len(data.get('links', [])),
            'structured_data_count': len(data.get('structured_data', []))
        }
        
        return analysis

    def get_openai_recommendations(self, data: Dict[str, Any], technical_analysis: Dict, content_analysis: Dict) -> str:
        """Get AI-powered SEO recommendations from OpenAI"""
        try:
            prompt = f"""
            Analyze this website data and provide comprehensive SEO, AEO (Answer Engine Optimization), and GEO (Generative Engine Optimization) recommendations:

            Website: {data.get('url', '')}
            Title: {data.get('title', '')}
            Meta Description: {data.get('meta_description', '')}
            H1 Tags: {', '.join(data.get('h1_tags', []))}
            Word Count: {content_analysis['details'].get('word_count', 0)}
            Technical Issues: {', '.join(technical_analysis.get('issues', []))}
            Content Issues: {', '.join(content_analysis.get('issues', []))}

            Please provide:
            1. SEO Recommendations (traditional search optimization)
            2. AEO Recommendations (answer engine optimization for voice search, featured snippets)
            3. GEO Recommendations (generative engine optimization for AI search engines)
            4. Technical improvements
            5. Content strategy suggestions
            6. Priority actions (high, medium, low)

            Format as structured recommendations with specific, actionable advice.
            """
            
            print("🤖 Getting AI-powered recommendations...")
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert SEO consultant with deep knowledge of traditional SEO, AEO, and GEO optimization strategies."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️ Warning: Could not get OpenAI recommendations: {str(e)}")
            return "AI recommendations unavailable. Please check your OpenAI API key and connection."

    def generate_html_report(self, data: Dict[str, Any], technical_analysis: Dict, content_analysis: Dict, ai_recommendations: str) -> str:
        """Generate beautiful HTML report"""
        
        # Calculate overall score
        max_score = 100
        current_score = technical_analysis['score'] + content_analysis['score']
        score_percentage = min(100, (current_score / max_score) * 100)
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Analysis Report - {data.get('url', '')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2b59ff 0%, #1a4bff 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            animation: slideDown 0.8s ease-out;
        }}
        
        .header h1 {{
            color: #2b59ff;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-align: center;
        }}
        
        .header .url {{
            text-align: center;
            color: #666;
            font-size: 1.2em;
            margin-bottom: 20px;
        }}
        
        .score-circle {{
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: conic-gradient(#2b59ff {score_percentage * 3.6}deg, #e0e0e0 0deg);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            position: relative;
            animation: rotateIn 1s ease-out;
        }}
        
        .score-inner {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        }}
        
        .score-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2b59ff;
        }}
        
        .score-text {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .report-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        .report-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            animation: slideUp 0.8s ease-out;
            transition: transform 0.3s ease;
        }}
        
        .report-card:hover {{
            transform: translateY(-5px);
        }}
        
        .card-header {{
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }}
        
        .card-icon {{
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: linear-gradient(135deg, #2b59ff, #1a4bff);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            color: white;
            font-size: 1.2em;
        }}
        
        .card-title {{
            font-size: 1.5em;
            color: #2b59ff;
            font-weight: 600;
        }}
        
        .metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        .metric:last-child {{
            border-bottom: none;
        }}
        
        .metric-label {{
            color: #666;
        }}
        
        .metric-value {{
            font-weight: 600;
            color: #333;
        }}
        
        .issues-list {{
            list-style: none;
        }}
        
        .issues-list li {{
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
            color: #d32f2f;
        }}
        
        .issues-list li:before {{
            content: "⚠️";
            position: absolute;
            left: 0;
        }}
        
        .recommendations {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            animation: slideUp 0.8s ease-out 0.2s both;
        }}
        
        .recommendations h2 {{
            color: #2b59ff;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .ai-content {{
            line-height: 1.6;
            color: #444;
            white-space: pre-wrap;
        }}
        
        .footer {{
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 30px;
            font-size: 0.9em;
        }}
        
        @keyframes slideDown {{
            from {{
                opacity: 0;
                transform: translateY(-50px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(50px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes rotateIn {{
            from {{
                opacity: 0;
                transform: rotate(-180deg) scale(0.5);
            }}
            to {{
                opacity: 1;
                transform: rotate(0deg) scale(1);
            }}
        }}
        
        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #2b59ff, #1a4bff);
            border-radius: 4px;
            animation: progressFill 1.5s ease-out;
        }}
        
        @keyframes progressFill {{
            from {{ width: 0%; }}
            to {{ width: var(--progress-width); }}
        }}
        
        .status-good {{ color: #4caf50; }}
        .status-warning {{ color: #ff9800; }}
        .status-error {{ color: #f44336; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 SEO Analysis Report</h1>
            <div class="url">{data.get('url', '')}</div>
            <div class="score-circle">
                <div class="score-inner">
                    <div class="score-number">{score_percentage:.0f}</div>
                    <div class="score-text">SEO Score</div>
                </div>
            </div>
            <div style="text-align: center; color: #666; margin-top: 10px;">
                Generated on {timestamp}
            </div>
        </div>
        
        <div class="report-grid">
            <div class="report-card">
                <div class="card-header">
                    <div class="card-icon">🔧</div>
                    <div class="card-title">Technical SEO</div>
                </div>
                <div class="metric">
                    <span class="metric-label">Title Length</span>
                    <span class="metric-value">{technical_analysis['details'].get('title_length', 0)} chars</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Meta Description Length</span>
                    <span class="metric-value">{technical_analysis['details'].get('meta_description_length', 0)} chars</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Response Time</span>
                    <span class="metric-value">{technical_analysis['details'].get('response_time', 0):.2f}s</span>
                </div>
                <div class="metric">
                    <span class="metric-label">H1 Tags</span>
                    <span class="metric-value">{technical_analysis['details'].get('h1_count', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Images without Alt</span>
                    <span class="metric-value">{technical_analysis['details'].get('images_without_alt', 0)}</span>
                </div>
            </div>
            
            <div class="report-card">
                <div class="card-header">
                    <div class="card-icon">📝</div>
                    <div class="card-title">Content Analysis</div>
                </div>
                <div class="metric">
                    <span class="metric-label">Word Count</span>
                    <span class="metric-value">{content_analysis['details'].get('word_count', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Internal Links</span>
                    <span class="metric-value">{content_analysis['details'].get('internal_links', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">External Links</span>
                    <span class="metric-value">{content_analysis['details'].get('external_links', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Structured Data</span>
                    <span class="metric-value">{content_analysis['details'].get('structured_data_count', 0)}</span>
                </div>
            </div>
            
            <div class="report-card">
                <div class="card-header">
                    <div class="card-icon">⚠️</div>
                    <div class="card-title">Issues Found</div>
                </div>
                <ul class="issues-list">
                    {"".join([f"<li>{issue}</li>" for issue in technical_analysis.get('issues', []) + content_analysis.get('issues', [])])}
                </ul>
                {f'<p style="color: #4caf50; margin-top: 15px;">✅ No critical issues found!</p>' if not (technical_analysis.get('issues', []) + content_analysis.get('issues', [])) else ''}
            </div>
        </div>
        
        <div class="recommendations">
            <h2>🤖 AI-Powered Recommendations</h2>
            <div class="ai-content">{ai_recommendations}</div>
        </div>
        
        <div class="footer">
            <p>Report generated by SEO Analysis Tool • Powered by OpenAI</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html_template

    def run_analysis(self, url: str):
        """Run complete SEO analysis"""
        print(f"\n🚀 Starting comprehensive SEO analysis for: {url}")
        print("=" * 60)
        
        # Fetch website data
        data = self.fetch_website_data(url)
        if not data:
            return
        
        print("✅ Website data fetched successfully")
        
        # Run technical SEO analysis
        print("🔧 Analyzing technical SEO...")
        technical_analysis = self.analyze_technical_seo(data)
        
        # Run content SEO analysis
        print("📝 Analyzing content SEO...")
        content_analysis = self.analyze_content_seo(data)
        
        # Get AI recommendations
        ai_recommendations = self.get_openai_recommendations(data, technical_analysis, content_analysis)
        
        # Generate HTML report
        print("📊 Generating HTML report...")
        html_report = self.generate_html_report(data, technical_analysis, content_analysis, ai_recommendations)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = urlparse(url).netloc.replace('www.', '')
        filename = f"seo_report_{domain}_{timestamp}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"✅ Report saved as: {filename}")
        print(f"🌐 Open the file in your browser to view the detailed analysis")
        print("=" * 60)

def main():
    """Main function"""
    print("🔍 SEO Analysis Tool")
    print("=" * 40)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found!")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Get URL from user
    url = input("🌐 Enter the website URL to analyze: ").strip()
    
    if not url:
        print("❌ Error: No URL provided")
        sys.exit(1)
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # Initialize analyzer and run analysis
    analyzer = SEOAnalyzer()
    analyzer.run_analysis(url)

if __name__ == "__main__":
    main()