#!/usr/bin/env python3
"""
Comprehensive Keyword Analysis Tool
Analyzes keywords, generates insights, and provides SEO recommendations
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
from typing import Dict, List, Any, Optional, Tuple
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import textstat
from langdetect import detect
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

class KeywordAnalyzer:
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
            self.stop_words = set(stopwords.words('english'))
        except:
            print("⚠️ Warning: Some NLP features may not work properly")
            self.sentiment_analyzer = None
            self.stop_words = set()

    def analyze_url_keywords(self, url: str) -> Dict[str, Any]:
        """Analyze keywords from a specific URL"""
        try:
            print(f"🔍 Analyzing keywords from URL: {url}")
            
            # Fetch webpage content
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text content
            text_content = self._extract_text_content(soup)
            
            # Extract metadata
            metadata = self._extract_metadata(soup)
            
            # Perform keyword analysis
            keyword_analysis = self._analyze_keywords(text_content, metadata)
            
            # Add URL-specific data
            keyword_analysis['url'] = url
            keyword_analysis['domain'] = urlparse(url).netloc
            keyword_analysis['analysis_date'] = datetime.now().isoformat()
            
            return keyword_analysis
            
        except Exception as e:
            print(f"❌ Error analyzing URL {url}: {str(e)}")
            return {'error': str(e), 'url': url}

    def analyze_text_keywords(self, text: str, title: str = "", description: str = "") -> Dict[str, Any]:
        """Analyze keywords from provided text"""
        try:
            print(f"🔍 Analyzing keywords from provided text ({len(text)} characters)")
            
            # Create metadata structure
            metadata = {
                'title': title,
                'description': description,
                'h1': [],
                'h2': [],
                'h3': []
            }
            
            # Perform keyword analysis
            keyword_analysis = self._analyze_keywords(text, metadata)
            
            # Add analysis metadata
            keyword_analysis['source'] = 'text_input'
            keyword_analysis['analysis_date'] = datetime.now().isoformat()
            
            return keyword_analysis
            
        except Exception as e:
            print(f"❌ Error analyzing text: {str(e)}")
            return {'error': str(e)}

    def analyze_competitor_keywords(self, urls: List[str]) -> Dict[str, Any]:
        """Analyze keywords from multiple competitor URLs"""
        try:
            print(f"🏆 Analyzing competitor keywords from {len(urls)} URLs")
            
            competitor_data = []
            all_keywords = []
            
            for url in urls:
                print(f"   📊 Analyzing: {url}")
                analysis = self.analyze_url_keywords(url)
                
                if 'error' not in analysis:
                    competitor_data.append(analysis)
                    all_keywords.extend(analysis.get('primary_keywords', []))
                else:
                    print(f"   ❌ Failed to analyze: {url}")
            
            # Perform competitive analysis
            competitive_analysis = self._perform_competitive_analysis(competitor_data)
            
            return {
                'competitor_analyses': competitor_data,
                'competitive_insights': competitive_analysis,
                'analysis_date': datetime.now().isoformat(),
                'total_competitors': len(competitor_data)
            }
            
        except Exception as e:
            print(f"❌ Error in competitor analysis: {str(e)}")
            return {'error': str(e)}

    def _extract_text_content(self, soup: BeautifulSoup) -> str:
        """Extract clean text content from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text

    def _extract_metadata(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract metadata from HTML"""
        metadata = {
            'title': '',
            'description': '',
            'keywords': '',
            'h1': [],
            'h2': [],
            'h3': [],
            'alt_texts': [],
            'links': []
        }
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            metadata['title'] = title_tag.get_text().strip()
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            metadata['description'] = meta_desc.get('content', '').strip()
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            metadata['keywords'] = meta_keywords.get('content', '').strip()
        
        # Headers
        for i in range(1, 4):
            headers = soup.find_all(f'h{i}')
            metadata[f'h{i}'] = [h.get_text().strip() for h in headers]
        
        # Alt texts
        images = soup.find_all('img')
        metadata['alt_texts'] = [img.get('alt', '').strip() for img in images if img.get('alt')]
        
        # Internal links
        links = soup.find_all('a', href=True)
        metadata['links'] = [link.get_text().strip() for link in links if link.get_text().strip()]
        
        return metadata

    def _analyze_keywords(self, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive keyword analysis"""
        # Basic text statistics
        word_count = len(text.split())
        char_count = len(text)
        
        # Language detection
        try:
            language = detect(text) if text else 'en'
        except:
            language = 'en'
        
        # Tokenize text
        words = word_tokenize(text.lower())
        sentences = sent_tokenize(text)
        
        # Remove stopwords and punctuation
        filtered_words = [word for word in words if word.isalnum() and word not in self.stop_words and len(word) > 2]
        
        # Calculate keyword density
        keyword_density = self._calculate_keyword_density(filtered_words)
        
        # Extract key phrases
        key_phrases = self._extract_key_phrases(text)
        
        # Analyze semantic clusters
        semantic_clusters = self._analyze_semantic_clusters(filtered_words)
        
        # TF-IDF analysis
        tfidf_keywords = self._perform_tfidf_analysis([text])
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(text)
        
        # Readability analysis
        readability = self._analyze_readability(text)
        
        # Metadata keyword analysis
        metadata_keywords = self._analyze_metadata_keywords(metadata)
        
        # Generate AI recommendations
        ai_recommendations = self._generate_ai_recommendations(text, metadata, keyword_density)
        
        # Create word cloud data
        wordcloud_data = self._generate_wordcloud_data(filtered_words)
        
        return {
            'text_statistics': {
                'word_count': word_count,
                'character_count': char_count,
                'sentence_count': len(sentences),
                'language': language,
                'unique_words': len(set(filtered_words))
            },
            'primary_keywords': list(keyword_density.keys())[:20],
            'keyword_density': dict(list(keyword_density.items())[:50]),
            'key_phrases': key_phrases,
            'semantic_clusters': semantic_clusters,
            'tfidf_keywords': tfidf_keywords,
            'sentiment_analysis': sentiment,
            'readability_analysis': readability,
            'metadata_keywords': metadata_keywords,
            'wordcloud_data': wordcloud_data,
            'ai_recommendations': ai_recommendations
        }

    def _calculate_keyword_density(self, words: List[str]) -> Dict[str, float]:
        """Calculate keyword density"""
        word_count = len(words)
        if word_count == 0:
            return {}
        
        word_freq = Counter(words)
        keyword_density = {}
        
        for word, freq in word_freq.most_common(100):
            density = (freq / word_count) * 100
            keyword_density[word] = round(density, 2)
        
        return keyword_density

    def _extract_key_phrases(self, text: str, max_phrases: int = 20) -> List[Dict[str, Any]]:
        """Extract key phrases using n-grams"""
        try:
            # Create n-grams (2-4 words)
            phrases = []
            words = word_tokenize(text.lower())
            
            for n in range(2, 5):  # 2-gram to 4-gram
                for i in range(len(words) - n + 1):
                    phrase = ' '.join(words[i:i+n])
                    if all(word.isalnum() and word not in self.stop_words for word in words[i:i+n]):
                        phrases.append(phrase)
            
            # Count phrase frequency
            phrase_freq = Counter(phrases)
            
            # Return top phrases with frequency
            key_phrases = []
            for phrase, freq in phrase_freq.most_common(max_phrases):
                key_phrases.append({
                    'phrase': phrase,
                    'frequency': freq,
                    'word_count': len(phrase.split())
                })
            
            return key_phrases
            
        except Exception as e:
            print(f"⚠️ Warning: Error extracting key phrases: {str(e)}")
            return []

    def _analyze_semantic_clusters(self, words: List[str], n_clusters: int = 5) -> List[Dict[str, Any]]:
        """Analyze semantic clusters using K-means"""
        try:
            if len(words) < 10:
                return []
            
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
            word_text = ' '.join(words)
            
            # Split into sentences for clustering
            sentences = sent_tokenize(word_text)
            if len(sentences) < n_clusters:
                n_clusters = max(1, len(sentences) // 2)
            
            if len(sentences) < 2:
                return []
            
            tfidf_matrix = vectorizer.fit_transform(sentences)
            
            # Perform K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(tfidf_matrix)
            
            # Get feature names
            feature_names = vectorizer.get_feature_names_out()
            
            # Analyze clusters
            cluster_analysis = []
            for i in range(n_clusters):
                cluster_center = kmeans.cluster_centers_[i]
                top_indices = cluster_center.argsort()[-10:][::-1]
                top_words = [feature_names[idx] for idx in top_indices]
                
                cluster_sentences = [sentences[j] for j, cluster in enumerate(clusters) if cluster == i]
                
                cluster_analysis.append({
                    'cluster_id': i,
                    'top_keywords': top_words,
                    'sentence_count': len(cluster_sentences),
                    'sample_sentences': cluster_sentences[:3]
                })
            
            return cluster_analysis
            
        except Exception as e:
            print(f"⚠️ Warning: Error in semantic clustering: {str(e)}")
            return []

    def _perform_tfidf_analysis(self, texts: List[str]) -> List[Dict[str, float]]:
        """Perform TF-IDF analysis"""
        try:
            vectorizer = TfidfVectorizer(
                max_features=50,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get TF-IDF scores
            tfidf_scores = []
            for i, text in enumerate(texts):
                scores = tfidf_matrix[i].toarray()[0]
                word_scores = list(zip(feature_names, scores))
                word_scores.sort(key=lambda x: x[1], reverse=True)
                
                tfidf_scores.append([
                    {'keyword': word, 'tfidf_score': round(score, 4)}
                    for word, score in word_scores[:30] if score > 0
                ])
            
            return tfidf_scores[0] if tfidf_scores else []
            
        except Exception as e:
            print(f"⚠️ Warning: Error in TF-IDF analysis: {str(e)}")
            return []

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of the text"""
        try:
            if not self.sentiment_analyzer:
                return {'error': 'Sentiment analyzer not available'}
            
            scores = self.sentiment_analyzer.polarity_scores(text)
            
            # Determine overall sentiment
            if scores['compound'] >= 0.05:
                overall = 'positive'
            elif scores['compound'] <= -0.05:
                overall = 'negative'
            else:
                overall = 'neutral'
            
            return {
                'overall_sentiment': overall,
                'positive_score': round(scores['pos'], 3),
                'negative_score': round(scores['neg'], 3),
                'neutral_score': round(scores['neu'], 3),
                'compound_score': round(scores['compound'], 3)
            }
            
        except Exception as e:
            print(f"⚠️ Warning: Error in sentiment analysis: {str(e)}")
            return {'error': str(e)}

    def _analyze_readability(self, text: str) -> Dict[str, Any]:
        """Analyze text readability"""
        try:
            return {
                'flesch_reading_ease': round(textstat.flesch_reading_ease(text), 2),
                'flesch_kincaid_grade': round(textstat.flesch_kincaid_grade(text), 2),
                'gunning_fog': round(textstat.gunning_fog(text), 2),
                'automated_readability_index': round(textstat.automated_readability_index(text), 2),
                'coleman_liau_index': round(textstat.coleman_liau_index(text), 2),
                'reading_time_minutes': round(textstat.reading_time(text, ms_per_char=14.69), 1)
            }
        except Exception as e:
            print(f"⚠️ Warning: Error in readability analysis: {str(e)}")
            return {}

    def _analyze_metadata_keywords(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze keywords in metadata"""
        metadata_analysis = {}
        
        # Title keywords
        if metadata.get('title'):
            title_words = word_tokenize(metadata['title'].lower())
            title_keywords = [word for word in title_words if word.isalnum() and word not in self.stop_words]
            metadata_analysis['title_keywords'] = title_keywords
        
        # Description keywords
        if metadata.get('description'):
            desc_words = word_tokenize(metadata['description'].lower())
            desc_keywords = [word for word in desc_words if word.isalnum() and word not in self.stop_words]
            metadata_analysis['description_keywords'] = desc_keywords
        
        # Header keywords
        for header_level in ['h1', 'h2', 'h3']:
            if metadata.get(header_level):
                header_text = ' '.join(metadata[header_level])
                header_words = word_tokenize(header_text.lower())
                header_keywords = [word for word in header_words if word.isalnum() and word not in self.stop_words]
                metadata_analysis[f'{header_level}_keywords'] = header_keywords
        
        return metadata_analysis

    def _generate_wordcloud_data(self, words: List[str]) -> str:
        """Generate word cloud data as base64 image"""
        try:
            if not words:
                return ""
            
            # Create word frequency dictionary
            word_freq = Counter(words)
            
            # Generate word cloud
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                max_words=100,
                colormap='viridis'
            ).generate_from_frequencies(word_freq)
            
            # Save to base64
            img_buffer = BytesIO()
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=150)
            plt.close()
            
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            print(f"⚠️ Warning: Error generating word cloud: {str(e)}")
            return ""

    def _perform_competitive_analysis(self, competitor_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform competitive keyword analysis"""
        try:
            if not competitor_data:
                return {}
            
            # Collect all keywords from competitors
            all_keywords = []
            competitor_keywords = {}
            
            for i, data in enumerate(competitor_data):
                domain = data.get('domain', f'competitor_{i+1}')
                keywords = data.get('primary_keywords', [])
                competitor_keywords[domain] = keywords
                all_keywords.extend(keywords)
            
            # Find common keywords
            keyword_counts = Counter(all_keywords)
            common_keywords = [kw for kw, count in keyword_counts.items() if count > 1]
            
            # Find unique keywords per competitor
            unique_keywords = {}
            for domain, keywords in competitor_keywords.items():
                unique = [kw for kw in keywords if keyword_counts[kw] == 1]
                unique_keywords[domain] = unique[:10]  # Top 10 unique
            
            # Calculate keyword overlap matrix
            overlap_matrix = {}
            domains = list(competitor_keywords.keys())
            
            for i, domain1 in enumerate(domains):
                overlap_matrix[domain1] = {}
                for domain2 in domains:
                    if domain1 != domain2:
                        kw1 = set(competitor_keywords[domain1])
                        kw2 = set(competitor_keywords[domain2])
                        overlap = len(kw1.intersection(kw2))
                        total = len(kw1.union(kw2))
                        similarity = (overlap / total * 100) if total > 0 else 0
                        overlap_matrix[domain1][domain2] = round(similarity, 2)
            
            return {
                'total_unique_keywords': len(set(all_keywords)),
                'common_keywords': common_keywords[:20],
                'unique_keywords_per_competitor': unique_keywords,
                'keyword_overlap_matrix': overlap_matrix,
                'most_frequent_keywords': [kw for kw, count in keyword_counts.most_common(20)]
            }
            
        except Exception as e:
            print(f"⚠️ Warning: Error in competitive analysis: {str(e)}")
            return {'error': str(e)}

    def _generate_ai_recommendations(self, text: str, metadata: Dict[str, Any], keyword_density: Dict[str, float]) -> List[str]:
        """Generate AI-powered keyword recommendations"""
        try:
            # Prepare analysis summary for AI
            top_keywords = list(keyword_density.keys())[:10]
            word_count = len(text.split())
            
            prompt = f"""
            Analyze this content and provide keyword optimization recommendations:
            
            Content Statistics:
            - Word count: {word_count}
            - Top keywords: {', '.join(top_keywords)}
            - Title: {metadata.get('title', 'Not provided')}
            - Meta description: {metadata.get('description', 'Not provided')}
            
            Provide 8-10 specific, actionable SEO keyword recommendations focusing on:
            1. Keyword density optimization
            2. Long-tail keyword opportunities
            3. Semantic keyword suggestions
            4. Content gaps to fill
            5. Title and meta optimization
            
            Format as a numbered list with brief explanations.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert SEO consultant specializing in keyword optimization. Provide specific, actionable recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            recommendations = response.choices[0].message.content.strip().split('\n')
            return [rec.strip() for rec in recommendations if rec.strip()]
            
        except Exception as e:
            print(f"⚠️ Warning: Error generating AI recommendations: {str(e)}")
            return [
                "1. Optimize keyword density for primary keywords (aim for 1-3%)",
                "2. Include more long-tail keywords to capture specific search intent",
                "3. Add semantic keywords related to your main topics",
                "4. Optimize title tag with primary keywords",
                "5. Improve meta description with relevant keywords",
                "6. Use keywords naturally in headers (H1, H2, H3)",
                "7. Include keywords in image alt text",
                "8. Create content around related keyword clusters"
            ]

    def export_analysis_to_json(self, analysis_data: Dict[str, Any], filename: str) -> str:
        """Export analysis data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis_data, f, indent=2, ensure_ascii=False)
            return filename
        except Exception as e:
            print(f"❌ Error exporting to JSON: {str(e)}")
            return ""

    def export_analysis_to_csv(self, analysis_data: Dict[str, Any], filename: str) -> str:
        """Export keyword analysis to CSV file"""
        try:
            # Prepare data for CSV
            csv_data = []
            
            # Primary keywords with density
            keyword_density = analysis_data.get('keyword_density', {})
            for keyword, density in keyword_density.items():
                csv_data.append({
                    'keyword': keyword,
                    'density_percent': density,
                    'type': 'primary'
                })
            
            # Key phrases
            key_phrases = analysis_data.get('key_phrases', [])
            for phrase_data in key_phrases:
                csv_data.append({
                    'keyword': phrase_data.get('phrase', ''),
                    'frequency': phrase_data.get('frequency', 0),
                    'type': 'phrase'
                })
            
            # TF-IDF keywords
            tfidf_keywords = analysis_data.get('tfidf_keywords', [])
            for tfidf_data in tfidf_keywords:
                csv_data.append({
                    'keyword': tfidf_data.get('keyword', ''),
                    'tfidf_score': tfidf_data.get('tfidf_score', 0),
                    'type': 'tfidf'
                })
            
            # Create DataFrame and save
            df = pd.DataFrame(csv_data)
            df.to_csv(filename, index=False, encoding='utf-8')
            return filename
            
        except Exception as e:
            print(f"❌ Error exporting to CSV: {str(e)}")
            return ""