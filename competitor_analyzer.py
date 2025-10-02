#!/usr/bin/env python3
"""
Competitor Analysis Module for Advanced SEO Tool
Analyzes competitor websites and provides comparative insights
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time
from typing import Dict, List, Any
import concurrent.futures
from threading import Lock
import openai
from dotenv import load_dotenv
import os

load_dotenv()

class CompetitorAnalyzer:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            self.client = openai.OpenAI(api_key=self.openai_api_key)
        else:
            self.client = None
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.results_lock = Lock()

    def analyze_competitor(self, url: str) -> Dict[str, Any]:
        """Analyze a single competitor website"""
        try:
            print(f"🔍 Analyzing competitor: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic competitor data
            competitor_data = {
                'url': url,
                'domain': urlparse(url).netloc,
                'title': soup.find('title').get_text().strip() if soup.find('title') else '',
                'meta_description': '',
                'h1_tags': [h1.get_text().strip() for h1 in soup.find_all('h1')],
                'h2_tags': [h2.get_text().strip() for h2 in soup.find_all('h2')],
                'word_count': len(soup.get_text().split()),
                'images': len(soup.find_all('img')),
                'internal_links': 0,
                'external_links': 0,
                'response_time': response.elapsed.total_seconds(),
                'page_size': len(response.content),
                'https': url.startswith('https'),
                'structured_data': [],
                'social_links': [],
                'keywords': [],
                'content_topics': []
            }
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                competitor_data['meta_description'] = meta_desc.get('content', '')
            
            # Analyze links
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http'):
                    if urlparse(href).netloc == competitor_data['domain']:
                        competitor_data['internal_links'] += 1
                    else:
                        competitor_data['external_links'] += 1
                elif href.startswith('/'):
                    competitor_data['internal_links'] += 1
            
            # Extract structured data
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    structured = json.loads(script.string)
                    competitor_data['structured_data'].append(structured)
                except:
                    pass
            
            # Detect social media links
            social_platforms = ['facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 'tiktok']
            for link in soup.find_all('a', href=True):
                href = link['href'].lower()
                for platform in social_platforms:
                    if platform in href:
                        competitor_data['social_links'].append({
                            'platform': platform,
                            'url': href
                        })
                        break
            
            # Extract potential keywords from content
            content_text = soup.get_text().lower()
            words = content_text.split()
            word_freq = {}
            for word in words:
                if len(word) > 3 and word.isalpha():
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top keywords
            competitor_data['keywords'] = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:20]
            
            return competitor_data
            
        except Exception as e:
            print(f"❌ Error analyzing competitor {url}: {str(e)}")
            return None

    def compare_competitors(self, main_url: str, competitor_urls: List[str]) -> Dict[str, Any]:
        """Compare main website with competitors"""
        print(f"\n🏆 Starting competitor analysis...")
        print(f"📊 Main website: {main_url}")
        print(f"🎯 Competitors: {', '.join(competitor_urls)}")
        
        all_urls = [main_url] + competitor_urls
        results = {}
        
        # Analyze all websites in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.analyze_competitor, url): url for url in all_urls}
            
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result:
                        results[url] = result
                except Exception as e:
                    print(f"❌ Error processing {url}: {str(e)}")
        
        if not results:
            return {'error': 'No competitor data could be retrieved'}
        
        # Generate comparison analysis
        comparison = {
            'main_site': results.get(main_url, {}),
            'competitors': {url: data for url, data in results.items() if url != main_url},
            'analysis': self._generate_comparison_analysis(results, main_url),
            'recommendations': []
        }
        
        # Get AI-powered competitor insights
        if self.client:
            comparison['ai_insights'] = self._get_ai_competitor_insights(comparison)
        
        return comparison

    def _generate_comparison_analysis(self, results: Dict[str, Any], main_url: str) -> Dict[str, Any]:
        """Generate detailed comparison analysis"""
        main_site = results.get(main_url, {})
        competitors = {url: data for url, data in results.items() if url != main_url}
        
        if not main_site or not competitors:
            return {}
        
        analysis = {
            'metrics_comparison': {},
            'content_gaps': [],
            'technical_gaps': [],
            'opportunities': [],
            'strengths': [],
            'weaknesses': []
        }
        
        # Compare key metrics
        metrics = ['word_count', 'images', 'internal_links', 'external_links', 'response_time', 'page_size']
        
        for metric in metrics:
            main_value = main_site.get(metric, 0)
            competitor_values = [comp.get(metric, 0) for comp in competitors.values()]
            
            if competitor_values:
                avg_competitor = sum(competitor_values) / len(competitor_values)
                max_competitor = max(competitor_values)
                min_competitor = min(competitor_values)
                
                analysis['metrics_comparison'][metric] = {
                    'main_site': main_value,
                    'competitor_avg': avg_competitor,
                    'competitor_max': max_competitor,
                    'competitor_min': min_competitor,
                    'performance': 'above' if main_value > avg_competitor else 'below' if main_value < avg_competitor else 'equal'
                }
        
        # Identify content gaps
        main_keywords = set([kw[0] for kw in main_site.get('keywords', [])])
        competitor_keywords = set()
        for comp in competitors.values():
            competitor_keywords.update([kw[0] for kw in comp.get('keywords', [])])
        
        missing_keywords = competitor_keywords - main_keywords
        analysis['content_gaps'] = list(missing_keywords)[:20]  # Top 20 missing keywords
        
        # Technical analysis
        main_https = main_site.get('https', False)
        main_structured_data = len(main_site.get('structured_data', []))
        
        competitor_https = [comp.get('https', False) for comp in competitors.values()]
        competitor_structured = [len(comp.get('structured_data', [])) for comp in competitors.values()]
        
        if not main_https and any(competitor_https):
            analysis['technical_gaps'].append('HTTPS not implemented while competitors use it')
        
        if main_structured_data == 0 and any(s > 0 for s in competitor_structured):
            analysis['technical_gaps'].append('Missing structured data while competitors implement it')
        
        # Identify opportunities and strengths
        for metric, data in analysis['metrics_comparison'].items():
            if data['performance'] == 'above':
                analysis['strengths'].append(f"Superior {metric.replace('_', ' ')}")
            elif data['performance'] == 'below':
                analysis['weaknesses'].append(f"Inferior {metric.replace('_', ' ')}")
        
        return analysis

    def _get_ai_competitor_insights(self, comparison: Dict[str, Any]) -> str:
        """Get AI-powered competitor insights"""
        try:
            main_site = comparison.get('main_site', {})
            competitors = comparison.get('competitors', {})
            analysis = comparison.get('analysis', {})
            
            prompt = f"""
            Analyze this competitor comparison data and provide strategic SEO insights:

            MAIN WEBSITE:
            - Domain: {main_site.get('domain', '')}
            - Title: {main_site.get('title', '')}
            - Word Count: {main_site.get('word_count', 0)}
            - Internal Links: {main_site.get('internal_links', 0)}
            - Response Time: {main_site.get('response_time', 0):.2f}s

            COMPETITORS ANALYZED: {len(competitors)}

            PERFORMANCE COMPARISON:
            {json.dumps(analysis.get('metrics_comparison', {}), indent=2)}

            IDENTIFIED GAPS:
            - Content Gaps: {', '.join(analysis.get('content_gaps', [])[:10])}
            - Technical Gaps: {', '.join(analysis.get('technical_gaps', []))}

            STRENGTHS: {', '.join(analysis.get('strengths', []))}
            WEAKNESSES: {', '.join(analysis.get('weaknesses', []))}

            Please provide:
            1. Strategic competitive positioning recommendations
            2. Content strategy to close gaps and gain advantages
            3. Technical improvements based on competitor analysis
            4. Unique opportunities to differentiate from competitors
            5. Priority actions for competitive advantage
            6. Long-term competitive SEO strategy

            Focus on actionable insights that can improve search rankings and market position.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a competitive SEO strategist with expertise in market analysis and competitive positioning."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI insights unavailable: {str(e)}"

    def generate_competitor_report_html(self, comparison: Dict[str, Any]) -> str:
        """Generate HTML report for competitor analysis"""
        main_site = comparison.get('main_site', {})
        competitors = comparison.get('competitors', {})
        analysis = comparison.get('analysis', {})
        ai_insights = comparison.get('ai_insights', '')
        
        html = f"""
        <div class="competitor-analysis">
            <h2>🏆 Competitor Analysis Report</h2>
            
            <div class="comparison-grid">
                <div class="main-site-card">
                    <h3>Your Website</h3>
                    <div class="site-metrics">
                        <div class="metric">
                            <span class="label">Domain:</span>
                            <span class="value">{main_site.get('domain', '')}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Word Count:</span>
                            <span class="value">{main_site.get('word_count', 0):,}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Internal Links:</span>
                            <span class="value">{main_site.get('internal_links', 0)}</span>
                        </div>
                        <div class="metric">
                            <span class="label">Response Time:</span>
                            <span class="value">{main_site.get('response_time', 0):.2f}s</span>
                        </div>
                    </div>
                </div>
                
                <div class="competitors-grid">
                    {"".join([f'''
                    <div class="competitor-card">
                        <h4>{comp_data.get('domain', '')}</h4>
                        <div class="competitor-metrics">
                            <div class="metric">Words: {comp_data.get('word_count', 0):,}</div>
                            <div class="metric">Links: {comp_data.get('internal_links', 0)}</div>
                            <div class="metric">Speed: {comp_data.get('response_time', 0):.2f}s</div>
                        </div>
                    </div>
                    ''' for comp_data in competitors.values()])}
                </div>
            </div>
            
            <div class="analysis-sections">
                <div class="gaps-section">
                    <h3>📊 Content Gaps</h3>
                    <div class="gaps-list">
                        {"".join([f'<span class="gap-keyword">{gap}</span>' for gap in analysis.get('content_gaps', [])[:15]])}
                    </div>
                </div>
                
                <div class="strengths-weaknesses">
                    <div class="strengths">
                        <h4>✅ Your Strengths</h4>
                        <ul>
                            {"".join([f'<li>{strength}</li>' for strength in analysis.get('strengths', [])])}
                        </ul>
                    </div>
                    
                    <div class="weaknesses">
                        <h4>⚠️ Areas for Improvement</h4>
                        <ul>
                            {"".join([f'<li>{weakness}</li>' for weakness in analysis.get('weaknesses', [])])}
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="ai-insights">
                <h3>🤖 AI Competitive Strategy</h3>
                <div class="insights-content">
                    {ai_insights.replace(chr(10), '<br>')}
                </div>
            </div>
        </div>
        
        <style>
        .competitor-analysis {{
            margin: 30px 0;
            padding: 30px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }}
        
        .comparison-grid {{
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 30px;
            margin: 20px 0;
        }}
        
        .main-site-card {{
            background: linear-gradient(135deg, #2b59ff, #1a4bff);
            color: white;
            padding: 25px;
            border-radius: 15px;
        }}
        
        .competitors-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        
        .competitor-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }}
        
        .metric {{
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
        }}
        
        .gaps-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }}
        
        .gap-keyword {{
            background: #fff3cd;
            color: #856404;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
        }}
        
        .strengths-weaknesses {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin: 20px 0;
        }}
        
        .strengths {{
            background: #d4edda;
            padding: 20px;
            border-radius: 10px;
        }}
        
        .weaknesses {{
            background: #f8d7da;
            padding: 20px;
            border-radius: 10px;
        }}
        
        .ai-insights {{
            background: #e3f2fd;
            padding: 25px;
            border-radius: 15px;
            margin: 20px 0;
        }}
        
        .insights-content {{
            line-height: 1.6;
            color: #333;
        }}
        </style>
        """
        
        return html