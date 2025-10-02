#!/usr/bin/env python3
"""
Ultimate SEO Analysis Tool - Enhanced Version
Comprehensive website analysis with competitor analysis, bulk analysis, and advanced features
"""

import os
import sys
import argparse
from datetime import datetime
from urllib.parse import urlparse
from typing import List

# Import our modules
from advanced_seo_analyzer import AdvancedSEOAnalyzer
from competitor_analyzer import CompetitorAnalyzer
from bulk_analyzer import BulkAnalyzer
from sitemap_generator import SitemapGenerator

class UltimateSEOAnalyzer:
    def __init__(self):
        self.advanced_analyzer = AdvancedSEOAnalyzer()
        self.competitor_analyzer = CompetitorAnalyzer()
        self.bulk_analyzer = BulkAnalyzer()
        self.sitemap_generator = SitemapGenerator()

    def run_single_analysis(self, url: str, include_competitors: bool = False, competitor_urls: List[str] = None):
        """Run comprehensive single URL analysis"""
        print(f"\n🚀 Starting Ultimate SEO Analysis for: {url}")
        print("=" * 80)
        
        # Run main analysis
        data = self.advanced_analyzer.fetch_comprehensive_website_data(url)
        if not data:
            return
        
        print("✅ Website data fetched successfully")
        
        # Run all analysis modules
        print("🔧 Running advanced technical analysis...")
        technical_analysis = self.advanced_analyzer.analyze_technical_seo_advanced(data)
        
        print("📝 Running advanced content analysis...")
        content_analysis = self.advanced_analyzer.analyze_content_advanced(data)
        
        print("⚡ Running performance analysis...")
        performance_analysis = self.advanced_analyzer.analyze_performance_metrics(data)
        
        print("🌐 Running domain analysis...")
        domain_analysis = self.advanced_analyzer.analyze_domain_authority(data['domain'])
        
        # Competitor analysis if requested
        competitor_data = None
        if include_competitors and competitor_urls:
            print("🏆 Running competitor analysis...")
            competitor_data = self.competitor_analyzer.compare_competitors(url, competitor_urls)
        
        # Get comprehensive AI recommendations
        ai_recommendations = self.advanced_analyzer.get_comprehensive_ai_recommendations(
            data, technical_analysis, content_analysis, performance_analysis
        )
        
        # Generate ultimate HTML report
        print("📊 Generating ultimate HTML report...")
        html_report = self.generate_ultimate_report(
            data, technical_analysis, content_analysis, performance_analysis, 
            domain_analysis, ai_recommendations, competitor_data
        )
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = urlparse(url).netloc.replace('www.', '')
        filename = f"ultimate_seo_report_{domain}_{timestamp}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        self._print_analysis_summary(technical_analysis, content_analysis, performance_analysis)
        print(f"\n✅ Ultimate report saved as: {filename}")
        print("🌐 Open the file in your browser to view the comprehensive analysis")

    def run_bulk_analysis(self, domain: str, max_urls: int = 100):
        """Run bulk sitemap analysis"""
        print(f"\n🗺️ Starting bulk sitemap analysis for: {domain}")
        print("=" * 80)
        
        # Run bulk analysis
        bulk_data = self.bulk_analyzer.analyze_website_sitemap(domain, max_urls)
        
        if bulk_data.get('error'):
            print(f"❌ Error: {bulk_data['error']}")
            return
        
        # Export CSV
        csv_filename = self.bulk_analyzer.export_results_csv(bulk_data['results'])
        
        # Generate HTML report for bulk analysis
        bulk_html = self.bulk_analyzer.generate_bulk_report_html(bulk_data)
        
        # Save bulk report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_filename = f"bulk_seo_report_{domain}_{timestamp}.html"
        
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(self._wrap_bulk_html(bulk_html, domain))
        
        # Print summary
        summary = bulk_data['summary']
        print(f"\n📊 BULK ANALYSIS SUMMARY")
        print("=" * 50)
        print(f"🎯 Domain: {domain}")
        print(f"📄 Pages Analyzed: {summary.get('total_pages', 0)}")
        print(f"✅ Success Rate: {summary.get('success_rate', 0):.1f}%")
        print(f"📊 Average SEO Score: {summary.get('avg_seo_score', 0):.1f}/100")
        print(f"🚨 Critical Issues: {summary.get('pages_missing_title', 0)} missing titles, {summary.get('pages_missing_meta_desc', 0)} missing meta descriptions")
        print(f"⚡ Performance: {summary.get('avg_response_time', 0):.2f}s avg response time")
        
        print(f"\n✅ Bulk analysis reports saved:")
        print(f"📊 HTML Report: {html_filename}")
        print(f"📋 CSV Export: {csv_filename}")

    def run_comprehensive_crawl_and_sitemap(self, url: str, max_pages: int = 500, max_depth: int = 5):
        """Run comprehensive website crawling and generate sitemap"""
        print(f"\n🕷️ Starting comprehensive website crawling and sitemap generation for: {url}")
        print("=" * 80)
        
        # Configure sitemap generator
        self.sitemap_generator.max_pages = max_pages
        self.sitemap_generator.max_depth = max_depth
        
        # Discover website structure
        discovery_data = self.sitemap_generator.discover_website_structure(url)
        
        if not discovery_data.get('pages'):
            print("❌ No pages discovered. Cannot generate sitemap.")
            return
        
        # Generate sitemap XML
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = urlparse(url).netloc.replace('www.', '').replace('.', '_')
        sitemap_filename = f"sitemap_{domain}_{timestamp}.xml"
        
        sitemap_path = self.sitemap_generator.generate_sitemap_xml(discovery_data, sitemap_filename)
        
        # Generate sitemap report
        report_path = self.sitemap_generator.generate_sitemap_report(discovery_data, sitemap_path)
        
        # Run SEO analysis on discovered pages (sample)
        print(f"\n📊 Running SEO analysis on discovered pages...")
        sample_pages = list(discovery_data['pages'].keys())[:10]  # Analyze first 10 pages
        
        seo_results = []
        for page_url in sample_pages:
            try:
                print(f"   🔍 Analyzing: {page_url}")
                page_data = self.advanced_analyzer.fetch_comprehensive_website_data(page_url)
                if page_data:
                    technical_analysis = self.advanced_analyzer.analyze_technical_seo_advanced(page_data)
                    content_analysis = self.advanced_analyzer.analyze_content_advanced(page_data)
                    
                    seo_results.append({
                        'url': page_url,
                        'technical_score': (technical_analysis['score'] / technical_analysis['max_score']) * 100,
                        'content_score': (content_analysis['score'] / content_analysis['max_score']) * 100,
                        'issues': len(technical_analysis.get('issues', []) + content_analysis.get('issues', [])),
                        'warnings': len(technical_analysis.get('warnings', []) + content_analysis.get('warnings', []))
                    })
            except Exception as e:
                print(f"   ❌ Error analyzing {page_url}: {str(e)}")
        
        # Generate comprehensive report
        comprehensive_report = self._generate_comprehensive_crawl_report(
            discovery_data, sitemap_path, seo_results, url
        )
        
        comprehensive_filename = f"comprehensive_crawl_report_{domain}_{timestamp}.html"
        with open(comprehensive_filename, 'w', encoding='utf-8') as f:
            f.write(comprehensive_report)
        
        # Print final summary
        print(f"\n🎉 COMPREHENSIVE CRAWLING COMPLETE")
        print("=" * 60)
        print(f"🕷️ Total Pages Discovered: {discovery_data['total_discovered']}")
        print(f"✅ Successfully Crawled: {discovery_data['total_crawled']}")
        print(f"📏 Maximum Depth: {discovery_data['max_depth_reached']}")
        print(f"📊 SEO Analysis: {len(seo_results)} pages analyzed")
        
        print(f"\n📄 Generated Files:")
        print(f"🗺️ Sitemap XML: {sitemap_path}")
        print(f"📊 Sitemap Report: {report_path}")
        print(f"📋 Comprehensive Report: {comprehensive_filename}")
        
        return {
            'sitemap_path': sitemap_path,
            'report_path': report_path,
            'comprehensive_report': comprehensive_filename,
            'discovery_data': discovery_data,
            'seo_results': seo_results
        }

    def run_competitor_analysis(self, main_url: str, competitor_urls: List[str]):
        """Run standalone competitor analysis"""
        print(f"\n🏆 Starting competitor analysis...")
        print("=" * 80)
        
        competitor_data = self.competitor_analyzer.compare_competitors(main_url, competitor_urls)
        
        if competitor_data.get('error'):
            print(f"❌ Error: {competitor_data['error']}")
            return
        
        # Generate competitor report
        competitor_html = self.competitor_analyzer.generate_competitor_report_html(competitor_data)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = urlparse(main_url).netloc.replace('www.', '')
        filename = f"competitor_analysis_{domain}_{timestamp}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self._wrap_competitor_html(competitor_html, main_url))
        
        print(f"✅ Competitor analysis saved as: {filename}")

    def generate_ultimate_report(self, data, technical_analysis, content_analysis, 
                                performance_analysis, domain_analysis, ai_recommendations, 
                                competitor_data=None):
        """Generate the ultimate comprehensive HTML report"""
        
        # Get base report from advanced analyzer
        base_html = self.advanced_analyzer.generate_advanced_html_report(
            data, technical_analysis, content_analysis, performance_analysis, 
            domain_analysis, ai_recommendations
        )
        
        # Add competitor analysis if available
        competitor_section = ""
        if competitor_data and not competitor_data.get('error'):
            competitor_section = self.competitor_analyzer.generate_competitor_report_html(competitor_data)
        
        # Insert competitor section before recommendations
        if competitor_section:
            recommendations_pos = base_html.find('<div class="recommendations">')
            if recommendations_pos != -1:
                base_html = (base_html[:recommendations_pos] + 
                           competitor_section + 
                           base_html[recommendations_pos:])
        
        # Add ultimate branding
        base_html = base_html.replace(
            "🔍 Advanced SEO Analysis Report",
            "🚀 Ultimate SEO Analysis Report"
        ).replace(
            "Advanced SEO Analysis Report • Powered by OpenAI GPT-4",
            "Ultimate SEO Analysis Tool • Advanced AI-Powered Analysis • Competitor Intelligence"
        )
        
        return base_html

    def _generate_comprehensive_crawl_report(self, discovery_data: Dict, sitemap_path: str, seo_results: List, url: str) -> str:
        """Generate comprehensive crawl and sitemap report"""
        pages = discovery_data.get('pages', {})
        
        # Calculate statistics
        avg_technical_score = sum(r['technical_score'] for r in seo_results) / len(seo_results) if seo_results else 0
        avg_content_score = sum(r['content_score'] for r in seo_results) / len(seo_results) if seo_results else 0
        total_issues = sum(r['issues'] for r in seo_results)
        total_warnings = sum(r['warnings'] for r in seo_results)
        
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Comprehensive Crawl & Sitemap Report - {urlparse(url).netloc}</title>
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
            max-width: 1400px;
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
        .header h1 {{
            color: #2b59ff;
            font-size: 3em;
            margin-bottom: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2b59ff;
            margin-bottom: 10px;
        }}
        .stat-label {{
            color: #666;
            font-size: 1.1em;
        }}
        .section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }}
        .section h2 {{
            color: #2b59ff;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }}
        .section-icon {{
            margin-right: 15px;
            font-size: 1.5em;
        }}
        .sitemap-info {{
            background: #e8f5e8;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #4caf50;
        }}
        .seo-results {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .seo-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #e9ecef;
        }}
        .seo-card h4 {{
            color: #2b59ff;
            margin-bottom: 15px;
            font-size: 0.9em;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .score-bar {{
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .score-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 1s ease-out;
        }}
        .score-excellent {{ background: linear-gradient(90deg, #4caf50, #8bc34a); }}
        .score-good {{ background: linear-gradient(90deg, #8bc34a, #cddc39); }}
        .score-average {{ background: linear-gradient(90deg, #ff9800, #ffc107); }}
        .score-poor {{ background: linear-gradient(90deg, #f44336, #e91e63); }}
        .metric {{
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            font-size: 0.9em;
        }}
        .pages-table {{
            overflow-x: auto;
            margin: 20px 0;
        }}
        .pages-table table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
        }}
        .pages-table th {{
            background: #2b59ff;
            color: white;
            padding: 15px 10px;
            text-align: left;
        }}
        .pages-table td {{
            padding: 12px 10px;
            border-bottom: 1px solid #eee;
        }}
        .pages-table tr:hover {{
            background: #f8f9fa;
        }}
        .url-cell {{
            max-width: 250px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .url-cell a {{
            color: #2b59ff;
            text-decoration: none;
        }}
        .depth-0 {{ background: #e8f5e8; }}
        .depth-1 {{ background: #fff3cd; }}
        .depth-2 {{ background: #cce5ff; }}
        .depth-3 {{ background: #f8d7da; }}
        .good {{ color: #28a745; font-weight: bold; }}
        .warning {{ color: #ffc107; font-weight: bold; }}
        .error {{ color: #dc3545; font-weight: bold; }}
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
            <h1>🕷️ Comprehensive Crawl & Sitemap Report</h1>
            <p>Complete website discovery, analysis, and sitemap generation</p>
            <p><strong>Website:</strong> {url}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{discovery_data['total_discovered']}</div>
                <div class="stat-label">Pages Discovered</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{discovery_data['total_crawled']}</div>
                <div class="stat-label">Successfully Crawled</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{discovery_data['max_depth_reached']}</div>
                <div class="stat-label">Max Depth Reached</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(seo_results)}</div>
                <div class="stat-label">SEO Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{avg_technical_score:.0f}</div>
                <div class="stat-label">Avg Technical Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{avg_content_score:.0f}</div>
                <div class="stat-label">Avg Content Score</div>
            </div>
        </div>
        
        <div class="section">
            <h2><span class="section-icon">🗺️</span>Generated Sitemap</h2>
            <div class="sitemap-info">
                <h3>📄 Sitemap XML Generated Successfully</h3>
                <p><strong>File:</strong> {sitemap_path}</p>
                <p><strong>URLs Included:</strong> {len([p for p in pages.values() if p.get('status_code') == 200])}</p>
                <p><strong>Format:</strong> XML Sitemap Protocol 0.9 with priority, changefreq, and lastmod</p>
                <p><strong>Features:</strong> Automatic priority assignment based on page depth and content quality</p>
                <p><strong>Usage:</strong> Upload this sitemap to your website root and submit to Google Search Console</p>
            </div>
        </div>
        
        <div class="section">
            <h2><span class="section-icon">📊</span>SEO Analysis Results</h2>
            <p>Detailed SEO analysis performed on {len(seo_results)} sample pages:</p>
            
            <div class="seo-results">
                {"".join([f'''
                <div class="seo-card">
                    <h4 title="{result['url']}">{result['url'][:40]}{'...' if len(result['url']) > 40 else ''}</h4>
                    
                    <div class="metric">
                        <span>Technical SEO:</span>
                        <span class="{'good' if result['technical_score'] >= 70 else 'warning' if result['technical_score'] >= 50 else 'error'}">{result['technical_score']:.0f}/100</span>
                    </div>
                    <div class="score-bar">
                        <div class="score-fill score-{'excellent' if result['technical_score'] >= 80 else 'good' if result['technical_score'] >= 60 else 'average' if result['technical_score'] >= 40 else 'poor'}" 
                             style="width: {result['technical_score']}%"></div>
                    </div>
                    
                    <div class="metric">
                        <span>Content Quality:</span>
                        <span class="{'good' if result['content_score'] >= 70 else 'warning' if result['content_score'] >= 50 else 'error'}">{result['content_score']:.0f}/100</span>
                    </div>
                    <div class="score-bar">
                        <div class="score-fill score-{'excellent' if result['content_score'] >= 80 else 'good' if result['content_score'] >= 60 else 'average' if result['content_score'] >= 40 else 'poor'}" 
                             style="width: {result['content_score']}%"></div>
                    </div>
                    
                    <div class="metric">
                        <span>Issues:</span>
                        <span class="{'error' if result['issues'] > 0 else 'good'}">{result['issues']}</span>
                    </div>
                    
                    <div class="metric">
                        <span>Warnings:</span>
                        <span class="{'warning' if result['warnings'] > 0 else 'good'}">{result['warnings']}</span>
                    </div>
                </div>
                ''' for result in seo_results])}
            </div>
            
            <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 10px;">
                <h4>📈 SEO Summary</h4>
                <p><strong>Total Issues Found:</strong> {total_issues}</p>
                <p><strong>Total Warnings:</strong> {total_warnings}</p>
                <p><strong>Average Technical Score:</strong> {avg_technical_score:.1f}/100</p>
                <p><strong>Average Content Score:</strong> {avg_content_score:.1f}/100</p>
            </div>
        </div>
        
        <div class="section">
            <h2><span class="section-icon">📋</span>All Discovered Pages</h2>
            <p>Complete list of all pages discovered during crawling:</p>
            
            <div class="pages-table">
                <table>
                    <thead>
                        <tr>
                            <th>URL</th>
                            <th>Title</th>
                            <th>Depth</th>
                            <th>Word Count</th>
                            <th>Response Time</th>
                            <th>Status</th>
                            <th>Links</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join([f'''
                        <tr class="depth-{page.get('depth', 0)}">
                            <td class="url-cell">
                                <a href="{url}" target="_blank" title="{url}">
                                    {url[:40]}{'...' if len(url) > 40 else ''}
                                </a>
                            </td>
                            <td>{page.get('title', 'No title')[:30]}{'...' if len(page.get('title', '')) > 30 else ''}</td>
                            <td>{page.get('depth', 0)}</td>
                            <td class="{'good' if page.get('word_count', 0) > 300 else 'warning'}">{page.get('word_count', 0)}</td>
                            <td class="{'good' if page.get('response_time', 0) < 2 else 'warning'}">{page.get('response_time', 0):.2f}s</td>
                            <td class="{'good' if page.get('status_code') == 200 else 'error'}">{page.get('status_code', 'N/A')}</td>
                            <td>{page.get('internal_links', 0)}</td>
                        </tr>
                        ''' for url, page in sorted(pages.items(), key=lambda x: (x[1].get('depth', 0), x[0]))])}
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="footer">
            <p>🕷️ Comprehensive Crawl & Sitemap Report • Ultimate SEO Analysis Tool</p>
            <p><strong>Generated Files:</strong></p>
            <p>🗺️ Sitemap XML: {sitemap_path}</p>
            <p>📊 This comprehensive report with all analysis results</p>
        </div>
    </div>
</body>
</html>
        """

    def _wrap_bulk_html(self, bulk_html: str, domain: str) -> str:
        """Wrap bulk HTML in complete page structure"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bulk SEO Analysis - {domain}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2b59ff 0%, #1a4bff 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
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
        .header h1 {{
            color: #2b59ff;
            font-size: 3em;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗺️ Bulk SEO Analysis Report</h1>
            <p>Comprehensive sitemap analysis for {domain}</p>
            <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        {bulk_html}
    </div>
</body>
</html>
        """

    def _wrap_competitor_html(self, competitor_html: str, main_url: str) -> str:
        """Wrap competitor HTML in complete page structure"""
        return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Competitor Analysis - {urlparse(main_url).netloc}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2b59ff 0%, #1a4bff 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
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
        .header h1 {{
            color: #2b59ff;
            font-size: 3em;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏆 Competitor Analysis Report</h1>
            <p>Strategic competitive intelligence for {main_url}</p>
            <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        {competitor_html}
    </div>
</body>
</html>
        """

    def _print_analysis_summary(self, technical_analysis, content_analysis, performance_analysis):
        """Print analysis summary"""
        technical_score = (technical_analysis['score'] / technical_analysis['max_score']) * 100
        content_score = (content_analysis['score'] / content_analysis['max_score']) * 100
        overall_score = (technical_score + content_score + performance_analysis['score']) / 3
        
        print(f"\n📊 ULTIMATE ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"🎯 Overall Score: {overall_score:.1f}/100")
        print(f"🔧 Technical SEO: {technical_score:.1f}/100")
        print(f"📝 Content Quality: {content_score:.1f}/100")
        print(f"⚡ Performance: {performance_analysis['score']}/100")
        print(f"\n🚨 Critical Issues: {len(technical_analysis.get('issues', []) + content_analysis.get('issues', []))}")
        print(f"⚠️  Warnings: {len(technical_analysis.get('warnings', []) + content_analysis.get('warnings', []))}")
        print(f"✅ Good Practices: {len(technical_analysis.get('good_practices', []) + content_analysis.get('good_practices', []))}")

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='Ultimate SEO Analysis Tool')
    parser.add_argument('url', nargs='?', help='Website URL to analyze')
    parser.add_argument('--bulk', '-b', action='store_true', help='Run bulk sitemap analysis')
    parser.add_argument('--competitors', '-c', nargs='+', help='Competitor URLs for comparison')
    parser.add_argument('--max-urls', '-m', type=int, default=100, help='Maximum URLs for bulk analysis')
    parser.add_argument('--competitor-only', action='store_true', help='Run only competitor analysis')
    parser.add_argument('--generate-sitemap', '-s', action='store_true', help='Generate comprehensive sitemap with full website crawling')
    parser.add_argument('--max-pages', '-p', type=int, default=500, help='Maximum pages to crawl for sitemap generation')
    parser.add_argument('--max-depth', '-d', type=int, default=5, help='Maximum crawl depth for sitemap generation')
    
    args = parser.parse_args()
    
    print("🚀 Ultimate SEO Analysis Tool v3.0")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found!")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    analyzer = UltimateSEOAnalyzer()
    
    # Get URL if not provided
    if not args.url:
        args.url = input("🌐 Enter the website URL to analyze: ").strip()
    
    if not args.url:
        print("❌ Error: No URL provided")
        sys.exit(1)
    
    # Add protocol if missing
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    # Determine analysis type
    if args.competitor_only and args.competitors:
        # Run only competitor analysis
        analyzer.run_competitor_analysis(args.url, args.competitors)
    elif args.generate_sitemap:
        # Run comprehensive crawling and sitemap generation
        analyzer.run_comprehensive_crawl_and_sitemap(args.url, args.max_pages, args.max_depth)
    elif args.bulk:
        # Run bulk analysis
        domain = urlparse(args.url).netloc
        analyzer.run_bulk_analysis(domain, args.max_urls)
    else:
        # Run comprehensive single analysis
        include_competitors = bool(args.competitors)
        analyzer.run_single_analysis(args.url, include_competitors, args.competitors)
    
    print("\n🎉 Analysis complete! Check the generated HTML reports for detailed insights.")

if __name__ == "__main__":
    main()