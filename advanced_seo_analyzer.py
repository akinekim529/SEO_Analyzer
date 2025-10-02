#!/usr/bin/env python3
"""
Advanced Comprehensive SEO Analysis Tool
Analyzes websites for SEO, AEO, GEO, performance, accessibility, and more using OpenAI API
"""

import os
import sys
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import openai
from dotenv import load_dotenv
from datetime import datetime, timedelta
import re
import time
import threading
from typing import Dict, List, Any, Optional
import base64
from io import BytesIO
import hashlib
import socket
import ssl
import whois
import dns.resolver
import textstat
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from spellchecker import SpellChecker
from langdetect import detect
import psutil

# Load environment variables
load_dotenv()

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

class AdvancedSEOAnalyzer:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_api_key:
            print("❌ Error: OPENAI_API_KEY not found in .env file")
            sys.exit(1)
        
        self.client = openai.OpenAI(api_key=self.openai_api_key)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Initialize NLP tools
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
            self.spell_checker = SpellChecker()
            self.stop_words = set(stopwords.words('english'))
        except:
            print("⚠️ Warning: Some NLP features may not work properly")
            self.sentiment_analyzer = None
            self.spell_checker = None
            self.stop_words = set()

    def fetch_comprehensive_website_data(self, url: str) -> Dict[str, Any]:
        """Fetch comprehensive website data with advanced analysis"""
        try:
            print(f"🔍 Fetching comprehensive website data from: {url}")
            
            # Start timing
            start_time = time.time()
            
            # Get basic response
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            fetch_time = time.time() - start_time
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract comprehensive data
            data = {
                'url': url,
                'domain': urlparse(url).netloc,
                'status_code': response.status_code,
                'content_length': len(response.content),
                'response_time': fetch_time,
                'headers': dict(response.headers),
                'encoding': response.encoding,
                'final_url': response.url,
                'redirects': len(response.history),
                
                # Basic SEO elements
                'title': soup.find('title').get_text().strip() if soup.find('title') else '',
                'meta_description': '',
                'meta_keywords': '',
                'canonical_url': '',
                'robots_meta': '',
                'viewport': '',
                'charset': '',
                
                # Content analysis
                'h1_tags': [h1.get_text().strip() for h1 in soup.find_all('h1')],
                'h2_tags': [h2.get_text().strip() for h2 in soup.find_all('h2')],
                'h3_tags': [h3.get_text().strip() for h3 in soup.find_all('h3')],
                'h4_tags': [h4.get_text().strip() for h4 in soup.find_all('h4')],
                'h5_tags': [h5.get_text().strip() for h5 in soup.find_all('h5')],
                'h6_tags': [h6.get_text().strip() for h6 in soup.find_all('h6')],
                
                # Images and media
                'images': [],
                'videos': [],
                'audio': [],
                
                # Links
                'internal_links': [],
                'external_links': [],
                'broken_links': [],
                
                # Technical elements
                'meta_tags': {},
                'structured_data': [],
                'css_files': [],
                'js_files': [],
                'forms': [],
                
                # Content
                'content': soup.get_text(),
                'html_content': str(soup),
                'word_count': 0,
                'sentences': [],
                'paragraphs': [],
                
                # Performance data
                'page_size': len(response.content),
                'compression': response.headers.get('content-encoding', ''),
                'cache_control': response.headers.get('cache-control', ''),
                'server': response.headers.get('server', ''),
                
                # Security
                'https': url.startswith('https'),
                'security_headers': {},
                
                # Social media
                'og_tags': {},
                'twitter_tags': {},
                
                # Language and accessibility
                'lang': soup.find('html', lang=True).get('lang', '') if soup.find('html', lang=True) else '',
                'alt_texts': [],
                'aria_labels': [],
                
                # Additional metadata
                'fetch_timestamp': datetime.now().isoformat(),
                'analysis_version': '2.0'
            }
            
            # Extract meta tags
            for meta in soup.find_all('meta'):
                name = meta.get('name', '').lower()
                property_attr = meta.get('property', '').lower()
                content = meta.get('content', '')
                
                if name == 'description':
                    data['meta_description'] = content
                elif name == 'keywords':
                    data['meta_keywords'] = content
                elif name == 'robots':
                    data['robots_meta'] = content
                elif name == 'viewport':
                    data['viewport'] = content
                elif property_attr.startswith('og:'):
                    data['og_tags'][property_attr] = content
                elif name.startswith('twitter:'):
                    data['twitter_tags'][name] = content
                elif name or property_attr:
                    data['meta_tags'][name or property_attr] = content
            
            # Extract canonical URL
            canonical = soup.find('link', rel='canonical')
            if canonical:
                data['canonical_url'] = canonical.get('href', '')
            
            # Extract charset
            charset_meta = soup.find('meta', charset=True)
            if charset_meta:
                data['charset'] = charset_meta.get('charset', '')
            
            # Extract images with detailed analysis
            for img in soup.find_all('img'):
                img_data = {
                    'src': img.get('src', ''),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', ''),
                    'width': img.get('width', ''),
                    'height': img.get('height', ''),
                    'loading': img.get('loading', ''),
                    'srcset': img.get('srcset', ''),
                    'sizes': img.get('sizes', ''),
                    'has_alt': bool(img.get('alt')),
                    'is_decorative': img.get('alt') == '',
                    'file_extension': self._get_file_extension(img.get('src', ''))
                }
                data['images'].append(img_data)
                if img_data['alt']:
                    data['alt_texts'].append(img_data['alt'])
            
            # Extract videos
            for video in soup.find_all(['video', 'iframe']):
                if video.name == 'video':
                    video_data = {
                        'src': video.get('src', ''),
                        'controls': video.has_attr('controls'),
                        'autoplay': video.has_attr('autoplay'),
                        'muted': video.has_attr('muted'),
                        'loop': video.has_attr('loop')
                    }
                else:  # iframe
                    src = video.get('src', '')
                    if any(platform in src for platform in ['youtube', 'vimeo', 'dailymotion']):
                        video_data = {
                            'src': src,
                            'platform': self._detect_video_platform(src),
                            'embedded': True
                        }
                    else:
                        continue
                data['videos'].append(video_data)
            
            # Extract links with analysis
            for link in soup.find_all('a', href=True):
                href = link['href']
                link_url = urljoin(url, href)
                link_domain = urlparse(link_url).netloc
                
                link_data = {
                    'url': link_url,
                    'text': link.get_text().strip(),
                    'title': link.get('title', ''),
                    'rel': link.get('rel', []),
                    'target': link.get('target', ''),
                    'is_internal': link_domain == data['domain'] or not link_domain,
                    'is_external': link_domain != data['domain'] and bool(link_domain),
                    'is_nofollow': 'nofollow' in link.get('rel', []),
                    'is_sponsored': 'sponsored' in link.get('rel', []),
                    'anchor_text_length': len(link.get_text().strip())
                }
                
                if link_data['is_internal']:
                    data['internal_links'].append(link_data)
                elif link_data['is_external']:
                    data['external_links'].append(link_data)
            
            # Extract CSS and JS files
            for css in soup.find_all('link', rel='stylesheet'):
                data['css_files'].append({
                    'href': css.get('href', ''),
                    'media': css.get('media', ''),
                    'type': css.get('type', '')
                })
            
            for script in soup.find_all('script', src=True):
                data['js_files'].append({
                    'src': script.get('src', ''),
                    'type': script.get('type', ''),
                    'async': script.has_attr('async'),
                    'defer': script.has_attr('defer')
                })
            
            # Extract forms
            for form in soup.find_all('form'):
                form_data = {
                    'action': form.get('action', ''),
                    'method': form.get('method', 'get').lower(),
                    'inputs': len(form.find_all('input')),
                    'has_labels': len(form.find_all('label')) > 0,
                    'has_fieldsets': len(form.find_all('fieldset')) > 0
                }
                data['forms'].append(form_data)
            
            # Extract structured data
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    structured = json.loads(script.string)
                    data['structured_data'].append(structured)
                except:
                    pass
            
            # Extract ARIA labels
            for element in soup.find_all(attrs={'aria-label': True}):
                data['aria_labels'].append(element.get('aria-label'))
            
            # Process content
            content_text = soup.get_text()
            data['content'] = content_text
            data['word_count'] = len(content_text.split())
            data['sentences'] = sent_tokenize(content_text) if content_text else []
            data['paragraphs'] = [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()]
            
            # Extract security headers
            security_headers = [
                'strict-transport-security', 'content-security-policy', 'x-frame-options',
                'x-content-type-options', 'x-xss-protection', 'referrer-policy'
            ]
            for header in security_headers:
                if header in response.headers:
                    data['security_headers'][header] = response.headers[header]
            
            return data
            
        except Exception as e:
            print(f"❌ Error fetching website data: {str(e)}")
            return None

    def analyze_technical_seo_advanced(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced technical SEO analysis"""
        analysis = {
            'score': 0,
            'max_score': 200,
            'issues': [],
            'warnings': [],
            'recommendations': [],
            'good_practices': [],
            'details': {},
            'categories': {
                'basic_seo': {'score': 0, 'max': 50},
                'performance': {'score': 0, 'max': 50},
                'accessibility': {'score': 0, 'max': 50},
                'security': {'score': 0, 'max': 50}
            }
        }
        
        # Basic SEO Analysis
        title = data.get('title', '')
        if not title:
            analysis['issues'].append('Missing page title')
        elif len(title) < 30:
            analysis['warnings'].append(f'Title too short ({len(title)} chars) - recommended 50-60 characters')
        elif len(title) > 60:
            analysis['warnings'].append(f'Title too long ({len(title)} chars) - recommended 50-60 characters')
        else:
            analysis['categories']['basic_seo']['score'] += 15
            analysis['good_practices'].append('Title length is optimal')
        
        # Meta description
        meta_desc = data.get('meta_description', '')
        if not meta_desc:
            analysis['issues'].append('Missing meta description')
        elif len(meta_desc) < 120:
            analysis['warnings'].append(f'Meta description too short ({len(meta_desc)} chars)')
        elif len(meta_desc) > 160:
            analysis['warnings'].append(f'Meta description too long ({len(meta_desc)} chars)')
        else:
            analysis['categories']['basic_seo']['score'] += 15
            analysis['good_practices'].append('Meta description length is optimal')
        
        # Heading structure
        h1_count = len(data.get('h1_tags', []))
        if h1_count == 0:
            analysis['issues'].append('Missing H1 tag')
        elif h1_count > 1:
            analysis['issues'].append(f'Multiple H1 tags found ({h1_count}) - should be unique')
        else:
            analysis['categories']['basic_seo']['score'] += 10
            analysis['good_practices'].append('Proper H1 tag structure')
        
        # Canonical URL
        if not data.get('canonical_url'):
            analysis['warnings'].append('Missing canonical URL')
        else:
            analysis['categories']['basic_seo']['score'] += 5
        
        # Robots meta
        if not data.get('robots_meta'):
            analysis['warnings'].append('Missing robots meta tag')
        else:
            analysis['categories']['basic_seo']['score'] += 5
        
        # Performance Analysis
        response_time = data.get('response_time', 0)
        if response_time > 3:
            analysis['issues'].append(f'Very slow response time: {response_time:.2f}s (should be < 1s)')
        elif response_time > 1:
            analysis['warnings'].append(f'Slow response time: {response_time:.2f}s (should be < 1s)')
        else:
            analysis['categories']['performance']['score'] += 20
            analysis['good_practices'].append('Fast response time')
        
        # Page size analysis
        page_size_mb = data.get('page_size', 0) / (1024 * 1024)
        if page_size_mb > 3:
            analysis['issues'].append(f'Large page size: {page_size_mb:.2f}MB (should be < 1MB)')
        elif page_size_mb > 1:
            analysis['warnings'].append(f'Page size could be optimized: {page_size_mb:.2f}MB')
        else:
            analysis['categories']['performance']['score'] += 15
        
        # Compression
        if not data.get('compression'):
            analysis['warnings'].append('No content compression detected')
        else:
            analysis['categories']['performance']['score'] += 10
            analysis['good_practices'].append('Content compression enabled')
        
        # Caching
        cache_control = data.get('cache_control', '')
        if not cache_control:
            analysis['warnings'].append('No cache control headers')
        else:
            analysis['categories']['performance']['score'] += 5
        
        # Accessibility Analysis
        images_without_alt = [img for img in data.get('images', []) if not img.get('has_alt')]
        if images_without_alt:
            analysis['issues'].append(f'{len(images_without_alt)} images missing alt text')
        else:
            analysis['categories']['accessibility']['score'] += 20
            analysis['good_practices'].append('All images have alt text')
        
        # Language declaration
        if not data.get('lang'):
            analysis['warnings'].append('Missing language declaration in HTML tag')
        else:
            analysis['categories']['accessibility']['score'] += 10
        
        # Forms accessibility
        forms_without_labels = [form for form in data.get('forms', []) if not form.get('has_labels')]
        if forms_without_labels and data.get('forms'):
            analysis['warnings'].append('Some forms may be missing proper labels')
        elif data.get('forms'):
            analysis['categories']['accessibility']['score'] += 10
        
        # ARIA labels
        if data.get('aria_labels'):
            analysis['categories']['accessibility']['score'] += 10
            analysis['good_practices'].append('ARIA labels found for better accessibility')
        
        # Security Analysis
        if not data.get('https'):
            analysis['issues'].append('Website not using HTTPS')
        else:
            analysis['categories']['security']['score'] += 20
            analysis['good_practices'].append('HTTPS enabled')
        
        # Security headers
        security_headers = data.get('security_headers', {})
        if 'strict-transport-security' in security_headers:
            analysis['categories']['security']['score'] += 10
        else:
            analysis['warnings'].append('Missing HSTS header')
        
        if 'content-security-policy' in security_headers:
            analysis['categories']['security']['score'] += 10
        else:
            analysis['warnings'].append('Missing Content Security Policy')
        
        if 'x-frame-options' in security_headers:
            analysis['categories']['security']['score'] += 5
        else:
            analysis['warnings'].append('Missing X-Frame-Options header')
        
        if 'x-content-type-options' in security_headers:
            analysis['categories']['security']['score'] += 5
        else:
            analysis['warnings'].append('Missing X-Content-Type-Options header')
        
        # Calculate total score
        total_score = sum(cat['score'] for cat in analysis['categories'].values())
        analysis['score'] = total_score
        
        # Detailed metrics
        analysis['details'] = {
            'title_length': len(title),
            'meta_description_length': len(meta_desc),
            'h1_count': h1_count,
            'h2_count': len(data.get('h2_tags', [])),
            'h3_count': len(data.get('h3_tags', [])),
            'total_images': len(data.get('images', [])),
            'images_without_alt': len(images_without_alt),
            'response_time': response_time,
            'page_size_mb': page_size_mb,
            'internal_links': len(data.get('internal_links', [])),
            'external_links': len(data.get('external_links', [])),
            'css_files': len(data.get('css_files', [])),
            'js_files': len(data.get('js_files', [])),
            'forms': len(data.get('forms', [])),
            'structured_data_items': len(data.get('structured_data', [])),
            'security_headers_count': len(security_headers),
            'redirects': data.get('redirects', 0)
        }
        
        return analysis

    def analyze_content_advanced(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Advanced content analysis with NLP"""
        analysis = {
            'score': 0,
            'max_score': 200,
            'issues': [],
            'warnings': [],
            'recommendations': [],
            'good_practices': [],
            'details': {},
            'categories': {
                'content_quality': {'score': 0, 'max': 50},
                'readability': {'score': 0, 'max': 50},
                'keyword_optimization': {'score': 0, 'max': 50},
                'semantic_analysis': {'score': 0, 'max': 50}
            }
        }
        
        content = data.get('content', '')
        word_count = len(content.split()) if content else 0
        
        # Content Quality Analysis
        if word_count < 300:
            analysis['issues'].append(f'Content too short ({word_count} words) - minimum 300 recommended')
        elif word_count < 500:
            analysis['warnings'].append(f'Content could be longer ({word_count} words) - 500+ recommended')
        elif word_count > 2000:
            analysis['categories']['content_quality']['score'] += 20
            analysis['good_practices'].append('Comprehensive content length')
        else:
            analysis['categories']['content_quality']['score'] += 15
        
        # Paragraph analysis
        paragraphs = data.get('paragraphs', [])
        if paragraphs:
            avg_paragraph_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
            if avg_paragraph_length > 100:
                analysis['warnings'].append('Paragraphs are too long - consider breaking them up')
            else:
                analysis['categories']['content_quality']['score'] += 10
        
        # Sentence analysis
        sentences = data.get('sentences', [])
        if sentences:
            avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
            if avg_sentence_length > 25:
                analysis['warnings'].append('Sentences are too long - consider shorter sentences')
            else:
                analysis['categories']['content_quality']['score'] += 10
        
        # Readability Analysis
        if content and len(content) > 100:
            try:
                flesch_score = textstat.flesch_reading_ease(content)
                flesch_grade = textstat.flesch_kincaid_grade(content)
                
                if flesch_score >= 60:
                    analysis['categories']['readability']['score'] += 20
                    analysis['good_practices'].append(f'Good readability score: {flesch_score:.1f}')
                elif flesch_score >= 30:
                    analysis['categories']['readability']['score'] += 10
                    analysis['warnings'].append(f'Moderate readability score: {flesch_score:.1f}')
                else:
                    analysis['warnings'].append(f'Poor readability score: {flesch_score:.1f}')
                
                if flesch_grade <= 8:
                    analysis['categories']['readability']['score'] += 15
                elif flesch_grade <= 12:
                    analysis['categories']['readability']['score'] += 10
                else:
                    analysis['warnings'].append(f'High reading grade level: {flesch_grade:.1f}')
                
                analysis['details']['flesch_reading_ease'] = flesch_score
                analysis['details']['flesch_kincaid_grade'] = flesch_grade
                
            except:
                analysis['warnings'].append('Could not calculate readability scores')
        
        # Language detection
        try:
            detected_lang = detect(content) if content else 'unknown'
            analysis['details']['detected_language'] = detected_lang
            if detected_lang != 'en' and data.get('lang', '').startswith('en'):
                analysis['warnings'].append(f'Language mismatch: declared English but detected {detected_lang}')
        except:
            analysis['details']['detected_language'] = 'unknown'
        
        # Keyword Analysis
        title_words = data.get('title', '').lower().split()
        if title_words and content:
            # Find potential main keywords from title
            main_keywords = [word for word in title_words if len(word) > 3 and word not in self.stop_words]
            
            if main_keywords:
                keyword_densities = {}
                for keyword in main_keywords[:3]:  # Analyze top 3 keywords
                    keyword_count = content.lower().count(keyword.lower())
                    density = (keyword_count / word_count * 100) if word_count > 0 else 0
                    keyword_densities[keyword] = {
                        'count': keyword_count,
                        'density': density
                    }
                    
                    if density < 0.5:
                        analysis['warnings'].append(f'Low keyword density for "{keyword}": {density:.1f}%')
                    elif density > 3:
                        analysis['warnings'].append(f'High keyword density for "{keyword}": {density:.1f}% (may be over-optimization)')
                    else:
                        analysis['categories']['keyword_optimization']['score'] += 10
                
                analysis['details']['keyword_densities'] = keyword_densities
        
        # Semantic Analysis with NLP
        if self.sentiment_analyzer and content:
            try:
                sentiment_scores = self.sentiment_analyzer.polarity_scores(content)
                analysis['details']['sentiment'] = sentiment_scores
                
                if sentiment_scores['compound'] >= 0.1:
                    analysis['categories']['semantic_analysis']['score'] += 15
                    analysis['good_practices'].append('Positive content sentiment')
                elif sentiment_scores['compound'] <= -0.1:
                    analysis['warnings'].append('Negative content sentiment detected')
                else:
                    analysis['categories']['semantic_analysis']['score'] += 10
                    
            except:
                pass
        
        # Spelling check (sample)
        if self.spell_checker and content:
            try:
                words = word_tokenize(content.lower())
                words = [word for word in words if word.isalpha() and len(word) > 2]
                misspelled = self.spell_checker.unknown(words[:100])  # Check first 100 words
                
                if len(misspelled) > 5:
                    analysis['warnings'].append(f'Potential spelling issues detected ({len(misspelled)} words)')
                elif len(misspelled) == 0:
                    analysis['categories']['semantic_analysis']['score'] += 10
                    analysis['good_practices'].append('No spelling issues detected')
                
                analysis['details']['potential_misspellings'] = list(misspelled)[:10]
            except:
                pass
        
        # Content structure analysis
        headings_text = ' '.join(data.get('h1_tags', []) + data.get('h2_tags', []) + data.get('h3_tags', []))
        if headings_text and content:
            heading_word_ratio = len(headings_text.split()) / word_count if word_count > 0 else 0
            if heading_word_ratio < 0.02:
                analysis['warnings'].append('Content may lack proper heading structure')
            else:
                analysis['categories']['content_quality']['score'] += 10
        
        # Calculate total score
        total_score = sum(cat['score'] for cat in analysis['categories'].values())
        analysis['score'] = total_score
        
        # Additional details
        analysis['details'].update({
            'word_count': word_count,
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'avg_sentence_length': sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0,
            'avg_paragraph_length': sum(len(p.split()) for p in paragraphs) / len(paragraphs) if paragraphs else 0,
            'content_to_code_ratio': len(content) / len(data.get('html_content', '')) if data.get('html_content') else 0
        })
        
        return analysis

    def analyze_performance_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance metrics"""
        analysis = {
            'score': 0,
            'max_score': 100,
            'issues': [],
            'warnings': [],
            'recommendations': [],
            'good_practices': [],
            'details': {},
            'metrics': {}
        }
        
        # Response time analysis
        response_time = data.get('response_time', 0)
        if response_time <= 0.5:
            analysis['score'] += 25
            analysis['good_practices'].append('Excellent response time')
        elif response_time <= 1.0:
            analysis['score'] += 20
            analysis['good_practices'].append('Good response time')
        elif response_time <= 2.0:
            analysis['score'] += 10
            analysis['warnings'].append('Response time could be improved')
        else:
            analysis['issues'].append('Poor response time - needs optimization')
        
        # Page size analysis
        page_size = data.get('page_size', 0)
        page_size_mb = page_size / (1024 * 1024)
        
        if page_size_mb <= 0.5:
            analysis['score'] += 20
            analysis['good_practices'].append('Optimal page size')
        elif page_size_mb <= 1.0:
            analysis['score'] += 15
        elif page_size_mb <= 2.0:
            analysis['score'] += 10
            analysis['warnings'].append('Page size could be optimized')
        else:
            analysis['issues'].append('Large page size - consider optimization')
        
        # Resource analysis
        css_count = len(data.get('css_files', []))
        js_count = len(data.get('js_files', []))
        image_count = len(data.get('images', []))
        
        if css_count <= 3:
            analysis['score'] += 10
        elif css_count <= 6:
            analysis['score'] += 5
        else:
            analysis['warnings'].append(f'Many CSS files ({css_count}) - consider combining')
        
        if js_count <= 5:
            analysis['score'] += 10
        elif js_count <= 10:
            analysis['score'] += 5
        else:
            analysis['warnings'].append(f'Many JavaScript files ({js_count}) - consider combining')
        
        # Compression check
        if data.get('compression'):
            analysis['score'] += 15
            analysis['good_practices'].append('Content compression enabled')
        else:
            analysis['warnings'].append('Enable content compression (gzip/brotli)')
        
        # Caching analysis
        cache_control = data.get('cache_control', '')
        if 'max-age' in cache_control or 'public' in cache_control:
            analysis['score'] += 10
            analysis['good_practices'].append('Caching headers configured')
        else:
            analysis['warnings'].append('Configure caching headers for better performance')
        
        # CDN detection (basic)
        server = data.get('server', '').lower()
        cdn_indicators = ['cloudflare', 'cloudfront', 'fastly', 'maxcdn', 'keycdn']
        if any(cdn in server for cdn in cdn_indicators):
            analysis['score'] += 10
            analysis['good_practices'].append('CDN detected')
        
        analysis['metrics'] = {
            'response_time_ms': response_time * 1000,
            'page_size_kb': page_size / 1024,
            'css_files': css_count,
            'js_files': js_count,
            'image_count': image_count,
            'compression_enabled': bool(data.get('compression')),
            'https_enabled': data.get('https', False)
        }
        
        return analysis

    def analyze_domain_authority(self, domain: str) -> Dict[str, Any]:
        """Analyze domain authority and technical details"""
        analysis = {
            'domain_info': {},
            'dns_info': {},
            'ssl_info': {},
            'whois_info': {},
            'issues': [],
            'recommendations': []
        }
        
        try:
            # DNS Analysis
            try:
                # A record
                a_records = dns.resolver.resolve(domain, 'A')
                analysis['dns_info']['a_records'] = [str(record) for record in a_records]
                
                # MX records
                try:
                    mx_records = dns.resolver.resolve(domain, 'MX')
                    analysis['dns_info']['mx_records'] = [str(record) for record in mx_records]
                except:
                    analysis['dns_info']['mx_records'] = []
                
                # NS records
                try:
                    ns_records = dns.resolver.resolve(domain, 'NS')
                    analysis['dns_info']['ns_records'] = [str(record) for record in ns_records]
                except:
                    analysis['dns_info']['ns_records'] = []
                
            except Exception as e:
                analysis['issues'].append(f'DNS resolution failed: {str(e)}')
            
            # SSL Certificate Analysis
            try:
                context = ssl.create_default_context()
                with socket.create_connection((domain, 443), timeout=10) as sock:
                    with context.wrap_socket(sock, server_hostname=domain) as ssock:
                        cert = ssock.getpeercert()
                        analysis['ssl_info'] = {
                            'subject': dict(x[0] for x in cert['subject']),
                            'issuer': dict(x[0] for x in cert['issuer']),
                            'version': cert['version'],
                            'serial_number': cert['serialNumber'],
                            'not_before': cert['notBefore'],
                            'not_after': cert['notAfter'],
                            'san': cert.get('subjectAltName', [])
                        }
            except Exception as e:
                analysis['issues'].append(f'SSL analysis failed: {str(e)}')
            
            # WHOIS Information
            try:
                w = whois.whois(domain)
                if w:
                    analysis['whois_info'] = {
                        'domain_name': w.domain_name,
                        'registrar': w.registrar,
                        'creation_date': str(w.creation_date) if w.creation_date else None,
                        'expiration_date': str(w.expiration_date) if w.expiration_date else None,
                        'name_servers': w.name_servers if w.name_servers else [],
                        'status': w.status if w.status else []
                    }
            except Exception as e:
                analysis['issues'].append(f'WHOIS lookup failed: {str(e)}')
        
        except Exception as e:
            analysis['issues'].append(f'Domain analysis failed: {str(e)}')
        
        return analysis

    def get_comprehensive_ai_recommendations(self, data: Dict[str, Any], technical_analysis: Dict, content_analysis: Dict, performance_analysis: Dict) -> str:
        """Get comprehensive AI recommendations"""
        try:
            # Prepare comprehensive data for AI analysis
            prompt = f"""
            Analyze this comprehensive website data and provide detailed SEO, AEO, and GEO recommendations:

            WEBSITE OVERVIEW:
            - URL: {data.get('url', '')}
            - Domain: {data.get('domain', '')}
            - Title: {data.get('title', '')} ({len(data.get('title', ''))} chars)
            - Meta Description: {data.get('meta_description', '')} ({len(data.get('meta_description', ''))} chars)
            - Word Count: {content_analysis['details'].get('word_count', 0)}
            - Language: {data.get('lang', 'not specified')}

            TECHNICAL SEO SCORES:
            - Overall Technical Score: {technical_analysis['score']}/{technical_analysis['max_score']}
            - Basic SEO: {technical_analysis['categories']['basic_seo']['score']}/{technical_analysis['categories']['basic_seo']['max']}
            - Performance: {technical_analysis['categories']['performance']['score']}/{technical_analysis['categories']['performance']['max']}
            - Accessibility: {technical_analysis['categories']['accessibility']['score']}/{technical_analysis['categories']['accessibility']['max']}
            - Security: {technical_analysis['categories']['security']['score']}/{technical_analysis['categories']['security']['max']}

            CONTENT ANALYSIS SCORES:
            - Overall Content Score: {content_analysis['score']}/{content_analysis['max_score']}
            - Content Quality: {content_analysis['categories']['content_quality']['score']}/{content_analysis['categories']['content_quality']['max']}
            - Readability: {content_analysis['categories']['readability']['score']}/{content_analysis['categories']['readability']['max']}
            - Keyword Optimization: {content_analysis['categories']['keyword_optimization']['score']}/{content_analysis['categories']['keyword_optimization']['max']}
            - Semantic Analysis: {content_analysis['categories']['semantic_analysis']['score']}/{content_analysis['categories']['semantic_analysis']['max']}

            PERFORMANCE METRICS:
            - Response Time: {data.get('response_time', 0):.2f}s
            - Page Size: {data.get('page_size', 0) / 1024:.1f}KB
            - Images: {len(data.get('images', []))} total, {len([img for img in data.get('images', []) if not img.get('has_alt')])} without alt text
            - CSS Files: {len(data.get('css_files', []))}
            - JS Files: {len(data.get('js_files', []))}

            CRITICAL ISSUES:
            {chr(10).join('- ' + issue for issue in technical_analysis.get('issues', []) + content_analysis.get('issues', []))}

            WARNINGS:
            {chr(10).join('- ' + warning for warning in technical_analysis.get('warnings', []) + content_analysis.get('warnings', []))}

            CURRENT GOOD PRACTICES:
            {chr(10).join('- ' + practice for practice in technical_analysis.get('good_practices', []) + content_analysis.get('good_practices', []))}

            Please provide comprehensive, actionable recommendations in the following categories:

            1. CRITICAL FIXES (High Priority - Fix Immediately)
            2. SEO OPTIMIZATION (Traditional Search Engine Optimization)
            3. AEO OPTIMIZATION (Answer Engine Optimization for voice search, featured snippets, AI assistants)
            4. GEO OPTIMIZATION (Generative Engine Optimization for ChatGPT, Bard, Claude, etc.)
            5. PERFORMANCE IMPROVEMENTS
            6. ACCESSIBILITY ENHANCEMENTS
            7. SECURITY HARDENING
            8. CONTENT STRATEGY
            9. TECHNICAL IMPROVEMENTS
            10. MONITORING & MAINTENANCE

            For each category, provide:
            - Specific, actionable recommendations
            - Expected impact (High/Medium/Low)
            - Implementation difficulty (Easy/Medium/Hard)
            - Estimated timeframe
            - Tools or resources needed

            Focus on modern SEO best practices, Core Web Vitals, E-A-T signals, and preparing for the future of AI-powered search.
            """
            
            print("🤖 Getting comprehensive AI-powered recommendations...")
            
            response = self.client.chat.completions.create(
                model="gpt-4",  # Use GPT-4 for better analysis
                messages=[
                    {"role": "system", "content": "You are a world-class SEO expert with deep knowledge of traditional SEO, AEO (Answer Engine Optimization), GEO (Generative Engine Optimization), web performance, accessibility, and modern search engine algorithms. Provide detailed, actionable, and prioritized recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️ Warning: Could not get OpenAI recommendations: {str(e)}")
            return self._get_fallback_recommendations(technical_analysis, content_analysis, performance_analysis)

    def _get_fallback_recommendations(self, technical_analysis: Dict, content_analysis: Dict, performance_analysis: Dict) -> str:
        """Fallback recommendations when AI is unavailable"""
        return """
        # COMPREHENSIVE SEO RECOMMENDATIONS

        ## 🚨 CRITICAL FIXES (High Priority)
        - Fix all critical technical issues identified in the analysis
        - Ensure HTTPS is properly implemented
        - Optimize page loading speed to under 2 seconds
        - Fix missing or poorly optimized meta tags

        ## 🔍 SEO OPTIMIZATION (Traditional Search)
        - Optimize title tags (50-60 characters with primary keywords)
        - Write compelling meta descriptions (150-160 characters)
        - Implement proper heading hierarchy (H1, H2, H3)
        - Add alt text to all images
        - Improve internal linking structure
        - Create XML sitemap and submit to search engines

        ## 🎯 AEO OPTIMIZATION (Answer Engine Optimization)
        - Structure content for featured snippets
        - Add comprehensive FAQ sections
        - Optimize for voice search with conversational keywords
        - Implement structured data markup (Schema.org)
        - Create "People Also Ask" style content
        - Optimize for local search if applicable

        ## 🤖 GEO OPTIMIZATION (Generative Engine Optimization)
        - Create authoritative, well-sourced content
        - Use clear entity definitions and relationships
        - Implement comprehensive topic coverage
        - Add factual accuracy and citations
        - Structure content for AI understanding
        - Build topical authority through content clusters

        ## ⚡ PERFORMANCE IMPROVEMENTS
        - Optimize images (WebP format, proper sizing)
        - Minify CSS and JavaScript files
        - Enable compression (gzip/brotli)
        - Implement browser caching
        - Use a Content Delivery Network (CDN)
        - Optimize Core Web Vitals (LCP, FID, CLS)

        ## ♿ ACCESSIBILITY ENHANCEMENTS
        - Add alt text to all images
        - Ensure proper color contrast ratios
        - Implement keyboard navigation
        - Add ARIA labels where needed
        - Use semantic HTML elements
        - Test with screen readers

        ## 🔒 SECURITY HARDENING
        - Implement security headers (HSTS, CSP, X-Frame-Options)
        - Keep software and plugins updated
        - Use strong SSL/TLS configuration
        - Implement proper authentication
        - Regular security audits
        - Backup strategy

        ## 📝 CONTENT STRATEGY
        - Increase content depth and quality
        - Target long-tail keywords
        - Create pillar pages and topic clusters
        - Regular content updates and freshness
        - User-generated content integration
        - Multi-media content (videos, infographics)

        ## 🔧 TECHNICAL IMPROVEMENTS
        - Implement proper redirects (301 for permanent)
        - Fix broken links and 404 errors
        - Optimize URL structure
        - Implement breadcrumb navigation
        - Mobile-first responsive design
        - Progressive Web App features

        ## 📊 MONITORING & MAINTENANCE
        - Set up Google Search Console and Analytics
        - Regular SEO audits and monitoring
        - Track keyword rankings and traffic
        - Monitor Core Web Vitals
        - Competitor analysis
        - Regular content audits and updates
        """

    def _get_file_extension(self, url: str) -> str:
        """Get file extension from URL"""
        try:
            return url.split('.')[-1].lower() if '.' in url else ''
        except:
            return ''

    def _detect_video_platform(self, url: str) -> str:
        """Detect video platform from URL"""
        if 'youtube' in url:
            return 'YouTube'
        elif 'vimeo' in url:
            return 'Vimeo'
        elif 'dailymotion' in url:
            return 'Dailymotion'
        else:
            return 'Unknown'

    def generate_advanced_html_report(self, data: Dict[str, Any], technical_analysis: Dict, content_analysis: Dict, performance_analysis: Dict, domain_analysis: Dict, ai_recommendations: str) -> str:
        """Generate advanced HTML report with charts and detailed analysis"""
        
        # Calculate overall scores
        technical_score = (technical_analysis['score'] / technical_analysis['max_score']) * 100
        content_score = (content_analysis['score'] / content_analysis['max_score']) * 100
        performance_score = performance_analysis['score']
        overall_score = (technical_score + content_score + performance_score) / 3
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate performance chart data
        performance_data = {
            'Technical SEO': technical_score,
            'Content Quality': content_score,
            'Performance': performance_score,
            'Accessibility': (technical_analysis['categories']['accessibility']['score'] / technical_analysis['categories']['accessibility']['max']) * 100,
            'Security': (technical_analysis['categories']['security']['score'] / technical_analysis['categories']['security']['max']) * 100
        }
        
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced SEO Analysis Report - {data.get('domain', '')}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
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
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            animation: slideDown 0.8s ease-out;
            text-align: center;
        }}
        
        .header h1 {{
            color: #2b59ff;
            font-size: 3em;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 1.2em;
            margin-bottom: 20px;
        }}
        
        .header .url {{
            color: #2b59ff;
            font-size: 1.4em;
            font-weight: 600;
            margin-bottom: 30px;
        }}
        
        .score-dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .score-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }}
        
        .score-card:hover {{
            transform: translateY(-5px);
        }}
        
        .score-circle {{
            width: 100px;
            height: 100px;
            border-radius: 50%;
            margin: 0 auto 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            font-weight: bold;
            color: white;
            position: relative;
        }}
        
        .score-excellent {{ background: conic-gradient(#4caf50 var(--percentage), #e0e0e0 0deg); }}
        .score-good {{ background: conic-gradient(#8bc34a var(--percentage), #e0e0e0 0deg); }}
        .score-average {{ background: conic-gradient(#ff9800 var(--percentage), #e0e0e0 0deg); }}
        .score-poor {{ background: conic-gradient(#f44336 var(--percentage), #e0e0e0 0deg); }}
        
        .score-inner {{
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: white;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
        }}
        
        .report-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
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
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .card-icon {{
            width: 50px;
            height: 50px;
            border-radius: 12px;
            background: linear-gradient(135deg, #2b59ff, #1a4bff);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 20px;
            color: white;
            font-size: 1.5em;
        }}
        
        .card-title {{
            font-size: 1.8em;
            color: #2b59ff;
            font-weight: 600;
        }}
        
        .metric {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 0;
            border-bottom: 1px solid #f5f5f5;
        }}
        
        .metric:last-child {{
            border-bottom: none;
        }}
        
        .metric-label {{
            color: #666;
            font-weight: 500;
        }}
        
        .metric-value {{
            font-weight: 600;
            color: #333;
        }}
        
        .status-excellent {{ color: #4caf50; }}
        .status-good {{ color: #8bc34a; }}
        .status-warning {{ color: #ff9800; }}
        .status-error {{ color: #f44336; }}
        
        .issues-section {{
            margin: 20px 0;
        }}
        
        .issues-list {{
            list-style: none;
            margin: 15px 0;
        }}
        
        .issues-list li {{
            padding: 10px 15px;
            margin: 8px 0;
            border-radius: 8px;
            position: relative;
            padding-left: 45px;
        }}
        
        .issue-critical {{
            background: #ffebee;
            border-left: 4px solid #f44336;
            color: #c62828;
        }}
        
        .issue-warning {{
            background: #fff3e0;
            border-left: 4px solid #ff9800;
            color: #ef6c00;
        }}
        
        .issue-good {{
            background: #e8f5e8;
            border-left: 4px solid #4caf50;
            color: #2e7d32;
        }}
        
        .issue-critical:before {{ content: "🚨"; position: absolute; left: 15px; }}
        .issue-warning:before {{ content: "⚠️"; position: absolute; left: 15px; }}
        .issue-good:before {{ content: "✅"; position: absolute; left: 15px; }}
        
        .chart-container {{
            background: white;
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        }}
        
        .recommendations {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            animation: slideUp 0.8s ease-out 0.2s both;
            margin: 30px 0;
        }}
        
        .recommendations h2 {{
            color: #2b59ff;
            margin-bottom: 25px;
            font-size: 2.2em;
            text-align: center;
        }}
        
        .ai-content {{
            line-height: 1.8;
            color: #444;
            white-space: pre-wrap;
            font-size: 1.1em;
        }}
        
        .tabs {{
            display: flex;
            background: #f8f9fa;
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 20px;
        }}
        
        .tab {{
            flex: 1;
            padding: 12px 20px;
            text-align: center;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }}
        
        .tab.active {{
            background: #2b59ff;
            color: white;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 10px;
            background: #e0e0e0;
            border-radius: 5px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            border-radius: 5px;
            transition: width 1.5s ease-out;
        }}
        
        .footer {{
            text-align: center;
            color: rgba(255, 255, 255, 0.9);
            margin-top: 50px;
            padding: 30px;
            font-size: 1.1em;
        }}
        
        @keyframes slideDown {{
            from {{ opacity: 0; transform: translateY(-50px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes slideUp {{
            from {{ opacity: 0; transform: translateY(50px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @media (max-width: 768px) {{
            .container {{ padding: 10px; }}
            .header h1 {{ font-size: 2em; }}
            .report-grid {{ grid-template-columns: 1fr; }}
            .score-dashboard {{ grid-template-columns: repeat(2, 1fr); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Advanced SEO Analysis Report</h1>
            <div class="subtitle">Comprehensive Website Analysis & Optimization Recommendations</div>
            <div class="url">{data.get('url', '')}</div>
            
            <div class="score-dashboard">
                <div class="score-card">
                    <div class="score-circle score-{'excellent' if overall_score >= 80 else 'good' if overall_score >= 60 else 'average' if overall_score >= 40 else 'poor'}" style="--percentage: {overall_score * 3.6}deg;">
                        <div class="score-inner">{overall_score:.0f}</div>
                    </div>
                    <h3>Overall Score</h3>
                </div>
                <div class="score-card">
                    <div class="score-circle score-{'excellent' if technical_score >= 80 else 'good' if technical_score >= 60 else 'average' if technical_score >= 40 else 'poor'}" style="--percentage: {technical_score * 3.6}deg;">
                        <div class="score-inner">{technical_score:.0f}</div>
                    </div>
                    <h3>Technical SEO</h3>
                </div>
                <div class="score-card">
                    <div class="score-circle score-{'excellent' if content_score >= 80 else 'good' if content_score >= 60 else 'average' if content_score >= 40 else 'poor'}" style="--percentage: {content_score * 3.6}deg;">
                        <div class="score-inner">{content_score:.0f}</div>
                    </div>
                    <h3>Content Quality</h3>
                </div>
                <div class="score-card">
                    <div class="score-circle score-{'excellent' if performance_score >= 80 else 'good' if performance_score >= 60 else 'average' if performance_score >= 40 else 'poor'}" style="--percentage: {performance_score * 3.6}deg;">
                        <div class="score-inner">{performance_score:.0f}</div>
                    </div>
                    <h3>Performance</h3>
                </div>
            </div>
            
            <div style="color: #666; margin-top: 20px;">
                Generated on {timestamp} | Analysis Version 2.0
            </div>
        </div>
        
        <div class="chart-container">
            <h2 style="color: #2b59ff; margin-bottom: 20px;">📊 Performance Overview</h2>
            <canvas id="performanceChart" width="400" height="200"></canvas>
        </div>
        
        <div class="report-grid">
            <div class="report-card">
                <div class="card-header">
                    <div class="card-icon">🔧</div>
                    <div class="card-title">Technical SEO Analysis</div>
                </div>
                
                <div class="tabs">
                    <div class="tab active" onclick="showTab('technical-basic')">Basic</div>
                    <div class="tab" onclick="showTab('technical-performance')">Performance</div>
                    <div class="tab" onclick="showTab('technical-security')">Security</div>
                </div>
                
                <div id="technical-basic" class="tab-content active">
                    <div class="metric">
                        <span class="metric-label">Title Length</span>
                        <span class="metric-value status-{'good' if 30 <= len(data.get('title', '')) <= 60 else 'warning'}">{len(data.get('title', ''))} chars</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Meta Description</span>
                        <span class="metric-value status-{'good' if 120 <= len(data.get('meta_description', '')) <= 160 else 'warning'}">{len(data.get('meta_description', ''))} chars</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">H1 Tags</span>
                        <span class="metric-value status-{'good' if len(data.get('h1_tags', [])) == 1 else 'warning'}">{len(data.get('h1_tags', []))}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Canonical URL</span>
                        <span class="metric-value status-{'good' if data.get('canonical_url') else 'warning'}">{'Set' if data.get('canonical_url') else 'Missing'}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Structured Data</span>
                        <span class="metric-value">{len(data.get('structured_data', []))} items</span>
                    </div>
                </div>
                
                <div id="technical-performance" class="tab-content">
                    <div class="metric">
                        <span class="metric-label">Response Time</span>
                        <span class="metric-value status-{'excellent' if data.get('response_time', 0) < 1 else 'good' if data.get('response_time', 0) < 2 else 'warning'}">{data.get('response_time', 0):.2f}s</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Page Size</span>
                        <span class="metric-value">{data.get('page_size', 0) / 1024:.1f} KB</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Compression</span>
                        <span class="metric-value status-{'good' if data.get('compression') else 'warning'}">{'Enabled' if data.get('compression') else 'Disabled'}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">CSS Files</span>
                        <span class="metric-value">{len(data.get('css_files', []))}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">JS Files</span>
                        <span class="metric-value">{len(data.get('js_files', []))}</span>
                    </div>
                </div>
                
                <div id="technical-security" class="tab-content">
                    <div class="metric">
                        <span class="metric-label">HTTPS</span>
                        <span class="metric-value status-{'good' if data.get('https') else 'error'}">{'Enabled' if data.get('https') else 'Disabled'}</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Security Headers</span>
                        <span class="metric-value">{len(data.get('security_headers', {}))}/6</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Redirects</span>
                        <span class="metric-value">{data.get('redirects', 0)}</span>
                    </div>
                </div>
            </div>
            
            <div class="report-card">
                <div class="card-header">
                    <div class="card-icon">📝</div>
                    <div class="card-title">Content Analysis</div>
                </div>
                
                <div class="metric">
                    <span class="metric-label">Word Count</span>
                    <span class="metric-value status-{'good' if content_analysis['details'].get('word_count', 0) >= 300 else 'warning'}">{content_analysis['details'].get('word_count', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Readability Score</span>
                    <span class="metric-value">{content_analysis['details'].get('flesch_reading_ease', 'N/A')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Language</span>
                    <span class="metric-value">{content_analysis['details'].get('detected_language', 'Unknown')}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Internal Links</span>
                    <span class="metric-value">{len(data.get('internal_links', []))}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">External Links</span>
                    <span class="metric-value">{len(data.get('external_links', []))}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Images</span>
                    <span class="metric-value">{len(data.get('images', []))}</span>
                </div>
            </div>
            
            <div class="report-card">
                <div class="card-header">
                    <div class="card-icon">⚡</div>
                    <div class="card-title">Performance Metrics</div>
                </div>
                
                <div class="metric">
                    <span class="metric-label">Load Time</span>
                    <span class="metric-value">{performance_analysis['metrics'].get('response_time_ms', 0):.0f}ms</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Page Weight</span>
                    <span class="metric-value">{performance_analysis['metrics'].get('page_size_kb', 0):.1f}KB</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Resource Count</span>
                    <span class="metric-value">{performance_analysis['metrics'].get('css_files', 0) + performance_analysis['metrics'].get('js_files', 0)}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Image Optimization</span>
                    <span class="metric-value status-{'good' if len([img for img in data.get('images', []) if not img.get('has_alt')]) == 0 else 'warning'}">{len([img for img in data.get('images', []) if img.get('has_alt')])}/{len(data.get('images', []))}</span>
                </div>
            </div>
            
            <div class="report-card">
                <div class="card-header">
                    <div class="card-icon">🎯</div>
                    <div class="card-title">Issues & Recommendations</div>
                </div>
                
                <div class="issues-section">
                    <h4>Critical Issues</h4>
                    <ul class="issues-list">
                        {"".join([f'<li class="issue-critical">{issue}</li>' for issue in technical_analysis.get('issues', []) + content_analysis.get('issues', [])])}
                        {f'<li class="issue-good">No critical issues found!</li>' if not (technical_analysis.get('issues', []) + content_analysis.get('issues', [])) else ''}
                    </ul>
                </div>
                
                <div class="issues-section">
                    <h4>Warnings</h4>
                    <ul class="issues-list">
                        {"".join([f'<li class="issue-warning">{warning}</li>' for warning in technical_analysis.get('warnings', []) + content_analysis.get('warnings', [])])}
                        {f'<li class="issue-good">No warnings!</li>' if not (technical_analysis.get('warnings', []) + content_analysis.get('warnings', [])) else ''}
                    </ul>
                </div>
                
                <div class="issues-section">
                    <h4>Good Practices</h4>
                    <ul class="issues-list">
                        {"".join([f'<li class="issue-good">{practice}</li>' for practice in technical_analysis.get('good_practices', []) + content_analysis.get('good_practices', [])])}
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="recommendations">
            <h2>🤖 AI-Powered Comprehensive Recommendations</h2>
            <div class="ai-content">{ai_recommendations}</div>
        </div>
        
        <div class="footer">
            <p>🚀 Advanced SEO Analysis Report • Powered by OpenAI GPT-4 • Generated with ❤️</p>
            <p>For best results, implement recommendations in order of priority and re-analyze monthly</p>
        </div>
    </div>
    
    <script>
        // Performance Chart
        const ctx = document.getElementById('performanceChart').getContext('2d');
        new Chart(ctx, {{
            type: 'radar',
            data: {{
                labels: {list(performance_data.keys())},
                datasets: [{{
                    label: 'Current Performance',
                    data: {list(performance_data.values())},
                    backgroundColor: 'rgba(43, 89, 255, 0.2)',
                    borderColor: 'rgba(43, 89, 255, 1)',
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(43, 89, 255, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(43, 89, 255, 1)'
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    r: {{
                        beginAtZero: true,
                        max: 100,
                        ticks: {{
                            stepSize: 20
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
        
        // Tab functionality
        function showTab(tabId) {{
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(content => {{
                content.classList.remove('active');
            }});
            
            // Remove active class from all tabs
            document.querySelectorAll('.tab').forEach(tab => {{
                tab.classList.remove('active');
            }});
            
            // Show selected tab content
            document.getElementById(tabId).classList.add('active');
            
            // Add active class to clicked tab
            event.target.classList.add('active');
        }}
        
        // Animate progress bars on load
        window.addEventListener('load', function() {{
            document.querySelectorAll('.progress-fill').forEach(bar => {{
                const width = bar.getAttribute('data-width');
                bar.style.width = width + '%';
            }});
        }});
    </script>
</body>
</html>
        """
        
        return html_template

    def run_comprehensive_analysis(self, url: str):
        """Run comprehensive SEO analysis"""
        print(f"\n🚀 Starting comprehensive SEO analysis for: {url}")
        print("=" * 80)
        
        # Fetch comprehensive website data
        data = self.fetch_comprehensive_website_data(url)
        if not data:
            return
        
        print("✅ Website data fetched successfully")
        
        # Run advanced technical SEO analysis
        print("🔧 Analyzing advanced technical SEO...")
        technical_analysis = self.analyze_technical_seo_advanced(data)
        
        # Run advanced content analysis
        print("📝 Analyzing content with NLP...")
        content_analysis = self.analyze_content_advanced(data)
        
        # Run performance analysis
        print("⚡ Analyzing performance metrics...")
        performance_analysis = self.analyze_performance_metrics(data)
        
        # Run domain analysis
        print("🌐 Analyzing domain authority...")
        domain_analysis = self.analyze_domain_authority(data['domain'])
        
        # Get comprehensive AI recommendations
        ai_recommendations = self.get_comprehensive_ai_recommendations(
            data, technical_analysis, content_analysis, performance_analysis
        )
        
        # Generate advanced HTML report
        print("📊 Generating advanced HTML report...")
        html_report = self.generate_advanced_html_report(
            data, technical_analysis, content_analysis, performance_analysis, domain_analysis, ai_recommendations
        )
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = urlparse(url).netloc.replace('www.', '')
        filename = f"advanced_seo_report_{domain}_{timestamp}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        # Print summary
        technical_score = (technical_analysis['score'] / technical_analysis['max_score']) * 100
        content_score = (content_analysis['score'] / content_analysis['max_score']) * 100
        overall_score = (technical_score + content_score + performance_analysis['score']) / 3
        
        print(f"\n📊 ANALYSIS SUMMARY")
        print("=" * 50)
        print(f"🎯 Overall Score: {overall_score:.1f}/100")
        print(f"🔧 Technical SEO: {technical_score:.1f}/100")
        print(f"📝 Content Quality: {content_score:.1f}/100")
        print(f"⚡ Performance: {performance_analysis['score']}/100")
        print(f"\n🚨 Critical Issues: {len(technical_analysis.get('issues', []) + content_analysis.get('issues', []))}")
        print(f"⚠️  Warnings: {len(technical_analysis.get('warnings', []) + content_analysis.get('warnings', []))}")
        print(f"✅ Good Practices: {len(technical_analysis.get('good_practices', []) + content_analysis.get('good_practices', []))}")
        
        print(f"\n✅ Advanced report saved as: {filename}")
        print(f"🌐 Open the file in your browser to view the comprehensive analysis")
        print("=" * 80)

def main():
    """Main function"""
    print("🔍 Advanced SEO Analysis Tool v2.0")
    print("=" * 50)
    
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
    analyzer = AdvancedSEOAnalyzer()
    analyzer.run_comprehensive_analysis(url)

if __name__ == "__main__":
    main()