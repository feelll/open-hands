"""
图片爬虫模块
"""
import os
import re
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import logging
from config import *

class ImageScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_page_content(self, url):
        """获取页面内容"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            self.logger.error(f"获取页面失败 {url}: {e}")
            return None
            
    def parse_category_page(self, category_url, max_pages=3):
        """解析分类页面，获取图片详情页链接"""
        image_detail_urls = []
        
        for page in range(1, max_pages + 1):
            if page == 1:
                url = category_url
            else:
                url = f"{category_url}index_{page}.html"
                
            self.logger.info(f"正在解析页面: {url}")
            content = self.get_page_content(url)
            if not content:
                continue
                
            soup = BeautifulSoup(content, 'html.parser')
            
            # 查找图片链接 - 多种方式
            image_links = []
            
            # 方式1: 查找包含pic的链接
            links1 = soup.find_all('a', href=re.compile(r'/meinv/\w+/pic\d+\.html'))
            image_links.extend(links1)
            
            # 方式2: 查找class为imgw的链接
            links2 = soup.find_all('a', class_='imgw')
            image_links.extend(links2)
            
            # 方式3: 查找包含图片的链接
            links3 = soup.find_all('a', href=re.compile(r'pic\d+\.html'))
            image_links.extend(links3)
            
            if not image_links:
                self.logger.warning(f"页面 {url} 没有找到图片链接")
                # 打印页面内容的一部分用于调试
                self.logger.debug(f"页面内容片段: {content[:1000]}")
                break
                
            for link in image_links:
                href = link.get('href')
                if href:
                    if href.startswith('http'):
                        full_url = href
                    else:
                        full_url = urljoin(BASE_URL, href)
                    if full_url not in image_detail_urls:
                        image_detail_urls.append(full_url)
                    
            self.logger.info(f"页面 {url} 找到 {len(set([l.get('href') for l in image_links]))} 个图片链接")
            time.sleep(DELAY_BETWEEN_REQUESTS)
            
        return list(set(image_detail_urls))  # 去重
        
    def get_image_urls_from_detail_page(self, detail_url):
        """从详情页获取实际图片URL"""
        content = self.get_page_content(detail_url)
        if not content:
            return []
            
        soup = BeautifulSoup(content, 'html.parser')
        image_urls = []
        
        # 查找图片URL的多种方式
        # 方式1: 查找img标签
        img_tags = soup.find_all('img')
        for img in img_tags:
            # 检查多种src属性
            src = img.get('src') or img.get('data-src') or img.get('lay-src') or img.get('data-original')
            if src and any(ext in src.lower() for ext in IMAGE_EXTENSIONS):
                # 过滤掉loading图片和小图标
                if 'loading' not in src.lower() and 'icon' not in src.lower() and 'logo' not in src.lower():
                    if not src.startswith('http'):
                        src = urljoin(detail_url, src)
                    image_urls.append(src)
                
        # 方式2: 查找JavaScript中的图片URL
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                # 查找图片URL模式
                urls = re.findall(r'https?://[^\s"\']+\.(?:jpg|jpeg|png|gif|webp)', script.string)
                for url in urls:
                    if 'loading' not in url.lower() and 'icon' not in url.lower():
                        image_urls.append(url)
        
        # 方式3: 查找特定的图片容器
        img_containers = soup.find_all(['div', 'span'], class_=re.compile(r'img|pic|photo'))
        for container in img_containers:
            imgs = container.find_all('img')
            for img in imgs:
                src = img.get('src') or img.get('data-src') or img.get('lay-src')
                if src and any(ext in src.lower() for ext in IMAGE_EXTENSIONS):
                    if 'loading' not in src.lower():
                        if not src.startswith('http'):
                            src = urljoin(detail_url, src)
                        image_urls.append(src)
                
        # 去重并过滤
        unique_urls = []
        for url in image_urls:
            if url not in unique_urls and self.is_valid_image_url(url):
                unique_urls.append(url)
                
        return unique_urls
        
    def is_valid_image_url(self, url):
        """检查是否为有效的图片URL"""
        if not url:
            return False
        
        # 过滤掉明显不是图片的URL
        invalid_keywords = ['loading', 'icon', 'logo', 'avatar', 'thumb', 'favicon']
        for keyword in invalid_keywords:
            if keyword in url.lower():
                return False
                
        # 检查是否包含图片扩展名
        return any(ext in url.lower() for ext in IMAGE_EXTENSIONS)
        
    def download_image(self, image_url, save_path):
        """下载单张图片"""
        try:
            response = self.session.get(image_url, timeout=30, stream=True)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            return True
        except Exception as e:
            self.logger.error(f"下载图片失败 {image_url}: {e}")
            return False
            
    def get_image_filename(self, image_url, index=0):
        """生成图片文件名"""
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path)
        
        if not filename or '.' not in filename:
            # 如果无法从URL获取文件名，使用索引
            ext = '.jpg'  # 默认扩展名
            for ext_check in IMAGE_EXTENSIONS:
                if ext_check in image_url.lower():
                    ext = ext_check
                    break
            filename = f"image_{index:04d}{ext}"
            
        return filename
        
    def scrape_category(self, category_code, category_name):
        """爬取指定分类的图片"""
        self.logger.info(f"开始爬取分类: {category_name} ({category_code})")
        
        category_url = f"{BASE_URL}{category_code}/"
        save_dir = os.path.join(DOWNLOAD_DIR, category_name)
        
        # 获取图片详情页链接
        detail_urls = self.parse_category_page(category_url)
        self.logger.info(f"找到 {len(detail_urls)} 个图片详情页")
        
        downloaded_count = 0
        
        for detail_url in tqdm(detail_urls[:MAX_IMAGES_PER_CATEGORY], desc=f"下载{category_name}"):
            if downloaded_count >= MAX_IMAGES_PER_CATEGORY:
                break
                
            # 获取图片URL
            image_urls = self.get_image_urls_from_detail_page(detail_url)
            
            for i, image_url in enumerate(image_urls):
                if downloaded_count >= MAX_IMAGES_PER_CATEGORY:
                    break
                    
                filename = self.get_image_filename(image_url, downloaded_count)
                save_path = os.path.join(save_dir, filename)
                
                # 检查文件是否已存在
                if os.path.exists(save_path):
                    continue
                    
                if self.download_image(image_url, save_path):
                    downloaded_count += 1
                    self.logger.info(f"下载成功: {filename}")
                    
                time.sleep(DELAY_BETWEEN_REQUESTS)
                
        self.logger.info(f"分类 {category_name} 下载完成，共下载 {downloaded_count} 张图片")
        return downloaded_count
        
    def scrape_all_categories(self):
        """爬取所有分类的图片"""
        total_downloaded = 0
        
        for category_code, category_name in CATEGORIES.items():
            try:
                count = self.scrape_category(category_code, category_name)
                total_downloaded += count
            except Exception as e:
                self.logger.error(f"爬取分类 {category_name} 失败: {e}")
                
        self.logger.info(f"所有分类爬取完成，总共下载 {total_downloaded} 张图片")
        return total_downloaded