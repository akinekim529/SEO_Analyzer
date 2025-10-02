#!/usr/bin/env python3
"""
Keyword Analysis HTML Report Generator
Generates comprehensive HTML reports for keyword analysis with recommendations
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any
import base64

class KeywordReportGenerator:
    def __init__(self):
        self.report_template = self._get_report_template()

    def generate_comprehensive_report(self, analysis_data: Dict[str, Any], 
                                    competitive_data: Dict[str, Any] = None) -> str:
        """Generate comprehensive HTML report"""
        
        # Extract data
        text_stats = analysis_data.get('text_statistics', {})
        keyword_density = analysis_data.get('keyword_density', {})
        key_phrases = analysis_data.get('key_phrases', [])
        semantic_clusters = analysis_data.get('semantic_clusters', [])
        tfidf_keywords = analysis_data.get('tfidf_keywords', [])
        sentiment = analysis_data.get('sentiment_analysis', {})
        readability = analysis_data.get('readability_analysis', {})
        metadata_keywords = analysis_data.get('metadata_keywords', {})
        ai_recommendations = analysis_data.get('ai_recommendations', [])
        wordcloud_data = analysis_data.get('wordcloud_data', '')
        
        # Generate sections
        overview_section = self._generate_overview_section(analysis_data, text_stats)
        keyword_density_section = self._generate_keyword_density_section(keyword_density)
        key_phrases_section = self._generate_key_phrases_section(key_phrases)
        semantic_analysis_section = self._generate_semantic_analysis_section(semantic_clusters)
        tfidf_section = self._generate_tfidf_section(tfidf_keywords)
        sentiment_section = self._generate_sentiment_section(sentiment)
        readability_section = self._generate_readability_section(readability)
        metadata_section = self._generate_metadata_section(metadata_keywords)
        wordcloud_section = self._generate_wordcloud_section(wordcloud_data)
        competitive_section = self._generate_competitive_section(competitive_data) if competitive_data else ""
        recommendations_section = self._generate_recommendations_section(ai_recommendations)
        
        # Combine all sections
        report_content = f"""
        {overview_section}
        {keyword_density_section}
        {key_phrases_section}
        {semantic_analysis_section}
        {tfidf_section}
        {sentiment_section}
        {readability_section}
        {metadata_section}
        {wordcloud_section}
        {competitive_section}
        {recommendations_section}
        """
        
        # Insert into template
        report_html = self.report_template.replace('{{REPORT_CONTENT}}', report_content)
        report_html = report_html.replace('{{ANALYSIS_DATE}}', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        report_html = report_html.replace('{{SOURCE_URL}}', analysis_data.get('url', 'Text Input'))
        
        return report_html

    def _generate_overview_section(self, analysis_data: Dict[str, Any], text_stats: Dict[str, Any]) -> str:
        """Generate overview section"""
        source = analysis_data.get('url', 'Text Input')
        domain = analysis_data.get('domain', 'N/A')
        
        return f"""
        <div class="section">
            <h2><span class="section-icon">📊</span>Analysis Overview</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{text_stats.get('word_count', 0):,}</div>
                    <div class="stat-label">Total Words</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{text_stats.get('unique_words', 0):,}</div>
                    <div class="stat-label">Unique Words</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{text_stats.get('sentence_count', 0):,}</div>
                    <div class="stat-label">Sentences</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{text_stats.get('language', 'en').upper()}</div>
                    <div class="stat-label">Language</div>
                </div>
            </div>
            
            <div class="info-box">
                <h3>📍 Source Information</h3>
                <p><strong>Source:</strong> {source}</p>
                {f'<p><strong>Domain:</strong> {domain}</p>' if domain != 'N/A' else ''}
                <p><strong>Analysis Date:</strong> {analysis_data.get('analysis_date', 'N/A')}</p>
                <p><strong>Character Count:</strong> {text_stats.get('character_count', 0):,}</p>
            </div>
        </div>
        """

    def _generate_keyword_density_section(self, keyword_density: Dict[str, float]) -> str:
        """Generate keyword density section"""
        if not keyword_density:
            return ""
        
        # Create keyword density chart data
        top_keywords = list(keyword_density.items())[:20]
        
        keywords_html = ""
        for keyword, density in top_keywords:
            # Determine density level
            if density >= 3:
                level_class = "high"
                level_text = "High"
            elif density >= 1:
                level_class = "medium"
                level_text = "Medium"
            else:
                level_class = "low"
                level_text = "Low"
            
            keywords_html += f"""
            <div class="keyword-item">
                <div class="keyword-info">
                    <span class="keyword-text">{keyword}</span>
                    <span class="density-badge density-{level_class}">{density}% ({level_text})</span>
                </div>
                <div class="density-bar">
                    <div class="density-fill density-{level_class}" style="width: {min(density * 10, 100)}%"></div>
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2><span class="section-icon">🎯</span>Keyword Density Analysis</h2>
            <div class="info-box">
                <h3>📈 Top Keywords by Density</h3>
                <p>Keyword density shows how frequently each word appears relative to the total word count. Optimal density is typically 1-3% for primary keywords.</p>
            </div>
            
            <div class="keywords-container">
                {keywords_html}
            </div>
            
            <div class="density-legend">
                <div class="legend-item">
                    <span class="legend-color density-high"></span>
                    <span>High Density (3%+) - May be over-optimized</span>
                </div>
                <div class="legend-item">
                    <span class="legend-color density-medium"></span>
                    <span>Medium Density (1-3%) - Optimal range</span>
                </div>
                <div class="legend-item">
                    <span class="legend-color density-low"></span>
                    <span>Low Density (<1%) - Could be increased</span>
                </div>
            </div>
        </div>
        """

    def _generate_key_phrases_section(self, key_phrases: List[Dict[str, Any]]) -> str:
        """Generate key phrases section"""
        if not key_phrases:
            return ""
        
        phrases_html = ""
        for phrase_data in key_phrases[:15]:
            phrase = phrase_data.get('phrase', '')
            frequency = phrase_data.get('frequency', 0)
            word_count = phrase_data.get('word_count', 0)
            
            phrases_html += f"""
            <div class="phrase-item">
                <div class="phrase-text">"{phrase}"</div>
                <div class="phrase-stats">
                    <span class="phrase-frequency">Frequency: {frequency}</span>
                    <span class="phrase-length">{word_count} words</span>
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2><span class="section-icon">🔗</span>Key Phrases Analysis</h2>
            <div class="info-box">
                <h3>💡 Multi-word Phrases</h3>
                <p>Key phrases are combinations of 2-4 words that appear frequently in your content. These often represent important topics and potential long-tail keywords.</p>
            </div>
            
            <div class="phrases-container">
                {phrases_html}
            </div>
        </div>
        """

    def _generate_semantic_analysis_section(self, semantic_clusters: List[Dict[str, Any]]) -> str:
        """Generate semantic analysis section"""
        if not semantic_clusters:
            return ""
        
        clusters_html = ""
        for cluster in semantic_clusters:
            cluster_id = cluster.get('cluster_id', 0)
            top_keywords = cluster.get('top_keywords', [])
            sentence_count = cluster.get('sentence_count', 0)
            sample_sentences = cluster.get('sample_sentences', [])
            
            keywords_list = ', '.join(top_keywords[:8])
            
            clusters_html += f"""
            <div class="cluster-item">
                <div class="cluster-header">
                    <h4>Cluster {cluster_id + 1}</h4>
                    <span class="cluster-size">{sentence_count} sentences</span>
                </div>
                <div class="cluster-keywords">
                    <strong>Key Terms:</strong> {keywords_list}
                </div>
                {f'<div class="cluster-sample"><strong>Sample:</strong> "{sample_sentences[0][:150]}..."</div>' if sample_sentences else ''}
            </div>
            """
        
        return f"""
        <div class="section">
            <h2><span class="section-icon">🧠</span>Semantic Clusters</h2>
            <div class="info-box">
                <h3>🔍 Topic Clustering</h3>
                <p>Semantic clusters group your content into related topics using AI. This helps identify main themes and content organization opportunities.</p>
            </div>
            
            <div class="clusters-container">
                {clusters_html}
            </div>
        </div>
        """

    def _generate_tfidf_section(self, tfidf_keywords: List[Dict[str, Any]]) -> str:
        """Generate TF-IDF section"""
        if not tfidf_keywords:
            return ""
        
        tfidf_html = ""
        for item in tfidf_keywords[:20]:
            keyword = item.get('keyword', '')
            score = item.get('tfidf_score', 0)
            
            # Normalize score for visualization (0-100)
            normalized_score = min(score * 1000, 100)
            
            tfidf_html += f"""
            <div class="tfidf-item">
                <div class="tfidf-keyword">{keyword}</div>
                <div class="tfidf-score-container">
                    <div class="tfidf-score">{score:.4f}</div>
                    <div class="tfidf-bar">
                        <div class="tfidf-fill" style="width: {normalized_score}%"></div>
                    </div>
                </div>
            </div>
            """
        
        return f"""
        <div class="section">
            <h2><span class="section-icon">📐</span>TF-IDF Analysis</h2>
            <div class="info-box">
                <h3>🎯 Term Importance Scoring</h3>
                <p>TF-IDF (Term Frequency-Inverse Document Frequency) identifies the most important and unique terms in your content. Higher scores indicate more distinctive keywords.</p>
            </div>
            
            <div class="tfidf-container">
                {tfidf_html}
            </div>
        </div>
        """

    def _generate_sentiment_section(self, sentiment: Dict[str, Any]) -> str:
        """Generate sentiment analysis section"""
        if not sentiment or 'error' in sentiment:
            return ""
        
        overall = sentiment.get('overall_sentiment', 'neutral')
        positive = sentiment.get('positive_score', 0) * 100
        negative = sentiment.get('negative_score', 0) * 100
        neutral = sentiment.get('neutral_score', 0) * 100
        compound = sentiment.get('compound_score', 0)
        
        # Determine sentiment color
        sentiment_colors = {
            'positive': '#4CAF50',
            'negative': '#F44336',
            'neutral': '#FF9800'
        }
        sentiment_color = sentiment_colors.get(overall, '#FF9800')
        
        return f"""
        <div class="section">
            <h2><span class="section-icon">😊</span>Sentiment Analysis</h2>
            <div class="sentiment-overview">
                <div class="sentiment-main">
                    <div class="sentiment-indicator" style="background-color: {sentiment_color};">
                        {overall.upper()}
                    </div>
                    <div class="sentiment-compound">
                        Compound Score: {compound:.3f}
                    </div>
                </div>
                
                <div class="sentiment-breakdown">
                    <div class="sentiment-bar-container">
                        <div class="sentiment-label">Positive</div>
                        <div class="sentiment-bar">
                            <div class="sentiment-fill positive" style="width: {positive}%"></div>
                        </div>
                        <div class="sentiment-value">{positive:.1f}%</div>
                    </div>
                    
                    <div class="sentiment-bar-container">
                        <div class="sentiment-label">Neutral</div>
                        <div class="sentiment-bar">
                            <div class="sentiment-fill neutral" style="width: {neutral}%"></div>
                        </div>
                        <div class="sentiment-value">{neutral:.1f}%</div>
                    </div>
                    
                    <div class="sentiment-bar-container">
                        <div class="sentiment-label">Negative</div>
                        <div class="sentiment-bar">
                            <div class="sentiment-fill negative" style="width: {negative}%"></div>
                        </div>
                        <div class="sentiment-value">{negative:.1f}%</div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _generate_readability_section(self, readability: Dict[str, Any]) -> str:
        """Generate readability analysis section"""
        if not readability:
            return ""
        
        flesch_ease = readability.get('flesch_reading_ease', 0)
        flesch_grade = readability.get('flesch_kincaid_grade', 0)
        gunning_fog = readability.get('gunning_fog', 0)
        reading_time = readability.get('reading_time_minutes', 0)
        
        # Determine readability level
        if flesch_ease >= 90:
            ease_level = "Very Easy"
            ease_color = "#4CAF50"
        elif flesch_ease >= 80:
            ease_level = "Easy"
            ease_color = "#8BC34A"
        elif flesch_ease >= 70:
            ease_level = "Fairly Easy"
            ease_color = "#CDDC39"
        elif flesch_ease >= 60:
            ease_level = "Standard"
            ease_color = "#FF9800"
        elif flesch_ease >= 50:
            ease_level = "Fairly Difficult"
            ease_color = "#FF5722"
        else:
            ease_level = "Difficult"
            ease_color = "#F44336"
        
        return f"""
        <div class="section">
            <h2><span class="section-icon">📚</span>Readability Analysis</h2>
            <div class="readability-overview">
                <div class="readability-main">
                    <div class="readability-score" style="background-color: {ease_color};">
                        {flesch_ease:.1f}
                    </div>
                    <div class="readability-level">{ease_level}</div>
                </div>
                
                <div class="readability-metrics">
                    <div class="metric-item">
                        <div class="metric-label">Grade Level</div>
                        <div class="metric-value">{flesch_grade:.1f}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Gunning Fog</div>
                        <div class="metric-value">{gunning_fog:.1f}</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-label">Reading Time</div>
                        <div class="metric-value">{reading_time:.1f} min</div>
                    </div>
                </div>
            </div>
            
            <div class="info-box">
                <h3>📖 Readability Guidelines</h3>
                <p><strong>Flesch Reading Ease:</strong> Higher scores indicate easier reading. Aim for 60-70 for general audiences.</p>
                <p><strong>Grade Level:</strong> Shows the education level needed to understand the text. Lower is generally better for web content.</p>
            </div>
        </div>
        """

    def _generate_metadata_section(self, metadata_keywords: Dict[str, Any]) -> str:
        """Generate metadata keywords section"""
        if not metadata_keywords:
            return ""
        
        metadata_html = ""
        
        for key, keywords in metadata_keywords.items():
            if keywords:
                display_name = key.replace('_keywords', '').replace('_', ' ').title()
                keywords_list = ', '.join(keywords[:10])
                
                metadata_html += f"""
                <div class="metadata-item">
                    <div class="metadata-label">{display_name}</div>
                    <div class="metadata-keywords">{keywords_list}</div>
                </div>
                """
        
        if not metadata_html:
            return ""
        
        return f"""
        <div class="section">
            <h2><span class="section-icon">🏷️</span>Metadata Keywords</h2>
            <div class="info-box">
                <h3>🔍 SEO Metadata Analysis</h3>
                <p>Keywords extracted from page titles, descriptions, headers, and other metadata elements. These are crucial for SEO optimization.</p>
            </div>
            
            <div class="metadata-container">
                {metadata_html}
            </div>
        </div>
        """

    def _generate_wordcloud_section(self, wordcloud_data: str) -> str:
        """Generate word cloud section"""
        if not wordcloud_data:
            return ""
        
        return f"""
        <div class="section">
            <h2><span class="section-icon">☁️</span>Word Cloud Visualization</h2>
            <div class="info-box">
                <h3>👁️ Visual Keyword Overview</h3>
                <p>Word cloud visualization showing the most frequent keywords. Larger words appear more frequently in your content.</p>
            </div>
            
            <div class="wordcloud-container">
                <img src="{wordcloud_data}" alt="Word Cloud" class="wordcloud-image">
            </div>
        </div>
        """

    def _generate_competitive_section(self, competitive_data: Dict[str, Any]) -> str:
        """Generate competitive analysis section"""
        if not competitive_data or 'error' in competitive_data:
            return ""
        
        common_keywords = competitive_data.get('common_keywords', [])
        unique_keywords = competitive_data.get('unique_keywords_per_competitor', {})
        overlap_matrix = competitive_data.get('keyword_overlap_matrix', {})
        
        # Common keywords
        common_html = ""
        for keyword in common_keywords[:15]:
            common_html += f'<span class="keyword-tag">{keyword}</span>'
        
        # Unique keywords per competitor
        unique_html = ""
        for domain, keywords in unique_keywords.items():
            keywords_list = ', '.join(keywords[:8])
            unique_html += f"""
            <div class="competitor-unique">
                <div class="competitor-domain">{domain}</div>
                <div class="competitor-keywords">{keywords_list}</div>
            </div>
            """
        
        # Overlap matrix
        overlap_html = ""
        for domain1, overlaps in overlap_matrix.items():
            for domain2, similarity in overlaps.items():
                color_intensity = similarity / 100
                overlap_html += f"""
                <div class="overlap-item">
                    <span class="overlap-domains">{domain1} ↔ {domain2}</span>
                    <div class="overlap-bar">
                        <div class="overlap-fill" style="width: {similarity}%; background-color: rgba(43, 89, 255, {color_intensity})"></div>
                    </div>
                    <span class="overlap-percentage">{similarity}%</span>
                </div>
                """
        
        return f"""
        <div class="section">
            <h2><span class="section-icon">🏆</span>Competitive Analysis</h2>
            
            <div class="competitive-subsection">
                <h3>🤝 Common Keywords</h3>
                <p>Keywords that appear across multiple competitors:</p>
                <div class="keywords-tags">
                    {common_html}
                </div>
            </div>
            
            <div class="competitive-subsection">
                <h3>🎯 Unique Keywords by Competitor</h3>
                <div class="unique-keywords-container">
                    {unique_html}
                </div>
            </div>
            
            <div class="competitive-subsection">
                <h3>📊 Keyword Overlap Matrix</h3>
                <p>Similarity percentage between competitors based on shared keywords:</p>
                <div class="overlap-container">
                    {overlap_html}
                </div>
            </div>
        </div>
        """

    def _generate_recommendations_section(self, ai_recommendations: List[str]) -> str:
        """Generate AI recommendations section"""
        if not ai_recommendations:
            return ""
        
        recommendations_html = ""
        for i, recommendation in enumerate(ai_recommendations, 1):
            # Clean up the recommendation text
            clean_rec = recommendation.strip()
            if clean_rec.startswith(f"{i}."):
                clean_rec = clean_rec[len(f"{i}."):].strip()
            elif clean_rec.startswith(f"{i})"):
                clean_rec = clean_rec[len(f"{i})"):].strip()
            
            recommendations_html += f"""
            <div class="recommendation-item">
                <div class="recommendation-number">{i}</div>
                <div class="recommendation-text">{clean_rec}</div>
            </div>
            """
        
        return f"""
        <div class="section recommendations">
            <h2><span class="section-icon">🚀</span>AI-Powered Recommendations</h2>
            <div class="info-box">
                <h3>🤖 Expert SEO Suggestions</h3>
                <p>AI-generated recommendations based on your keyword analysis. These suggestions are tailored to improve your content's SEO performance.</p>
            </div>
            
            <div class="recommendations-container">
                {recommendations_html}
            </div>
        </div>
        """

    def _get_report_template(self) -> str:
        """Get the HTML report template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔍 Comprehensive Keyword Analysis Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .header h1 {
            color: #667eea;
            font-size: 3em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header p {
            color: #666;
            font-size: 1.2em;
            margin: 10px 0;
        }
        
        .section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .section h2 {
            color: #667eea;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            font-size: 1.8em;
            font-weight: 600;
        }
        
        .section-icon {
            margin-right: 15px;
            font-size: 1.2em;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 25px 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        }
        
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .stat-label {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .info-box {
            background: #f8f9ff;
            border: 2px solid #e3e8ff;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .info-box h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .info-box p {
            color: #666;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        
        /* Keyword Density Styles */
        .keywords-container {
            display: grid;
            gap: 15px;
            margin: 20px 0;
        }
        
        .keyword-item {
            background: #f8f9ff;
            border-radius: 10px;
            padding: 15px;
            border-left: 4px solid #667eea;
        }
        
        .keyword-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .keyword-text {
            font-weight: 600;
            color: #333;
            font-size: 1.1em;
        }
        
        .density-badge {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            color: white;
        }
        
        .density-high { background: #f44336; }
        .density-medium { background: #4caf50; }
        .density-low { background: #ff9800; }
        
        .density-bar {
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .density-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 1s ease-out;
        }
        
        .density-legend {
            display: flex;
            gap: 20px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9em;
        }
        
        .legend-color {
            width: 16px;
            height: 16px;
            border-radius: 3px;
        }
        
        /* Key Phrases Styles */
        .phrases-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .phrase-item {
            background: #f8f9ff;
            border-radius: 10px;
            padding: 15px;
            border-left: 4px solid #764ba2;
        }
        
        .phrase-text {
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
            font-style: italic;
        }
        
        .phrase-stats {
            display: flex;
            gap: 15px;
            font-size: 0.9em;
            color: #666;
        }
        
        /* Semantic Clusters Styles */
        .clusters-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .cluster-item {
            background: #f8f9ff;
            border-radius: 10px;
            padding: 20px;
            border: 2px solid #e3e8ff;
        }
        
        .cluster-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .cluster-header h4 {
            color: #667eea;
            font-size: 1.2em;
        }
        
        .cluster-size {
            background: #667eea;
            color: white;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.8em;
        }
        
        .cluster-keywords {
            margin-bottom: 10px;
            line-height: 1.5;
        }
        
        .cluster-sample {
            font-style: italic;
            color: #666;
            font-size: 0.9em;
        }
        
        /* TF-IDF Styles */
        .tfidf-container {
            display: grid;
            gap: 10px;
            margin: 20px 0;
        }
        
        .tfidf-item {
            display: flex;
            align-items: center;
            background: #f8f9ff;
            border-radius: 8px;
            padding: 12px;
            gap: 15px;
        }
        
        .tfidf-keyword {
            font-weight: 600;
            color: #333;
            min-width: 150px;
        }
        
        .tfidf-score-container {
            flex: 1;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .tfidf-score {
            font-family: monospace;
            color: #667eea;
            font-weight: 600;
            min-width: 60px;
        }
        
        .tfidf-bar {
            flex: 1;
            height: 6px;
            background: #e0e0e0;
            border-radius: 3px;
            overflow: hidden;
        }
        
        .tfidf-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 3px;
            transition: width 1s ease-out;
        }
        
        /* Sentiment Styles */
        .sentiment-overview {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 30px;
            align-items: center;
            margin: 20px 0;
        }
        
        .sentiment-main {
            text-align: center;
        }
        
        .sentiment-indicator {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        
        .sentiment-compound {
            font-weight: 600;
            color: #333;
        }
        
        .sentiment-breakdown {
            display: grid;
            gap: 15px;
        }
        
        .sentiment-bar-container {
            display: grid;
            grid-template-columns: 80px 1fr 60px;
            gap: 15px;
            align-items: center;
        }
        
        .sentiment-label {
            font-weight: 600;
            color: #333;
        }
        
        .sentiment-bar {
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
        }
        
        .sentiment-fill {
            height: 100%;
            border-radius: 10px;
            transition: width 1s ease-out;
        }
        
        .sentiment-fill.positive { background: #4CAF50; }
        .sentiment-fill.neutral { background: #FF9800; }
        .sentiment-fill.negative { background: #F44336; }
        
        .sentiment-value {
            font-weight: 600;
            color: #333;
            text-align: right;
        }
        
        /* Readability Styles */
        .readability-overview {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 30px;
            align-items: center;
            margin: 20px 0;
        }
        
        .readability-main {
            text-align: center;
        }
        
        .readability-score {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 1.8em;
            margin-bottom: 10px;
        }
        
        .readability-level {
            font-weight: 600;
            color: #333;
        }
        
        .readability-metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 20px;
        }
        
        .metric-item {
            text-align: center;
            background: #f8f9ff;
            padding: 15px;
            border-radius: 10px;
        }
        
        .metric-label {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }
        
        /* Metadata Styles */
        .metadata-container {
            display: grid;
            gap: 15px;
            margin: 20px 0;
        }
        
        .metadata-item {
            background: #f8f9ff;
            border-radius: 10px;
            padding: 15px;
            border-left: 4px solid #667eea;
        }
        
        .metadata-label {
            font-weight: 600;
            color: #667eea;
            margin-bottom: 8px;
            font-size: 1.1em;
        }
        
        .metadata-keywords {
            color: #333;
            line-height: 1.5;
        }
        
        /* Word Cloud Styles */
        .wordcloud-container {
            text-align: center;
            margin: 20px 0;
            padding: 20px;
            background: #f8f9ff;
            border-radius: 15px;
        }
        
        .wordcloud-image {
            max-width: 100%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }
        
        /* Competitive Analysis Styles */
        .competitive-subsection {
            margin: 25px 0;
            padding: 20px;
            background: #f8f9ff;
            border-radius: 15px;
        }
        
        .competitive-subsection h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .keywords-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }
        
        .keyword-tag {
            background: #667eea;
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }
        
        .unique-keywords-container {
            display: grid;
            gap: 15px;
            margin: 15px 0;
        }
        
        .competitor-unique {
            background: white;
            border-radius: 10px;
            padding: 15px;
            border-left: 4px solid #764ba2;
        }
        
        .competitor-domain {
            font-weight: 600;
            color: #764ba2;
            margin-bottom: 8px;
        }
        
        .competitor-keywords {
            color: #333;
            line-height: 1.5;
        }
        
        .overlap-container {
            display: grid;
            gap: 10px;
            margin: 15px 0;
        }
        
        .overlap-item {
            display: grid;
            grid-template-columns: 200px 1fr 60px;
            gap: 15px;
            align-items: center;
            background: white;
            padding: 10px 15px;
            border-radius: 8px;
        }
        
        .overlap-domains {
            font-weight: 600;
            color: #333;
            font-size: 0.9em;
        }
        
        .overlap-bar {
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
        }
        
        .overlap-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 1s ease-out;
        }
        
        .overlap-percentage {
            font-weight: 600;
            color: #333;
            text-align: right;
            font-size: 0.9em;
        }
        
        /* Recommendations Styles */
        .recommendations {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .recommendations h2 {
            color: white;
        }
        
        .recommendations .info-box {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2);
            color: white;
        }
        
        .recommendations .info-box h3 {
            color: white;
        }
        
        .recommendations .info-box p {
            color: rgba(255, 255, 255, 0.9);
        }
        
        .recommendations-container {
            display: grid;
            gap: 15px;
            margin: 20px 0;
        }
        
        .recommendation-item {
            display: flex;
            gap: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .recommendation-number {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
            flex-shrink: 0;
        }
        
        .recommendation-text {
            color: white;
            line-height: 1.6;
            font-size: 1.1em;
        }
        
        .footer {
            text-align: center;
            color: rgba(255, 255, 255, 0.9);
            margin-top: 40px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        
        .footer h3 {
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        
        .footer p {
            margin: 10px 0;
            font-size: 1.1em;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .section {
                padding: 20px;
            }
            
            .stats-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }
            
            .sentiment-overview,
            .readability-overview {
                grid-template-columns: 1fr;
                text-align: center;
            }
            
            .overlap-item {
                grid-template-columns: 1fr;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Comprehensive Keyword Analysis Report</h1>
            <p><strong>Source:</strong> {{SOURCE_URL}}</p>
            <p><strong>Generated:</strong> {{ANALYSIS_DATE}}</p>
            <p>Advanced AI-powered keyword analysis with SEO recommendations</p>
        </div>
        
        {{REPORT_CONTENT}}
        
        <div class="footer">
            <h3>🚀 Keyword Analysis Complete</h3>
            <p>This comprehensive report provides detailed insights into your content's keyword performance.</p>
            <p>Use the recommendations above to optimize your content for better SEO results.</p>
            <p><strong>Powered by AI • Advanced Keyword Analysis Tool</strong></p>
        </div>
    </div>
    
    <script>
        // Add smooth animations when page loads
        document.addEventListener('DOMContentLoaded', function() {
            // Animate progress bars
            const bars = document.querySelectorAll('.density-fill, .tfidf-fill, .sentiment-fill, .overlap-fill');
            bars.forEach(bar => {
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = width;
                }, 500);
            });
            
            // Animate stat cards
            const statCards = document.querySelectorAll('.stat-card');
            statCards.forEach((card, index) => {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    card.style.transition = 'all 0.6s ease';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, index * 100);
            });
        });
    </script>
</body>
</html>
        """