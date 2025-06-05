import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
from urllib.parse import urljoin, urlparse
import json

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_page_content(self, url, use_selenium=False):
        """获取网页内容"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"获取页面内容失败: {e}")
            return None
    
    def extract_text_content(self, html_content):
        """提取文本内容"""
        if not html_content:
            return {}
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 移除脚本和样式标签
        for script in soup(["script", "style"]):
            script.decompose()
        
        # 提取各种内容
        data = {
            'title': soup.title.string if soup.title else '',
            'meta_description': '',
            'meta_keywords': '',
            'headings': [],
            'paragraphs': [],
            'links': [],
            'images': [],
            'text_content': soup.get_text()
        }
        
        # 提取meta信息
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            data['meta_description'] = meta_desc.get('content', '')
        
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            data['meta_keywords'] = meta_keywords.get('content', '')
        
        # 提取标题
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            for heading in headings:
                data['headings'].append({
                    'level': i,
                    'text': heading.get_text().strip()
                })
        
        # 提取段落
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text().strip()
            if text:
                data['paragraphs'].append(text)
        
        # 提取链接
        links = soup.find_all('a', href=True)
        for link in links:
            data['links'].append({
                'text': link.get_text().strip(),
                'href': link['href']
            })
        
        # 提取图片
        images = soup.find_all('img', src=True)
        for img in images:
            data['images'].append({
                'src': img['src'],
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            })
        
        return data
    
    def extract_search_terms(self, text_content):
        """提取可能的搜索词"""
        if not text_content:
            return []
        
        # 清理文本
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text_content)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 提取关键词（简单的基于频率的方法）
        words = text.split()
        word_freq = {}
        
        for word in words:
            word = word.lower()
            if len(word) > 2:  # 过滤短词
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # 按频率排序
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:50]  # 返回前50个高频词
    
    def analyze_user_preferences(self, extracted_data):
        """分析用户喜好"""
        preferences = {
            'content_types': [],
            'topics': [],
            'language_style': '',
            'media_preference': {
                'text': 0,
                'images': 0,
                'links': 0
            }
        }
        
        # 分析内容类型
        if extracted_data.get('headings'):
            preferences['content_types'].append('structured_content')
        
        if len(extracted_data.get('paragraphs', [])) > 5:
            preferences['content_types'].append('detailed_articles')
        
        if len(extracted_data.get('images', [])) > 3:
            preferences['content_types'].append('visual_content')
        
        if len(extracted_data.get('links', [])) > 10:
            preferences['content_types'].append('reference_heavy')
        
        # 媒体偏好统计
        preferences['media_preference']['text'] = len(extracted_data.get('paragraphs', []))
        preferences['media_preference']['images'] = len(extracted_data.get('images', []))
        preferences['media_preference']['links'] = len(extracted_data.get('links', []))
        
        return preferences
    
    def categorize_content(self, extracted_data):
        """内容分类"""
        categories = []
        
        title = extracted_data.get('title', '').lower()
        meta_desc = extracted_data.get('meta_description', '').lower()
        text_content = extracted_data.get('text_content', '').lower()
        
        # 定义分类关键词
        category_keywords = {
            'technology': ['tech', 'software', 'programming', 'computer', 'ai', 'machine learning', 'data'],
            'business': ['business', 'finance', 'market', 'economy', 'investment', 'company'],
            'education': ['education', 'learning', 'course', 'tutorial', 'study', 'university'],
            'entertainment': ['entertainment', 'movie', 'music', 'game', 'fun', 'celebrity'],
            'health': ['health', 'medical', 'fitness', 'wellness', 'doctor', 'medicine'],
            'news': ['news', 'breaking', 'latest', 'update', 'report', 'journalism'],
            'sports': ['sports', 'football', 'basketball', 'soccer', 'athlete', 'game'],
            'travel': ['travel', 'tourism', 'vacation', 'destination', 'hotel', 'flight']
        }
        
        # 检查每个分类
        for category, keywords in category_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in title:
                    score += 3
                if keyword in meta_desc:
                    score += 2
                if keyword in text_content:
                    score += 1
            
            if score > 0:
                categories.append({
                    'category': category,
                    'confidence': min(score / 10, 1.0)  # 归一化到0-1
                })
        
        # 按置信度排序
        categories.sort(key=lambda x: x['confidence'], reverse=True)
        return categories[:3]  # 返回前3个最可能的分类