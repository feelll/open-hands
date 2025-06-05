import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import jieba
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

class DataAnalyzer:
    def __init__(self):
        self.data = None
        self.analysis_results = {}
        
    def load_data(self, scraped_data):
        """加载抓取的数据"""
        self.data = scraped_data
        
    def analyze_search_terms(self, search_terms):
        """分析搜索词"""
        if not search_terms:
            return {}
        
        # 转换为DataFrame
        df = pd.DataFrame(search_terms, columns=['term', 'frequency'])
        
        analysis = {
            'total_unique_terms': len(df),
            'top_terms': df.head(20).to_dict('records'),
            'frequency_distribution': {
                'high_frequency': len(df[df['frequency'] >= 10]),
                'medium_frequency': len(df[(df['frequency'] >= 5) & (df['frequency'] < 10)]),
                'low_frequency': len(df[df['frequency'] < 5])
            },
            'term_length_analysis': {
                'avg_length': df['term'].str.len().mean(),
                'max_length': df['term'].str.len().max(),
                'min_length': df['term'].str.len().min()
            }
        }
        
        return analysis
    
    def create_word_cloud(self, text_content, language='chinese'):
        """生成词云"""
        if not text_content:
            return None
        
        try:
            if language == 'chinese':
                # 中文分词
                words = jieba.cut(text_content)
                text_for_cloud = ' '.join(words)
            else:
                text_for_cloud = text_content
            
            # 创建词云
            wordcloud = WordCloud(
                width=800, 
                height=400,
                background_color='white',
                max_words=100,
                colormap='viridis'
            ).generate(text_for_cloud)
            
            # 保存词云图片
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig('/workspace/web-data-analyzer/static/wordcloud.png', 
                       bbox_inches='tight', dpi=300)
            plt.close()
            
            return '/static/wordcloud.png'
        except Exception as e:
            print(f"生成词云失败: {e}")
            return None
    
    def analyze_content_structure(self, extracted_data):
        """分析内容结构"""
        if not extracted_data:
            return {}
        
        structure_analysis = {
            'heading_distribution': {},
            'content_density': 0,
            'link_density': 0,
            'image_density': 0,
            'text_statistics': {}
        }
        
        # 标题分布分析
        headings = extracted_data.get('headings', [])
        for heading in headings:
            level = f"h{heading['level']}"
            structure_analysis['heading_distribution'][level] = \
                structure_analysis['heading_distribution'].get(level, 0) + 1
        
        # 内容密度分析
        text_content = extracted_data.get('text_content', '')
        paragraphs = extracted_data.get('paragraphs', [])
        links = extracted_data.get('links', [])
        images = extracted_data.get('images', [])
        
        total_chars = len(text_content)
        if total_chars > 0:
            structure_analysis['content_density'] = len(paragraphs) / total_chars * 1000
            structure_analysis['link_density'] = len(links) / total_chars * 1000
            structure_analysis['image_density'] = len(images) / total_chars * 1000
        
        # 文本统计
        structure_analysis['text_statistics'] = {
            'total_characters': total_chars,
            'total_paragraphs': len(paragraphs),
            'total_links': len(links),
            'total_images': len(images),
            'avg_paragraph_length': np.mean([len(p) for p in paragraphs]) if paragraphs else 0
        }
        
        return structure_analysis
    
    def sentiment_analysis(self, text_content):
        """情感分析（简单版本）"""
        if not text_content:
            return {}
        
        # 简单的情感词典（可以扩展）
        positive_words = ['好', '棒', '优秀', '喜欢', '满意', '推荐', '完美', '出色', 
                         'good', 'great', 'excellent', 'amazing', 'wonderful', 'perfect']
        negative_words = ['差', '糟糕', '失望', '不好', '讨厌', '问题', '错误', 
                         'bad', 'terrible', 'awful', 'horrible', 'disappointing', 'problem']
        
        text_lower = text_content.lower()
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            sentiment_score = 0
        else:
            sentiment_score = (positive_count - negative_count) / total_sentiment_words
        
        return {
            'sentiment_score': sentiment_score,
            'positive_words_count': positive_count,
            'negative_words_count': negative_count,
            'sentiment_label': 'positive' if sentiment_score > 0.1 else 'negative' if sentiment_score < -0.1 else 'neutral'
        }
    
    def create_visualizations(self, analysis_data):
        """创建可视化图表"""
        visualizations = {}
        
        try:
            # 1. 搜索词频率图
            if 'search_terms' in analysis_data:
                search_data = analysis_data['search_terms']
                if search_data.get('top_terms'):
                    terms_df = pd.DataFrame(search_data['top_terms'])
                    
                    fig = px.bar(
                        terms_df.head(15), 
                        x='frequency', 
                        y='term',
                        orientation='h',
                        title='Top 15 Search Terms by Frequency'
                    )
                    fig.update_layout(height=500)
                    visualizations['search_terms_chart'] = fig.to_html(include_plotlyjs=True)
            
            # 2. 内容结构分析图
            if 'content_structure' in analysis_data:
                structure_data = analysis_data['content_structure']
                
                # 标题分布饼图
                if structure_data.get('heading_distribution'):
                    labels = list(structure_data['heading_distribution'].keys())
                    values = list(structure_data['heading_distribution'].values())
                    
                    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
                    fig.update_layout(title="Heading Distribution")
                    visualizations['heading_distribution'] = fig.to_html(include_plotlyjs=True)
                
                # 内容密度指标
                density_metrics = {
                    'Content Density': structure_data.get('content_density', 0),
                    'Link Density': structure_data.get('link_density', 0),
                    'Image Density': structure_data.get('image_density', 0)
                }
                
                fig = go.Figure(data=[
                    go.Bar(x=list(density_metrics.keys()), y=list(density_metrics.values()))
                ])
                fig.update_layout(title="Content Density Metrics", yaxis_title="Density (per 1000 chars)")
                visualizations['density_metrics'] = fig.to_html(include_plotlyjs=True)
            
            # 3. 分类置信度图
            if 'categories' in analysis_data:
                categories = analysis_data['categories']
                if categories:
                    cat_df = pd.DataFrame(categories)
                    
                    fig = px.bar(
                        cat_df, 
                        x='category', 
                        y='confidence',
                        title='Content Category Confidence'
                    )
                    visualizations['categories_chart'] = fig.to_html(include_plotlyjs=True)
            
        except Exception as e:
            print(f"创建可视化图表失败: {e}")
        
        return visualizations
    
    def generate_comprehensive_report(self, url, extracted_data, search_terms, preferences, categories):
        """生成综合分析报告"""
        # 执行各种分析
        search_analysis = self.analyze_search_terms(search_terms)
        structure_analysis = self.analyze_content_structure(extracted_data)
        sentiment = self.sentiment_analysis(extracted_data.get('text_content', ''))
        
        # 生成词云
        wordcloud_path = self.create_word_cloud(extracted_data.get('text_content', ''))
        
        # 准备分析数据
        analysis_data = {
            'search_terms': search_analysis,
            'content_structure': structure_analysis,
            'sentiment': sentiment,
            'categories': categories,
            'preferences': preferences
        }
        
        # 创建可视化
        visualizations = self.create_visualizations(analysis_data)
        
        # 生成报告
        report = {
            'url': url,
            'timestamp': pd.Timestamp.now().isoformat(),
            'basic_info': {
                'title': extracted_data.get('title', ''),
                'meta_description': extracted_data.get('meta_description', ''),
                'total_text_length': len(extracted_data.get('text_content', '')),
                'total_paragraphs': len(extracted_data.get('paragraphs', [])),
                'total_links': len(extracted_data.get('links', [])),
                'total_images': len(extracted_data.get('images', []))
            },
            'analysis_results': analysis_data,
            'visualizations': visualizations,
            'wordcloud_path': wordcloud_path,
            'summary': self._generate_summary(analysis_data)
        }
        
        return report
    
    def _generate_summary(self, analysis_data):
        """生成分析摘要"""
        summary = []
        
        # 搜索词摘要
        if analysis_data.get('search_terms'):
            search_data = analysis_data['search_terms']
            summary.append(f"发现 {search_data.get('total_unique_terms', 0)} 个独特搜索词")
            
            if search_data.get('top_terms'):
                top_term = search_data['top_terms'][0]
                summary.append(f"最高频词汇: '{top_term['term']}' (出现 {top_term['frequency']} 次)")
        
        # 内容结构摘要
        if analysis_data.get('content_structure'):
            structure = analysis_data['content_structure']
            text_stats = structure.get('text_statistics', {})
            summary.append(f"内容包含 {text_stats.get('total_paragraphs', 0)} 个段落，{text_stats.get('total_links', 0)} 个链接")
        
        # 情感分析摘要
        if analysis_data.get('sentiment'):
            sentiment = analysis_data['sentiment']
            summary.append(f"情感倾向: {sentiment.get('sentiment_label', 'neutral')}")
        
        # 分类摘要
        if analysis_data.get('categories'):
            categories = analysis_data['categories']
            if categories:
                top_category = categories[0]
                summary.append(f"主要内容分类: {top_category['category']} (置信度: {top_category['confidence']:.2f})")
        
        return summary