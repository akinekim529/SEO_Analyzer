#!/usr/bin/env python3
"""
Sitemap Generator and Website Crawler
Discovers all pages on a website and generates comprehensive sitemaps
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET
from xml.dom import minidom
import json
import time
from typing import Dict, List, Set, Any, Optional
import concurrent.futures
from threading import Lock
from datetime import datetime, timezone
import re
from collections import deque
import hashlib

class SitemapGenerator:
    def __init__(self, max_pages: int = 500, max_depth: int = 5, delay: float = 1.0):
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; SEO-Analyzer-Bot/1.0; +https://example.com/bot)'
        })
        
        # Thread-safe collections
        self.discovered_urls: Set[str] = set()
        self.crawled_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.page_data: Dict[str, Dict] = {}
        self.lock = Lock()
        
        # Crawling state
        self.robots_parser = None
        self.base_domain = ""
        self.start_url = ""

    def can_fetch(self, url: str) -> bool:
        """Check if URL can be fetched according to robots.txt"""
        if not self.robots_parser:
            return True
        
        try:
            return self.robots_parser.can_fetch('*', url)
        except:
            return True

    def normalize_url(self, url: str) -> str:
        """Normalize URL for consistent processing"""
        parsed = urlparse(url)
        
        # Remove fragment
        normalized = urlunparse((
            parsed.scheme,
            parsed.netloc.lower(),
            parsed.path,
            parsed.params,
            parsed.query,
            ''  # Remove fragment
        ))
        
        # Remove trailing slash for non-root paths
        if normalized.endswith('/') and len(parsed.path) > 1:
            normalized = normalized[:-1]
        
        return normalized

    def is_valid_url(self, url: str, base_domain: str) -> bool:
        """Check if URL should be crawled"""
        try:
            parsed = urlparse(url)
            
            # Must be same domain
            if parsed.netloc.lower() != base_domain.lower():
                return False
            
            # Skip certain file types
            skip_extensions = {
                '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                '.zip', '.rar', '.tar', '.gz', '.mp3', '.mp4', '.avi',
                '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
                '.css', '.js', '.xml', '.txt', '.json'
            }
            
            path_lower = parsed.path.lower()
            if any(path_lower.endswith(ext) for ext in skip_extensions):
                return False
            
            # Skip admin/system paths
            skip_paths = [
                '/admin', '/wp-admin', '/wp-content', '/wp-includes',
                '/cgi-bin', '/api/', '/ajax/', '/search', '/login',
                '/register', '/cart', '/checkout', '/account'
            ]
            
            if any(skip_path in path_lower for skip_path in skip_paths):
                return False
            
            # Skip URLs with certain parameters
            skip_params = ['utm_', 'fbclid', 'gclid', 'ref=', 'source=']
            if parsed.query and any(param in parsed.query for param in skip_params):
                return False
            
            return True
            
        except:
            return False

    def setup_robots_parser(self, base_url: str):
        """Setup robots.txt parser"""
        try:
            robots_url = urljoin(base_url, '/robots.txt')
            self.robots_parser = RobotFileParser()
            self.robots_parser.set_url(robots_url)
            self.robots_parser.read()
            print(f"✅ Loaded robots.txt from {robots_url}")
        except Exception as e:
            print(f"⚠️ Could not load robots.txt: {str(e)}")
            self.robots_parser = None

    def extract_links_from_page(self, url: str, html_content: str) -> Set[str]:
        """Extract all valid links from a page"""
        links = set()
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract links from <a> tags
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(url, href)
                normalized_url = self.normalize_url(absolute_url)
                
                if self.is_valid_url(normalized_url, self.base_domain):
                    links.add(normalized_url)
            
            # Extract links from sitemaps referenced in the page
            for link in soup.find_all('link', rel='sitemap'):
                href = link.get('href')
                if href:
                    sitemap_url = urljoin(url, href)
                    sitemap_links = self.extract_urls_from_sitemap(sitemap_url)
                    links.update(sitemap_links)
            
        except Exception as e:
            print(f"⚠️ Error extracting links from {url}: {str(e)}")
        
        return links

    def extract_urls_from_sitemap(self, sitemap_url: str) -> Set[str]:
        """Extract URLs from XML sitemap"""
        urls = set()
        
        try:
            response = self.session.get(sitemap_url, timeout=10)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                
                # Handle different sitemap namespaces
                namespaces = {
                    'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'
                }
                
                # Check if it's a sitemap index
                sitemaps = root.findall('.//sitemap:sitemap', namespaces)
                if sitemaps:
                    for sitemap in sitemaps:
                        loc = sitemap.find('sitemap:loc', namespaces)
                        if loc is not None:
                            sub_urls = self.extract_urls_from_sitemap(loc.text)
                            urls.update(sub_urls)
                else:
                    # Regular sitemap with URLs
                    url_elements = root.findall('.//sitemap:url', namespaces)
                    for url_elem in url_elements:
                        loc = url_elem.find('sitemap:loc', namespaces)
                        if loc is not None:
                            normalized_url = self.normalize_url(loc.text)
                            if self.is_valid_url(normalized_url, self.base_domain):
                                urls.add(normalized_url)
        
        except Exception as e:
            print(f"⚠️ Error parsing sitemap {sitemap_url}: {str(e)}")
        
        return urls

    def crawl_page(self, url: str, depth: int = 0) -> Dict[str, Any]:
        """Crawl a single page and extract information"""
        try:
            # Check if already crawled
            with self.lock:
                if url in self.crawled_urls or url in self.failed_urls:
                    return {}
            
            # Check robots.txt
            if not self.can_fetch(url):
                with self.lock:
                    self.failed_urls.add(url)
                return {}
            
            # Add delay to be respectful
            time.sleep(self.delay)
            
            print(f"🔍 Crawling: {url} (depth: {depth})")
            
            start_time = time.time()
            response = self.session.get(url, timeout=15)
            response_time = time.time() - start_time
            
            if response.status_code != 200:
                with self.lock:
                    self.failed_urls.add(url)
                return {}
            
            # Parse content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract page information
            page_info = {
                'url': url,
                'title': soup.find('title').get_text().strip() if soup.find('title') else '',
                'meta_description': '',
                'h1_tags': [h1.get_text().strip() for h1 in soup.find_all('h1')],
                'word_count': len(soup.get_text().split()),
                'last_modified': response.headers.get('last-modified', ''),
                'content_type': response.headers.get('content-type', ''),
                'status_code': response.status_code,
                'response_time': response_time,
                'page_size': len(response.content),
                'depth': depth,
                'crawl_timestamp': datetime.now(timezone.utc).isoformat(),
                'links_found': 0,
                'images': len(soup.find_all('img')),
                'internal_links': 0,
                'external_links': 0
            }
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                page_info['meta_description'] = meta_desc.get('content', '')
            
            # Extract links if not at max depth
            new_links = set()
            if depth < self.max_depth:
                new_links = self.extract_links_from_page(url, response.text)
                page_info['links_found'] = len(new_links)
                
                # Count internal vs external links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(url, href)
                    parsed_link = urlparse(absolute_url)
                    
                    if parsed_link.netloc.lower() == self.base_domain.lower():
                        page_info['internal_links'] += 1
                    elif parsed_link.netloc:
                        page_info['external_links'] += 1
            
            # Update thread-safe collections
            with self.lock:
                self.crawled_urls.add(url)
                self.page_data[url] = page_info
                
                # Add new links to discovered set
                for link in new_links:
                    if (link not in self.discovered_urls and 
                        link not in self.crawled_urls and 
                        len(self.discovered_urls) < self.max_pages):
                        self.discovered_urls.add(link)
            
            return page_info
            
        except Exception as e:
            print(f"❌ Error crawling {url}: {str(e)}")
            with self.lock:
                self.failed_urls.add(url)
            return {}

    def discover_website_structure(self, start_url: str) -> Dict[str, Any]:
        """Discover entire website structure through crawling"""
        print(f"\n🕷️ Starting website discovery for: {start_url}")
        print("=" * 80)
        
        # Setup
        self.start_url = start_url
        parsed_start = urlparse(start_url)
        self.base_domain = parsed_start.netloc
        
        # Setup robots.txt parser
        self.setup_robots_parser(start_url)
        
        # Initialize with start URL
        self.discovered_urls.add(self.normalize_url(start_url))
        
        # Try to find existing sitemaps first
        print("🗺️ Looking for existing sitemaps...")
        existing_sitemap_urls = self.find_existing_sitemaps(start_url)
        
        if existing_sitemap_urls:
            print(f"✅ Found {len(existing_sitemap_urls)} existing sitemaps")
            for sitemap_url in existing_sitemap_urls:
                sitemap_links = self.extract_urls_from_sitemap(sitemap_url)
                print(f"   📄 {sitemap_url}: {len(sitemap_links)} URLs")
                
                # Add sitemap URLs to discovered set
                for link in sitemap_links:
                    if len(self.discovered_urls) < self.max_pages:
                        self.discovered_urls.add(link)
        
        # Breadth-first crawling
        print(f"\n🔍 Starting breadth-first crawling (max {self.max_pages} pages, max depth {self.max_depth})")
        
        current_depth = 0
        while current_depth <= self.max_depth and len(self.crawled_urls) < self.max_pages:
            # Get URLs at current depth
            urls_to_crawl = []
            with self.lock:
                for url in list(self.discovered_urls):
                    if (url not in self.crawled_urls and 
                        url not in self.failed_urls and 
                        len(urls_to_crawl) < 50):  # Process in batches
                        urls_to_crawl.append(url)
            
            if not urls_to_crawl:
                break
            
            print(f"\n📊 Crawling depth {current_depth}: {len(urls_to_crawl)} URLs")
            
            # Crawl URLs in parallel (limited concurrency)
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = {
                    executor.submit(self.crawl_page, url, current_depth): url 
                    for url in urls_to_crawl
                }
                
                completed = 0
                for future in concurrent.futures.as_completed(futures):
                    completed += 1
                    if completed % 10 == 0:
                        print(f"   Progress: {completed}/{len(urls_to_crawl)} pages crawled")
            
            current_depth += 1
            
            # Progress update
            with self.lock:
                print(f"   ✅ Crawled: {len(self.crawled_urls)}, Failed: {len(self.failed_urls)}, Discovered: {len(self.discovered_urls)}")
        
        # Generate summary
        summary = {
            'start_url': start_url,
            'base_domain': self.base_domain,
            'total_discovered': len(self.discovered_urls),
            'total_crawled': len(self.crawled_urls),
            'total_failed': len(self.failed_urls),
            'max_depth_reached': current_depth - 1,
            'existing_sitemaps_found': len(existing_sitemap_urls) if existing_sitemap_urls else 0,
            'crawl_timestamp': datetime.now(timezone.utc).isoformat(),
            'pages': dict(self.page_data)
        }
        
        print(f"\n📊 WEBSITE DISCOVERY COMPLETE")
        print("=" * 50)
        print(f"🎯 Total URLs Discovered: {summary['total_discovered']}")
        print(f"✅ Successfully Crawled: {summary['total_crawled']}")
        print(f"❌ Failed to Crawl: {summary['total_failed']}")
        print(f"📏 Maximum Depth Reached: {summary['max_depth_reached']}")
        
        return summary

    def find_existing_sitemaps(self, base_url: str) -> List[str]:
        """Find existing sitemaps on the website"""
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
        
        for path in common_paths:
            try:
                url = urljoin(base_url, path)
                response = self.session.get(url, timeout=10)
                if response.status_code == 200 and 'xml' in response.headers.get('content-type', ''):
                    sitemap_urls.append(url)
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
        except:
            pass
        
        return sitemap_urls

    def generate_sitemap_xml(self, discovery_data: Dict[str, Any], output_path: str = None) -> str:
        """Generate comprehensive XML sitemap"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = discovery_data['base_domain'].replace('.', '_')
            output_path = f"sitemap_{domain}_{timestamp}.xml"
        
        print(f"\n📝 Generating comprehensive sitemap: {output_path}")
        
        # Create XML structure
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        urlset.set('xsi:schemaLocation', 
                  'http://www.sitemaps.org/schemas/sitemap/0.9 '
                  'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
        
        # Add URLs from crawled pages
        pages = discovery_data.get('pages', {})
        sorted_urls = sorted(pages.keys(), key=lambda x: (pages[x].get('depth', 0), x))
        
        for url in sorted_urls:
            page_data = pages[url]
            
            # Skip if page had errors
            if page_data.get('status_code', 0) != 200:
                continue
            
            url_elem = ET.SubElement(urlset, 'url')
            
            # Location (required)
            loc = ET.SubElement(url_elem, 'loc')
            loc.text = url
            
            # Last modified
            if page_data.get('last_modified'):
                lastmod = ET.SubElement(url_elem, 'lastmod')
                try:
                    # Parse and format the date
                    from email.utils import parsedate_to_datetime
                    dt = parsedate_to_datetime(page_data['last_modified'])
                    lastmod.text = dt.strftime('%Y-%m-%d')
                except:
                    # Use crawl timestamp as fallback
                    crawl_time = page_data.get('crawl_timestamp', '')
                    if crawl_time:
                        lastmod.text = crawl_time.split('T')[0]
            
            # Change frequency (based on depth and content)
            changefreq = ET.SubElement(url_elem, 'changefreq')
            depth = page_data.get('depth', 0)
            word_count = page_data.get('word_count', 0)
            
            if depth == 0:  # Homepage
                changefreq.text = 'daily'
            elif depth == 1 and word_count > 500:  # Main pages with content
                changefreq.text = 'weekly'
            elif word_count > 1000:  # Content-rich pages
                changefreq.text = 'monthly'
            else:
                changefreq.text = 'yearly'
            
            # Priority (based on depth and importance)
            priority = ET.SubElement(url_elem, 'priority')
            if depth == 0:  # Homepage
                priority.text = '1.0'
            elif depth == 1:  # Main sections
                priority.text = '0.8'
            elif depth == 2:  # Secondary pages
                priority.text = '0.6'
            else:  # Deep pages
                priority.text = '0.4'
        
        # Create pretty XML
        rough_string = ET.tostring(urlset, 'unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="  ")
        
        # Remove empty lines
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        print(f"✅ Sitemap generated with {len(sorted_urls)} URLs")
        print(f"📄 Saved as: {output_path}")
        
        return output_path

    def generate_sitemap_report(self, discovery_data: Dict[str, Any], sitemap_path: str) -> str:
        """Generate HTML report for sitemap generation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = discovery_data['base_domain'].replace('.', '_')
        report_path = f"sitemap_report_{domain}_{timestamp}.html"
        
        pages = discovery_data.get('pages', {})
        
        # Calculate statistics
        stats = {
            'total_pages': len(pages),
            'avg_response_time': sum(p.get('response_time', 0) for p in pages.values()) / len(pages) if pages else 0,
            'avg_word_count': sum(p.get('word_count', 0) for p in pages.values()) / len(pages) if pages else 0,
            'pages_by_depth': {},
            'pages_missing_title': len([p for p in pages.values() if not p.get('title')]),
            'pages_missing_meta_desc': len([p for p in pages.values() if not p.get('meta_description')]),
            'total_internal_links': sum(p.get('internal_links', 0) for p in pages.values()),
            'total_external_links': sum(p.get('external_links', 0) for p in pages.values()),
        }
        
        # Pages by depth
        for page in pages.values():
            depth = page.get('depth', 0)
            stats['pages_by_depth'][depth] = stats['pages_by_depth'].get(depth, 0) + 1
        
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sitemap Generation Report - {discovery_data['base_domain']}</title>
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
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
        .pages-table {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }}
        .pages-table h2 {{
            color: #2b59ff;
            margin-bottom: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #2b59ff;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .url-cell {{
            max-width: 300px;
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
        .sitemap-info {{
            background: #e3f2fd;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
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
            <h1>🗺️ Sitemap Generation Report</h1>
            <p>Comprehensive website crawling and sitemap generation</p>
            <p><strong>Domain:</strong> {discovery_data['base_domain']}</p>
            <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{stats['total_pages']}</div>
                <div class="stat-label">Total Pages Discovered</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{discovery_data['total_crawled']}</div>
                <div class="stat-label">Successfully Crawled</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{discovery_data['max_depth_reached']}</div>
                <div class="stat-label">Maximum Depth Reached</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['avg_response_time']:.2f}s</div>
                <div class="stat-label">Average Response Time</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['avg_word_count']:.0f}</div>
                <div class="stat-label">Average Word Count</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['total_internal_links']}</div>
                <div class="stat-label">Total Internal Links</div>
            </div>
        </div>
        
        <div class="sitemap-info">
            <h3>📄 Generated Sitemap Information</h3>
            <p><strong>Sitemap File:</strong> {sitemap_path}</p>
            <p><strong>URLs Included:</strong> {len([p for p in pages.values() if p.get('status_code') == 200])}</p>
            <p><strong>Format:</strong> XML Sitemap Protocol 0.9</p>
            <p><strong>Features:</strong> Includes priority, change frequency, and last modified dates</p>
        </div>
        
        <div class="pages-table">
            <h2>📋 Discovered Pages Details</h2>
            <p>Pages by depth: {', '.join([f'Depth {k}: {v} pages' for k, v in sorted(stats['pages_by_depth'].items())])}</p>
            
            <table>
                <thead>
                    <tr>
                        <th>URL</th>
                        <th>Title</th>
                        <th>Depth</th>
                        <th>Word Count</th>
                        <th>Response Time</th>
                        <th>Status</th>
                        <th>Internal Links</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join([f'''
                    <tr class="depth-{page.get('depth', 0)}">
                        <td class="url-cell">
                            <a href="{url}" target="_blank" title="{url}">
                                {url[:60]}{'...' if len(url) > 60 else ''}
                            </a>
                        </td>
                        <td>{page.get('title', 'No title')[:50]}{'...' if len(page.get('title', '')) > 50 else ''}</td>
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
        
        <div class="footer">
            <p>🗺️ Sitemap Generation Report • Ultimate SEO Analysis Tool</p>
            <p>Sitemap saved as: <strong>{sitemap_path}</strong></p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📊 Sitemap report generated: {report_path}")
        return report_path

def main():
    """Main function for standalone sitemap generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Website Sitemap Generator')
    parser.add_argument('url', help='Website URL to crawl')
    parser.add_argument('--max-pages', '-p', type=int, default=500, help='Maximum pages to crawl')
    parser.add_argument('--max-depth', '-d', type=int, default=5, help='Maximum crawl depth')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    
    args = parser.parse_args()
    
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    # Create sitemap generator
    generator = SitemapGenerator(
        max_pages=args.max_pages,
        max_depth=args.max_depth,
        delay=args.delay
    )
    
    # Discover website structure
    discovery_data = generator.discover_website_structure(args.url)
    
    # Generate sitemap
    sitemap_path = generator.generate_sitemap_xml(discovery_data)
    
    # Generate report
    report_path = generator.generate_sitemap_report(discovery_data, sitemap_path)
    
    print(f"\n🎉 Sitemap generation complete!")
    print(f"📄 Sitemap: {sitemap_path}")
    print(f"📊 Report: {report_path}")

if __name__ == "__main__":
    main()