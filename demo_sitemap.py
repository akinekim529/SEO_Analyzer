#!/usr/bin/env python3
"""
Demo script for Sitemap Generation feature
Shows sitemap generation capabilities without requiring full crawling
"""

import os
from datetime import datetime
from urllib.parse import urlparse

def create_demo_sitemap(url: str) -> str:
    """Create a demo sitemap XML file"""
    domain = urlparse(url).netloc.replace('www.', '').replace('.', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"demo_sitemap_{domain}_{timestamp}.xml"
    
    # Demo URLs that would be discovered
    demo_urls = [
        url,
        f"{url}/about",
        f"{url}/services",
        f"{url}/products",
        f"{url}/contact",
        f"{url}/blog",
        f"{url}/blog/article-1",
        f"{url}/blog/article-2",
        f"{url}/support",
        f"{url}/privacy-policy"
    ]
    
    sitemap_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">
'''
    
    priorities = [1.0, 0.8, 0.8, 0.8, 0.6, 0.7, 0.5, 0.5, 0.6, 0.4]
    changefreqs = ['daily', 'weekly', 'weekly', 'weekly', 'monthly', 'weekly', 'monthly', 'monthly', 'monthly', 'yearly']
    
    for i, demo_url in enumerate(demo_urls):
        sitemap_content += f'''  <url>
    <loc>{demo_url}</loc>
    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>
    <changefreq>{changefreqs[i]}</changefreq>
    <priority>{priorities[i]}</priority>
  </url>
'''
    
    sitemap_content += '</urlset>'
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    return filename

def create_demo_report(url: str, sitemap_file: str) -> str:
    """Create a demo HTML report"""
    domain = urlparse(url).netloc.replace('www.', '').replace('.', '_')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"demo_sitemap_report_{domain}_{timestamp}.html"
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DEMO - Sitemap Generation Report</title>
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
        }}
        .sitemap-info {{
            background: #e8f5e8;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            border-left: 5px solid #4caf50;
        }}
        .demo-urls {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .demo-urls ul {{
            list-style: none;
            padding: 0;
        }}
        .demo-urls li {{
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
        }}
        .demo-urls li:last-child {{
            border-bottom: none;
        }}
        .url-priority {{
            color: #2b59ff;
            font-weight: bold;
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
                🎭 DEMO MODE - Sitemap Generation Demonstration
            </div>
            <h1>🗺️ Sitemap Generation Report</h1>
            <p>Comprehensive website crawling and sitemap generation</p>
            <p><strong>Website:</strong> {url}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">10</div>
                <div class="stat-label">Pages Discovered</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">10</div>
                <div class="stat-label">Successfully Crawled</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">3</div>
                <div class="stat-label">Max Depth Reached</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">100%</div>
                <div class="stat-label">Success Rate</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🗺️ Generated Sitemap</h2>
            <div class="sitemap-info">
                <h3>📄 Sitemap XML Generated Successfully</h3>
                <p><strong>File:</strong> {sitemap_file}</p>
                <p><strong>URLs Included:</strong> 10</p>
                <p><strong>Format:</strong> XML Sitemap Protocol 0.9 with priority, changefreq, and lastmod</p>
                <p><strong>Features:</strong> Automatic priority assignment based on page depth and content quality</p>
                <p><strong>Usage:</strong> Upload this sitemap to your website root and submit to Google Search Console</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📋 Discovered URLs (Demo)</h2>
            <p>The following URLs would be discovered and included in the sitemap:</p>
            
            <div class="demo-urls">
                <ul>
                    <li><span>{url}</span> <span class="url-priority">Priority: 1.0</span></li>
                    <li><span>{url}/about</span> <span class="url-priority">Priority: 0.8</span></li>
                    <li><span>{url}/services</span> <span class="url-priority">Priority: 0.8</span></li>
                    <li><span>{url}/products</span> <span class="url-priority">Priority: 0.8</span></li>
                    <li><span>{url}/contact</span> <span class="url-priority">Priority: 0.6</span></li>
                    <li><span>{url}/blog</span> <span class="url-priority">Priority: 0.7</span></li>
                    <li><span>{url}/blog/article-1</span> <span class="url-priority">Priority: 0.5</span></li>
                    <li><span>{url}/blog/article-2</span> <span class="url-priority">Priority: 0.5</span></li>
                    <li><span>{url}/support</span> <span class="url-priority">Priority: 0.6</span></li>
                    <li><span>{url}/privacy-policy</span> <span class="url-priority">Priority: 0.4</span></li>
                </ul>
            </div>
        </div>
        
        <div class="section">
            <h2>🚀 Real Sitemap Generation Features</h2>
            <div style="background: #e3f2fd; padding: 20px; border-radius: 10px;">
                <h4>🕷️ Comprehensive Website Crawling:</h4>
                <ul>
                    <li>✅ Discovers ALL pages on your website automatically</li>
                    <li>✅ Respects robots.txt and crawling best practices</li>
                    <li>✅ Configurable depth and page limits</li>
                    <li>✅ Parallel processing for fast crawling</li>
                </ul>
                
                <h4>🗺️ Professional Sitemap Generation:</h4>
                <ul>
                    <li>✅ XML Sitemap Protocol 0.9 compliant</li>
                    <li>✅ Automatic priority assignment based on content</li>
                    <li>✅ Change frequency optimization</li>
                    <li>✅ Last modified dates from server headers</li>
                </ul>
                
                <h4>📊 SEO Analysis Integration:</h4>
                <ul>
                    <li>✅ Analyzes discovered pages for SEO issues</li>
                    <li>✅ Identifies content gaps and opportunities</li>
                    <li>✅ Generates comprehensive reports</li>
                    <li>✅ Provides actionable recommendations</li>
                </ul>
            </div>
        </div>
        
        <div class="footer">
            <p>🎭 <strong>DEMO MODE</strong> - This demonstrates the Sitemap Generation feature</p>
            <p>For real sitemap generation with full website crawling:</p>
            <p><code>python ultimate_seo_analyzer.py {url} --generate-sitemap</code></p>
            <p>🗺️ Sitemap Generation • Ultimate SEO Analysis Tool</p>
        </div>
    </div>
</body>
</html>'''
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

def main():
    print("🗺️ Sitemap Generation Demo")
    print("=" * 50)
    print("This demo shows the sitemap generation capabilities")
    print()
    
    # Get URL from user
    url = input("🌐 Enter website URL for demo sitemap (or press Enter for example.com): ").strip()
    
    if not url:
        url = "https://example.com"
        print(f"Using demo URL: {url}")
    
    # Add protocol if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"\n🕷️ Demo: Crawling website structure for {url}")
    print("📊 Demo: Discovering pages and analyzing content...")
    print("🗺️ Demo: Generating comprehensive sitemap...")
    
    # Create demo files
    sitemap_file = create_demo_sitemap(url)
    report_file = create_demo_report(url, sitemap_file)
    
    print(f"\n✅ Demo sitemap generation complete!")
    print(f"📄 Demo Sitemap: {sitemap_file}")
    print(f"📊 Demo Report: {report_file}")
    
    print(f"\n🚀 For real sitemap generation, run:")
    print(f"python ultimate_seo_analyzer.py {url} --generate-sitemap")
    print(f"python sitemap_generator.py {url}")

if __name__ == "__main__":
    main()