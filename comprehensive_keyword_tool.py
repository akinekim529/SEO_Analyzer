#!/usr/bin/env python3
"""
Comprehensive Keyword Analysis Tool
Main application that integrates keyword analysis, report generation, and file management
"""

import os
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

# Import our modules
from keyword_analyzer import KeywordAnalyzer
from keyword_report_generator import KeywordReportGenerator

class ComprehensiveKeywordTool:
    def __init__(self):
        self.keyword_analyzer = KeywordAnalyzer()
        self.report_generator = KeywordReportGenerator()
        self.desktop_folder = self._create_desktop_folder()

    def _create_desktop_folder(self) -> str:
        """Create desktop folder for saving reports"""
        try:
            # Get desktop path (works on Windows, macOS, Linux)
            home = Path.home()
            
            # Try different desktop locations
            desktop_paths = [
                home / "Desktop",
                home / "Masaüstü",  # Turkish
                home / "Bureau",    # French
                home / "Escritorio", # Spanish
                home / "デスクトップ"   # Japanese
            ]
            
            desktop_path = None
            for path in desktop_paths:
                if path.exists():
                    desktop_path = path
                    break
            
            # If no desktop found, use home directory
            if not desktop_path:
                desktop_path = home
            
            # Create keyword analysis folder
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            folder_name = f"Keyword_Analysis_Reports_{timestamp}"
            analysis_folder = desktop_path / folder_name
            
            analysis_folder.mkdir(exist_ok=True)
            
            # Create subfolders
            (analysis_folder / "HTML_Reports").mkdir(exist_ok=True)
            (analysis_folder / "JSON_Data").mkdir(exist_ok=True)
            (analysis_folder / "CSV_Exports").mkdir(exist_ok=True)
            (analysis_folder / "Competitive_Analysis").mkdir(exist_ok=True)
            
            print(f"📁 Created analysis folder: {analysis_folder}")
            return str(analysis_folder)
            
        except Exception as e:
            print(f"⚠️ Warning: Could not create desktop folder: {str(e)}")
            # Fallback to current directory
            fallback_folder = f"Keyword_Analysis_Reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(fallback_folder, exist_ok=True)
            return fallback_folder

    def analyze_url_comprehensive(self, url: str, include_competitors: bool = False, 
                                competitor_urls: List[str] = None) -> Dict[str, Any]:
        """Perform comprehensive keyword analysis on a URL"""
        print(f"\n🚀 Starting comprehensive keyword analysis for: {url}")
        print("=" * 80)
        
        try:
            # Main URL analysis
            print("🔍 Analyzing main URL...")
            main_analysis = self.keyword_analyzer.analyze_url_keywords(url)
            
            if 'error' in main_analysis:
                print(f"❌ Error analyzing main URL: {main_analysis['error']}")
                return main_analysis
            
            # Competitive analysis if requested
            competitive_data = None
            if include_competitors and competitor_urls:
                print("🏆 Performing competitive analysis...")
                competitive_data = self.keyword_analyzer.analyze_competitor_keywords(competitor_urls)
                
                if 'error' not in competitive_data:
                    print(f"✅ Analyzed {competitive_data.get('total_competitors', 0)} competitors")
                else:
                    print(f"⚠️ Competitive analysis failed: {competitive_data['error']}")
                    competitive_data = None
            
            # Generate comprehensive report
            print("📊 Generating comprehensive HTML report...")
            html_report = self.report_generator.generate_comprehensive_report(
                main_analysis, competitive_data
            )
            
            # Save all files
            self._save_analysis_files(main_analysis, competitive_data, html_report, url)
            
            return {
                'main_analysis': main_analysis,
                'competitive_data': competitive_data,
                'success': True,
                'folder_path': self.desktop_folder
            }
            
        except Exception as e:
            error_msg = f"Error in comprehensive analysis: {str(e)}"
            print(f"❌ {error_msg}")
            return {'error': error_msg}

    def analyze_text_comprehensive(self, text: str, title: str = "", 
                                 description: str = "") -> Dict[str, Any]:
        """Perform comprehensive keyword analysis on text"""
        print(f"\n🚀 Starting comprehensive keyword analysis for provided text")
        print("=" * 80)
        
        try:
            # Text analysis
            print("🔍 Analyzing provided text...")
            text_analysis = self.keyword_analyzer.analyze_text_keywords(text, title, description)
            
            if 'error' in text_analysis:
                print(f"❌ Error analyzing text: {text_analysis['error']}")
                return text_analysis
            
            # Generate comprehensive report
            print("📊 Generating comprehensive HTML report...")
            html_report = self.report_generator.generate_comprehensive_report(text_analysis)
            
            # Save all files
            self._save_analysis_files(text_analysis, None, html_report, "Text_Input")
            
            return {
                'text_analysis': text_analysis,
                'success': True,
                'folder_path': self.desktop_folder
            }
            
        except Exception as e:
            error_msg = f"Error in text analysis: {str(e)}"
            print(f"❌ {error_msg}")
            return {'error': error_msg}

    def analyze_multiple_urls(self, urls: List[str]) -> Dict[str, Any]:
        """Analyze multiple URLs and compare them"""
        print(f"\n🚀 Starting multi-URL keyword analysis for {len(urls)} URLs")
        print("=" * 80)
        
        try:
            all_analyses = []
            successful_analyses = []
            
            for i, url in enumerate(urls, 1):
                print(f"🔍 Analyzing URL {i}/{len(urls)}: {url}")
                analysis = self.keyword_analyzer.analyze_url_keywords(url)
                
                all_analyses.append({
                    'url': url,
                    'analysis': analysis,
                    'success': 'error' not in analysis
                })
                
                if 'error' not in analysis:
                    successful_analyses.append(analysis)
                else:
                    print(f"   ❌ Failed: {analysis['error']}")
            
            if not successful_analyses:
                return {'error': 'No URLs were successfully analyzed'}
            
            # Perform comparative analysis
            print("📊 Performing comparative analysis...")
            comparative_data = self.keyword_analyzer._perform_competitive_analysis(successful_analyses)
            
            # Generate individual reports for each URL
            print("📄 Generating individual reports...")
            for analysis_data in all_analyses:
                if analysis_data['success']:
                    html_report = self.report_generator.generate_comprehensive_report(
                        analysis_data['analysis']
                    )
                    self._save_analysis_files(
                        analysis_data['analysis'], 
                        None, 
                        html_report, 
                        analysis_data['url']
                    )
            
            # Generate comparative report
            print("📊 Generating comparative analysis report...")
            comparative_report = self._generate_comparative_report(all_analyses, comparative_data)
            
            # Save comparative report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            comparative_filename = f"Comparative_Analysis_{timestamp}.html"
            comparative_path = os.path.join(self.desktop_folder, "HTML_Reports", comparative_filename)
            
            with open(comparative_path, 'w', encoding='utf-8') as f:
                f.write(comparative_report)
            
            print(f"✅ Comparative report saved: {comparative_filename}")
            
            return {
                'all_analyses': all_analyses,
                'comparative_data': comparative_data,
                'successful_count': len(successful_analyses),
                'total_count': len(urls),
                'success': True,
                'folder_path': self.desktop_folder
            }
            
        except Exception as e:
            error_msg = f"Error in multi-URL analysis: {str(e)}"
            print(f"❌ {error_msg}")
            return {'error': error_msg}

    def _save_analysis_files(self, main_analysis: Dict[str, Any], 
                           competitive_data: Optional[Dict[str, Any]], 
                           html_report: str, source: str):
        """Save all analysis files to desktop folder"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Clean source name for filename
            if source.startswith('http'):
                domain = urlparse(source).netloc.replace('www.', '').replace('.', '_')
                source_name = domain
            else:
                source_name = source.replace(' ', '_').replace('/', '_')
            
            # Save HTML report
            html_filename = f"Keyword_Analysis_{source_name}_{timestamp}.html"
            html_path = os.path.join(self.desktop_folder, "HTML_Reports", html_filename)
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_report)
            
            print(f"✅ HTML report saved: {html_filename}")
            
            # Save JSON data
            json_filename = f"Analysis_Data_{source_name}_{timestamp}.json"
            json_path = os.path.join(self.desktop_folder, "JSON_Data", json_filename)
            
            json_data = {
                'main_analysis': main_analysis,
                'competitive_data': competitive_data,
                'generated_at': datetime.now().isoformat(),
                'source': source
            }
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ JSON data saved: {json_filename}")
            
            # Save CSV export
            csv_filename = f"Keywords_{source_name}_{timestamp}.csv"
            csv_path = os.path.join(self.desktop_folder, "CSV_Exports", csv_filename)
            
            self.keyword_analyzer.export_analysis_to_csv(main_analysis, csv_path)
            print(f"✅ CSV export saved: {csv_filename}")
            
            # Save competitive data if available
            if competitive_data and 'error' not in competitive_data:
                comp_filename = f"Competitive_Data_{source_name}_{timestamp}.json"
                comp_path = os.path.join(self.desktop_folder, "Competitive_Analysis", comp_filename)
                
                with open(comp_path, 'w', encoding='utf-8') as f:
                    json.dump(competitive_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Competitive data saved: {comp_filename}")
            
        except Exception as e:
            print(f"⚠️ Warning: Error saving files: {str(e)}")

    def _generate_comparative_report(self, all_analyses: List[Dict[str, Any]], 
                                   comparative_data: Dict[str, Any]) -> str:
        """Generate comparative analysis HTML report"""
        successful_analyses = [a for a in all_analyses if a['success']]
        failed_analyses = [a for a in all_analyses if not a['success']]
        
        # Generate summary statistics
        total_keywords = []
        url_stats = []
        
        for analysis_data in successful_analyses:
            analysis = analysis_data['analysis']
            url = analysis_data['url']
            
            keywords = analysis.get('primary_keywords', [])
            total_keywords.extend(keywords)
            
            text_stats = analysis.get('text_statistics', {})
            url_stats.append({
                'url': url,
                'domain': urlparse(url).netloc,
                'word_count': text_stats.get('word_count', 0),
                'unique_words': text_stats.get('unique_words', 0),
                'top_keywords': keywords[:10],
                'sentiment': analysis.get('sentiment_analysis', {}).get('overall_sentiment', 'neutral')
            })
        
        # Create HTML report
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔍 Comparative Keyword Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
            margin: 0;
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
            color: #667eea;
            font-size: 3em;
            margin-bottom: 10px;
        }}
        
        .section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }}
        
        .section h2 {{
            color: #667eea;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            font-size: 1.8em;
        }}
        
        .section-icon {{
            margin-right: 15px;
            font-size: 1.2em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .url-comparison {{
            display: grid;
            gap: 20px;
            margin: 20px 0;
        }}
        
        .url-item {{
            background: #f8f9ff;
            border-radius: 15px;
            padding: 20px;
            border-left: 5px solid #667eea;
        }}
        
        .url-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        
        .url-title {{
            font-weight: bold;
            color: #333;
            font-size: 1.1em;
        }}
        
        .url-domain {{
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.9em;
        }}
        
        .url-stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }}
        
        .url-stat {{
            text-align: center;
            background: white;
            padding: 10px;
            border-radius: 8px;
        }}
        
        .url-stat-number {{
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }}
        
        .url-stat-label {{
            font-size: 0.9em;
            color: #666;
        }}
        
        .keywords-preview {{
            margin-top: 15px;
        }}
        
        .keywords-preview h4 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .keyword-tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .keyword-tag {{
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
        }}
        
        .competitive-insights {{
            background: #f8f9ff;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        }}
        
        .competitive-insights h3 {{
            color: #667eea;
            margin-bottom: 20px;
        }}
        
        .insights-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .insight-box {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #764ba2;
        }}
        
        .insight-title {{
            font-weight: bold;
            color: #764ba2;
            margin-bottom: 10px;
        }}
        
        .failed-urls {{
            background: #ffebee;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            border-left: 5px solid #f44336;
        }}
        
        .failed-urls h3 {{
            color: #f44336;
            margin-bottom: 15px;
        }}
        
        .failed-item {{
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }}
        
        .failed-url {{
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .failed-error {{
            color: #f44336;
            font-size: 0.9em;
        }}
        
        .footer {{
            text-align: center;
            color: rgba(255, 255, 255, 0.9);
            margin-top: 40px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Comparative Keyword Analysis Report</h1>
            <p><strong>Analysis Date:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>Comprehensive keyword comparison across multiple URLs</p>
        </div>
        
        <div class="section">
            <h2><span class="section-icon">📊</span>Analysis Overview</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{len(all_analyses)}</div>
                    <div class="stat-label">Total URLs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(successful_analyses)}</div>
                    <div class="stat-label">Successfully Analyzed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(failed_analyses)}</div>
                    <div class="stat-label">Failed Analyses</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(set(total_keywords))}</div>
                    <div class="stat-label">Unique Keywords</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2><span class="section-icon">🌐</span>URL Comparison</h2>
            <div class="url-comparison">
                {"".join([f'''
                <div class="url-item">
                    <div class="url-header">
                        <div class="url-title">{stat['url'][:60]}{'...' if len(stat['url']) > 60 else ''}</div>
                        <div class="url-domain">{stat['domain']}</div>
                    </div>
                    
                    <div class="url-stats">
                        <div class="url-stat">
                            <div class="url-stat-number">{stat['word_count']:,}</div>
                            <div class="url-stat-label">Words</div>
                        </div>
                        <div class="url-stat">
                            <div class="url-stat-number">{stat['unique_words']:,}</div>
                            <div class="url-stat-label">Unique Words</div>
                        </div>
                        <div class="url-stat">
                            <div class="url-stat-number">{stat['sentiment'].title()}</div>
                            <div class="url-stat-label">Sentiment</div>
                        </div>
                    </div>
                    
                    <div class="keywords-preview">
                        <h4>Top Keywords</h4>
                        <div class="keyword-tags">
                            {"".join([f'<span class="keyword-tag">{kw}</span>' for kw in stat['top_keywords']])}
                        </div>
                    </div>
                </div>
                ''' for stat in url_stats])}
            </div>
        </div>
        
        {f'''
        <div class="section">
            <h2><span class="section-icon">🏆</span>Competitive Insights</h2>
            <div class="competitive-insights">
                <h3>📈 Key Findings</h3>
                <div class="insights-grid">
                    <div class="insight-box">
                        <div class="insight-title">Common Keywords</div>
                        <div>{"".join([f'<span class="keyword-tag">{kw}</span> ' for kw in comparative_data.get('common_keywords', [])[:10]])}</div>
                    </div>
                    
                    <div class="insight-box">
                        <div class="insight-title">Most Frequent Keywords</div>
                        <div>{"".join([f'<span class="keyword-tag">{kw}</span> ' for kw in comparative_data.get('most_frequent_keywords', [])[:10]])}</div>
                    </div>
                    
                    <div class="insight-box">
                        <div class="insight-title">Total Unique Keywords</div>
                        <div style="font-size: 2em; font-weight: bold; color: #667eea;">{comparative_data.get('total_unique_keywords', 0)}</div>
                    </div>
                </div>
            </div>
        </div>
        ''' if comparative_data and 'error' not in comparative_data else ''}
        
        {f'''
        <div class="section">
            <h2><span class="section-icon">❌</span>Failed Analyses</h2>
            <div class="failed-urls">
                <h3>URLs that could not be analyzed:</h3>
                {"".join([f'''
                <div class="failed-item">
                    <div class="failed-url">{analysis['url']}</div>
                    <div class="failed-error">Error: {analysis['analysis'].get('error', 'Unknown error')}</div>
                </div>
                ''' for analysis in failed_analyses])}
            </div>
        </div>
        ''' if failed_analyses else ''}
        
        <div class="footer">
            <h3>🚀 Comparative Analysis Complete</h3>
            <p>This report provides a comprehensive comparison of keyword usage across multiple URLs.</p>
            <p>Individual detailed reports have been generated for each successfully analyzed URL.</p>
            <p><strong>Powered by AI • Comprehensive Keyword Analysis Tool</strong></p>
        </div>
    </div>
</body>
</html>
        """
        
        return html_content

    def print_analysis_summary(self, result: Dict[str, Any]):
        """Print analysis summary"""
        if result.get('success'):
            print(f"\n🎉 ANALYSIS COMPLETE!")
            print("=" * 60)
            print(f"📁 All files saved to: {result['folder_path']}")
            print(f"\n📄 Generated Files:")
            print(f"   🌐 HTML Report (comprehensive visualization)")
            print(f"   📊 JSON Data (structured analysis data)")
            print(f"   📋 CSV Export (keyword data for spreadsheets)")
            
            if result.get('competitive_data'):
                print(f"   🏆 Competitive Analysis Data")
            
            if 'successful_count' in result:
                print(f"\n📈 Multi-URL Analysis:")
                print(f"   ✅ Successfully analyzed: {result['successful_count']}/{result['total_count']} URLs")
                print(f"   📊 Comparative report generated")
            
            print(f"\n💡 Next Steps:")
            print(f"   1. Open the HTML report in your browser for detailed insights")
            print(f"   2. Review AI recommendations for optimization opportunities")
            print(f"   3. Use CSV data for further analysis in spreadsheet applications")
            print(f"   4. Implement suggested keyword optimizations")
        else:
            print(f"\n❌ ANALYSIS FAILED")
            print(f"Error: {result.get('error', 'Unknown error')}")

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='Comprehensive Keyword Analysis Tool')
    parser.add_argument('input', nargs='?', help='URL to analyze or text file path')
    parser.add_argument('--text', '-t', help='Analyze provided text directly')
    parser.add_argument('--title', help='Title for text analysis')
    parser.add_argument('--description', '-d', help='Description for text analysis')
    parser.add_argument('--competitors', '-c', nargs='+', help='Competitor URLs for comparison')
    parser.add_argument('--multiple', '-m', nargs='+', help='Multiple URLs to analyze and compare')
    parser.add_argument('--file', '-f', help='File containing URLs (one per line)')
    
    args = parser.parse_args()
    
    print("🚀 Comprehensive Keyword Analysis Tool v1.0")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ Error: .env file not found!")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    tool = ComprehensiveKeywordTool()
    
    try:
        # Determine analysis type
        if args.text:
            # Text analysis
            result = tool.analyze_text_comprehensive(
                args.text, 
                args.title or "", 
                args.description or ""
            )
            
        elif args.multiple:
            # Multiple URL analysis
            result = tool.analyze_multiple_urls(args.multiple)
            
        elif args.file:
            # URLs from file
            if not os.path.exists(args.file):
                print(f"❌ Error: File not found: {args.file}")
                sys.exit(1)
            
            with open(args.file, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            if not urls:
                print("❌ Error: No valid URLs found in file")
                sys.exit(1)
            
            result = tool.analyze_multiple_urls(urls)
            
        elif args.input:
            # Single URL analysis
            url = args.input
            
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Check if it's a file path
            if os.path.exists(args.input):
                with open(args.input, 'r', encoding='utf-8') as f:
                    text_content = f.read()
                
                result = tool.analyze_text_comprehensive(
                    text_content,
                    args.title or os.path.basename(args.input),
                    args.description or ""
                )
            else:
                # URL analysis
                include_competitors = bool(args.competitors)
                result = tool.analyze_url_comprehensive(url, include_competitors, args.competitors)
        else:
            # Interactive mode
            print("\n🌐 Interactive Mode")
            print("Choose analysis type:")
            print("1. Analyze URL")
            print("2. Analyze text")
            print("3. Analyze multiple URLs")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                url = input("Enter URL to analyze: ").strip()
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                comp_input = input("Enter competitor URLs (comma-separated, optional): ").strip()
                competitors = [u.strip() for u in comp_input.split(',') if u.strip()] if comp_input else None
                
                result = tool.analyze_url_comprehensive(url, bool(competitors), competitors)
                
            elif choice == '2':
                print("Enter your text (press Ctrl+D or Ctrl+Z when finished):")
                text_lines = []
                try:
                    while True:
                        line = input()
                        text_lines.append(line)
                except EOFError:
                    pass
                
                text = '\n'.join(text_lines)
                title = input("Enter title (optional): ").strip()
                description = input("Enter description (optional): ").strip()
                
                result = tool.analyze_text_comprehensive(text, title, description)
                
            elif choice == '3':
                urls_input = input("Enter URLs (comma-separated): ").strip()
                urls = [u.strip() for u in urls_input.split(',') if u.strip()]
                
                if not urls:
                    print("❌ Error: No URLs provided")
                    sys.exit(1)
                
                result = tool.analyze_multiple_urls(urls)
                
            else:
                print("❌ Invalid choice")
                sys.exit(1)
        
        # Print summary
        tool.print_analysis_summary(result)
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Analysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()