#!/usr/bin/env python3
"""
Bulk Analysis Module for Advanced SEO Tool
Analyzes multiple URLs, sitemaps, and generates comprehensive reports
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET
import json
import time
import csv
from typing import Dict, List, Any, Optional
import concurrent.futures
from threading import Lock
import openai
from dotenv import load_dotenv
import os
from datetime import datetime
import pandas as pd

load_dotenv()

class BulkAnalyzer:
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
        self.results = []

    def discover_sitemap(self, domain: str) -> List[str]:
        """Discover sitemap URLs for a domain"""
        sitemap_urls = []
        
        # Common sitemap locations
        common_paths = [
            '/sitemap.xml',
            '/sitemap_index.xml',
            '/sitemaps.xml',
            '/sitemap1.xml',
            '/wp-sitemap.xml',
            '/post-sitemap.xml',
            '/page-sitemap.xml'
        ]
        
        base_url = f"https://{domain}" if not domain.startswith('http') else domain
        
        for path in common_paths:
            try:
                url = urljoin(base_url, path)
                response = self.session.get(url, timeout=10)
                if response.status_code == 200 and 'xml' in response.headers.get('content-type', ''):
                    sitemap_urls.append(url)
                    print(f"✅ Found sitemap: {url}")
            except:
                continue
        
        # Check robots.txt for sitemap references
        try:
            robots_url = urljoin(base_url, '/robots.txt')
            response = self.session.get(robots_url, timeout=10)
            if response.status_code == 200:
                for line in response.text.split('\n'):
                    if line.lower().startswith('sitemap:'):
                        sitemap_url = line.split(':', 1)[1].strip()
                        if sitemap_url not in sitemap_urls:
                            sitemap_urls.append(sitemap_url)
                            print(f"✅ Found sitemap in robots.txt: {sitemap_url}")
        except:
            pass
        
        return sitemap_urls

    def parse_sitemap(self, sitemap_url: str) -> List[str]:
        """Parse sitemap XML and extract URLs"""
        urls = []
        
        try:
            print(f"📄 Parsing sitemap: {sitemap_url}")
            response = self.session.get(sitemap_url, timeout=15)
            response.raise_for_status()
            
            # Parse XML
            root = ET.fromstring(response.content)
            
            # Handle different sitemap formats
            namespaces = {
                'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9',
                'news': 'http://www.google.com/schemas/sitemap-news/0.9',
                'image': 'http://www.google.com/schemas/sitemap-image/1.1'
            }
            
            # Check if it's a sitemap index
            sitemaps = root.findall('.//sitemap:sitemap', namespaces)
            if sitemaps:
                print(f"📋 Found sitemap index with {len(sitemaps)} sitemaps")
                for sitemap in sitemaps:
                    loc = sitemap.find('sitemap:loc', namespaces)
                    if loc is not None:
                        # Recursively parse sub-sitemaps
                        sub_urls = self.parse_sitemap(loc.text)
                        urls.extend(sub_urls)
            else:
                # Regular sitemap with URLs
                url_elements = root.findall('.//sitemap:url', namespaces)
                for url_elem in url_elements:
                    loc = url_elem.find('sitemap:loc', namespaces)
                    if loc is not None:
                        urls.append(loc.text)
                
                print(f"📊 Extracted {len(urls)} URLs from sitemap")
        
        except Exception as e:
            print(f"❌ Error parsing sitemap {sitemap_url}: {str(e)}")
        
        return urls

    def analyze_single_url(self, url: str) -> Dict[str, Any]:
        """Analyze a single URL for bulk analysis"""
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                return {
                    'url': url,
                    'status': 'error',
                    'status_code': response.status_code,
                    'error': f'HTTP {response.status_code}'
                }
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic SEO data
            analysis = {
                'url': url,
                'status': 'success',
                'status_code': response.status_code,
                'response_time': response_time,
                'page_size': len(response.content),
                
                # SEO Elements
                'title': soup.find('title').get_text().strip() if soup.find('title') else '',
                'title_length': 0,
                'meta_description': '',
                'meta_description_length': 0,
                'h1_count': len(soup.find_all('h1')),
                'h2_count': len(soup.find_all('h2')),
                'h3_count': len(soup.find_all('h3')),
                
                # Content Analysis
                'word_count': len(soup.get_text().split()),
                'image_count': len(soup.find_all('img')),
                'images_without_alt': 0,
                'internal_links': 0,
                'external_links': 0,
                
                # Technical
                'canonical_url': '',
                'robots_meta': '',
                'structured_data_count': 0,
                'https': url.startswith('https'),
                
                # Issues
                'issues': [],
                'warnings': [],
                'score': 0
            }
            
            # Calculate title length
            if analysis['title']:
                analysis['title_length'] = len(analysis['title'])
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                analysis['meta_description'] = meta_desc.get('content', '')
                analysis['meta_description_length'] = len(analysis['meta_description'])
            
            # Extract canonical URL
            canonical = soup.find('link', rel='canonical')
            if canonical:
                analysis['canonical_url'] = canonical.get('href', '')
            
            # Extract robots meta
            robots_meta = soup.find('meta', attrs={'name': 'robots'})
            if robots_meta:
                analysis['robots_meta'] = robots_meta.get('content', '')
            
            # Count images without alt text
            images = soup.find_all('img')
            analysis['images_without_alt'] = len([img for img in images if not img.get('alt')])
            
            # Count links
            domain = urlparse(url).netloc
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http'):
                    if urlparse(href).netloc == domain:
                        analysis['internal_links'] += 1
                    else:
                        analysis['external_links'] += 1
                elif href.startswith('/'):
                    analysis['internal_links'] += 1
            
            # Count structured data
            structured_data = soup.find_all('script', type='application/ld+json')
            analysis['structured_data_count'] = len(structured_data)
            
            # Basic SEO scoring and issue detection
            score = 0
            
            # Title analysis
            if not analysis['title']:
                analysis['issues'].append('Missing title tag')
            elif analysis['title_length'] < 30:
                analysis['warnings'].append('Title too short')
            elif analysis['title_length'] > 60:
                analysis['warnings'].append('Title too long')
            else:
                score += 20
            
            # Meta description analysis
            if not analysis['meta_description']:
                analysis['issues'].append('Missing meta description')
            elif analysis['meta_description_length'] < 120:
                analysis['warnings'].append('Meta description too short')
            elif analysis['meta_description_length'] > 160:
                analysis['warnings'].append('Meta description too long')
            else:
                score += 20
            
            # H1 analysis
            if analysis['h1_count'] == 0:
                analysis['issues'].append('Missing H1 tag')
            elif analysis['h1_count'] > 1:
                analysis['warnings'].append('Multiple H1 tags')
            else:
                score += 15
            
            # Image analysis
            if analysis['images_without_alt'] > 0:
                analysis['warnings'].append(f'{analysis["images_without_alt"]} images without alt text')
            else:
                score += 15
            
            # Content analysis
            if analysis['word_count'] < 300:
                analysis['warnings'].append('Low word count')
            else:
                score += 15
            
            # Technical analysis
            if not analysis['canonical_url']:
                analysis['warnings'].append('Missing canonical URL')
            else:
                score += 10
            
            if not analysis['https']:
                analysis['issues'].append('Not using HTTPS')
            else:
                score += 5
            
            analysis['score'] = score
            
            return analysis
            
        except Exception as e:
            return {
                'url': url,
                'status': 'error',
                'error': str(e),
                'status_code': 0
            }

    def bulk_analyze_urls(self, urls: List[str], max_workers: int = 10) -> List[Dict[str, Any]]:
        """Analyze multiple URLs in parallel"""
        print(f"\n🚀 Starting bulk analysis of {len(urls)} URLs...")
        print(f"⚡ Using {max_workers} parallel workers")
        
        results = []
        completed = 0
        
        def update_progress(future):
            nonlocal completed
            completed += 1
            if completed % 10 == 0 or completed == len(urls):
                print(f"📊 Progress: {completed}/{len(urls)} URLs analyzed ({completed/len(urls)*100:.1f}%)")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_url = {executor.submit(self.analyze_single_url, url): url for url in urls}
            
            # Add progress callback
            for future in future_to_url:
                future.add_done_callback(update_progress)
            
            # Collect results
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    url = future_to_url[future]
                    results.append({
                        'url': url,
                        'status': 'error',
                        'error': str(e)
                    })
        
        print(f"✅ Bulk analysis completed!")
        return results

    def analyze_website_sitemap(self, domain: str, max_urls: int = 100) -> Dict[str, Any]:
        """Analyze a website's sitemap"""
        print(f"\n🗺️ Starting sitemap analysis for: {domain}")
        
        # Discover sitemaps
        sitemap_urls = self.discover_sitemap(domain)
        
        if not sitemap_urls:
            return {
                'error': 'No sitemaps found',
                'domain': domain,
                'sitemaps_found': 0
            }
        
        # Extract URLs from sitemaps
        all_urls = []
        for sitemap_url in sitemap_urls:
            urls = self.parse_sitemap(sitemap_url)
            all_urls.extend(urls)
        
        # Remove duplicates and limit
        unique_urls = list(set(all_urls))[:max_urls]
        
        print(f"📊 Found {len(all_urls)} total URLs, analyzing {len(unique_urls)} unique URLs")
        
        # Analyze URLs
        results = self.bulk_analyze_urls(unique_urls)
        
        # Generate summary
        summary = self._generate_bulk_summary(results)
        
        return {
            'domain': domain,
            'sitemaps_found': len(sitemap_urls),
            'sitemap_urls': sitemap_urls,
            'total_urls_found': len(all_urls),
            'urls_analyzed': len(unique_urls),
            'results': results,
            'summary': summary,
            'analysis_timestamp': datetime.now().isoformat()
        }

    def _generate_bulk_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics from bulk analysis results"""
        if not results:
            return {}
        
        successful_results = [r for r in results if r.get('status') == 'success']
        
        if not successful_results:
            return {'error': 'No successful analyses'}
        
        summary = {
            'total_pages': len(results),
            'successful_analyses': len(successful_results),
            'failed_analyses': len(results) - len(successful_results),
            'success_rate': len(successful_results) / len(results) * 100,
            
            # SEO Issues Summary
            'pages_missing_title': len([r for r in successful_results if not r.get('title')]),
            'pages_missing_meta_desc': len([r for r in successful_results if not r.get('meta_description')]),
            'pages_missing_h1': len([r for r in successful_results if r.get('h1_count', 0) == 0]),
            'pages_multiple_h1': len([r for r in successful_results if r.get('h1_count', 0) > 1]),
            'pages_without_https': len([r for r in successful_results if not r.get('https', True)]),
            
            # Performance Summary
            'avg_response_time': sum(r.get('response_time', 0) for r in successful_results) / len(successful_results),
            'avg_page_size': sum(r.get('page_size', 0) for r in successful_results) / len(successful_results),
            'avg_word_count': sum(r.get('word_count', 0) for r in successful_results) / len(successful_results),
            
            # Score Distribution
            'avg_seo_score': sum(r.get('score', 0) for r in successful_results) / len(successful_results),
            'high_score_pages': len([r for r in successful_results if r.get('score', 0) >= 80]),
            'medium_score_pages': len([r for r in successful_results if 50 <= r.get('score', 0) < 80]),
            'low_score_pages': len([r for r in successful_results if r.get('score', 0) < 50]),
            
            # Content Analysis
            'pages_low_content': len([r for r in successful_results if r.get('word_count', 0) < 300]),
            'pages_no_images': len([r for r in successful_results if r.get('image_count', 0) == 0]),
            'pages_images_no_alt': len([r for r in successful_results if r.get('images_without_alt', 0) > 0]),
        }
        
        return summary

    def export_results_csv(self, results: List[Dict[str, Any]], filename: str = None) -> str:
        """Export bulk analysis results to CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bulk_seo_analysis_{timestamp}.csv"
        
        # Prepare data for CSV
        csv_data = []
        for result in results:
            if result.get('status') == 'success':
                csv_row = {
                    'URL': result.get('url', ''),
                    'Status Code': result.get('status_code', ''),
                    'Response Time (s)': result.get('response_time', ''),
                    'Page Size (bytes)': result.get('page_size', ''),
                    'Title': result.get('title', ''),
                    'Title Length': result.get('title_length', ''),
                    'Meta Description': result.get('meta_description', ''),
                    'Meta Description Length': result.get('meta_description_length', ''),
                    'H1 Count': result.get('h1_count', ''),
                    'H2 Count': result.get('h2_count', ''),
                    'Word Count': result.get('word_count', ''),
                    'Image Count': result.get('image_count', ''),
                    'Images Without Alt': result.get('images_without_alt', ''),
                    'Internal Links': result.get('internal_links', ''),
                    'External Links': result.get('external_links', ''),
                    'HTTPS': result.get('https', ''),
                    'Canonical URL': result.get('canonical_url', ''),
                    'Structured Data Count': result.get('structured_data_count', ''),
                    'SEO Score': result.get('score', ''),
                    'Issues': '; '.join(result.get('issues', [])),
                    'Warnings': '; '.join(result.get('warnings', []))
                }
                csv_data.append(csv_row)
        
        # Write CSV
        if csv_data:
            df = pd.DataFrame(csv_data)
            df.to_csv(filename, index=False)
            print(f"📊 Results exported to: {filename}")
        
        return filename

    def generate_bulk_report_html(self, analysis_data: Dict[str, Any]) -> str:
        """Generate HTML report for bulk analysis"""
        domain = analysis_data.get('domain', '')
        summary = analysis_data.get('summary', {})
        results = analysis_data.get('results', [])
        
        # Calculate percentages
        total_pages = summary.get('total_pages', 1)
        
        html = f"""
        <div class="bulk-analysis-report">
            <h2>🗺️ Bulk SEO Analysis Report</h2>
            <h3>Domain: {domain}</h3>
            
            <div class="summary-grid">
                <div class="summary-card">
                    <h4>📊 Analysis Overview</h4>
                    <div class="metric">
                        <span class="label">Total Pages:</span>
                        <span class="value">{summary.get('total_pages', 0)}</span>
                    </div>
                    <div class="metric">
                        <span class="label">Success Rate:</span>
                        <span class="value">{summary.get('success_rate', 0):.1f}%</span>
                    </div>
                    <div class="metric">
                        <span class="label">Average SEO Score:</span>
                        <span class="value">{summary.get('avg_seo_score', 0):.1f}/100</span>
                    </div>
                </div>
                
                <div class="summary-card">
                    <h4>🚨 Critical Issues</h4>
                    <div class="metric">
                        <span class="label">Missing Titles:</span>
                        <span class="value error">{summary.get('pages_missing_title', 0)} ({summary.get('pages_missing_title', 0)/total_pages*100:.1f}%)</span>
                    </div>
                    <div class="metric">
                        <span class="label">Missing Meta Descriptions:</span>
                        <span class="value error">{summary.get('pages_missing_meta_desc', 0)} ({summary.get('pages_missing_meta_desc', 0)/total_pages*100:.1f}%)</span>
                    </div>
                    <div class="metric">
                        <span class="label">Missing H1 Tags:</span>
                        <span class="value error">{summary.get('pages_missing_h1', 0)} ({summary.get('pages_missing_h1', 0)/total_pages*100:.1f}%)</span>
                    </div>
                </div>
                
                <div class="summary-card">
                    <h4>⚡ Performance</h4>
                    <div class="metric">
                        <span class="label">Avg Response Time:</span>
                        <span class="value">{summary.get('avg_response_time', 0):.2f}s</span>
                    </div>
                    <div class="metric">
                        <span class="label">Avg Page Size:</span>
                        <span class="value">{summary.get('avg_page_size', 0)/1024:.1f} KB</span>
                    </div>
                    <div class="metric">
                        <span class="label">Avg Word Count:</span>
                        <span class="value">{summary.get('avg_word_count', 0):.0f}</span>
                    </div>
                </div>
                
                <div class="summary-card">
                    <h4>📈 Score Distribution</h4>
                    <div class="metric">
                        <span class="label">High Score (80+):</span>
                        <span class="value good">{summary.get('high_score_pages', 0)} ({summary.get('high_score_pages', 0)/total_pages*100:.1f}%)</span>
                    </div>
                    <div class="metric">
                        <span class="label">Medium Score (50-79):</span>
                        <span class="value warning">{summary.get('medium_score_pages', 0)} ({summary.get('medium_score_pages', 0)/total_pages*100:.1f}%)</span>
                    </div>
                    <div class="metric">
                        <span class="label">Low Score (<50):</span>
                        <span class="value error">{summary.get('low_score_pages', 0)} ({summary.get('low_score_pages', 0)/total_pages*100:.1f}%)</span>
                    </div>
                </div>
            </div>
            
            <div class="detailed-results">
                <h3>📋 Detailed Results</h3>
                <div class="results-table">
                    <table>
                        <thead>
                            <tr>
                                <th>URL</th>
                                <th>Score</th>
                                <th>Title Length</th>
                                <th>Meta Desc Length</th>
                                <th>Word Count</th>
                                <th>Response Time</th>
                                <th>Issues</th>
                            </tr>
                        </thead>
                        <tbody>
                            {"".join([f'''
                            <tr class="{'success' if result.get('status') == 'success' else 'error'}">
                                <td class="url-cell">
                                    <a href="{result.get('url', '')}" target="_blank">
                                        {result.get('url', '')[:50]}{'...' if len(result.get('url', '')) > 50 else ''}
                                    </a>
                                </td>
                                <td class="score-cell score-{self._get_score_class(result.get('score', 0))}">{result.get('score', 0)}</td>
                                <td class="{'good' if 30 <= result.get('title_length', 0) <= 60 else 'warning'}">{result.get('title_length', 0)}</td>
                                <td class="{'good' if 120 <= result.get('meta_description_length', 0) <= 160 else 'warning'}">{result.get('meta_description_length', 0)}</td>
                                <td class="{'good' if result.get('word_count', 0) >= 300 else 'warning'}">{result.get('word_count', 0)}</td>
                                <td class="{'good' if result.get('response_time', 0) < 2 else 'warning'}">{result.get('response_time', 0):.2f}s</td>
                                <td class="issues-cell">
                                    {len(result.get('issues', [])) + len(result.get('warnings', []))} issues
                                </td>
                            </tr>
                            ''' for result in results[:50]])}  <!-- Show first 50 results -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <style>
        .bulk-analysis-report {{
            margin: 30px 0;
            padding: 30px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }}
        
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .summary-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 15px;
            border: 2px solid #e9ecef;
        }}
        
        .summary-card h4 {{
            color: #2b59ff;
            margin-bottom: 15px;
        }}
        
        .metric {{
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 5px 0;
        }}
        
        .value.good {{ color: #28a745; font-weight: bold; }}
        .value.warning {{ color: #ffc107; font-weight: bold; }}
        .value.error {{ color: #dc3545; font-weight: bold; }}
        
        .results-table {{
            overflow-x: auto;
            margin: 20px 0;
        }}
        
        .results-table table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }}
        
        .results-table th {{
            background: #2b59ff;
            color: white;
            padding: 15px 10px;
            text-align: left;
        }}
        
        .results-table td {{
            padding: 12px 10px;
            border-bottom: 1px solid #eee;
        }}
        
        .results-table tr:hover {{
            background: #f8f9fa;
        }}
        
        .url-cell a {{
            color: #2b59ff;
            text-decoration: none;
        }}
        
        .score-cell {{
            font-weight: bold;
            text-align: center;
        }}
        
        .score-good {{ color: #28a745; }}
        .score-warning {{ color: #ffc107; }}
        .score-error {{ color: #dc3545; }}
        
        .good {{ color: #28a745; }}
        .warning {{ color: #ffc107; }}
        .error {{ color: #dc3545; }}
        </style>
        """
        
        return html

    def _get_score_class(self, score: int) -> str:
        """Get CSS class for score"""
        if score >= 80:
            return 'good'
        elif score >= 50:
            return 'warning'
        else:
            return 'error'