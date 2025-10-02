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

class UltimateSEOAnalyzer:
    def __init__(self):
        self.advanced_analyzer = AdvancedSEOAnalyzer()
        self.competitor_analyzer = CompetitorAnalyzer()
        self.bulk_analyzer = BulkAnalyzer()

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