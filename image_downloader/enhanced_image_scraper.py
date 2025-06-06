"""
增强版图片爬虫模块
支持完整分页下载、图片块处理、WebP转JPG格式转换
"""
import os
import re
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import logging
from PIL import Image
import io
from config import *

class EnhancedImageScraper:
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
                logging.FileHandler('enhanced_scraper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_page_content(self, url, retries=3):
        """获取页面内容，支持重试"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                response.encoding = 'utf-8'
                return response.text
            except Exception as e:
                self.logger.warning(f"获取页面失败 {url} (尝试 {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2)
                else:
                    self.logger.error(f"获取页面最终失败 {url}: {e}")
                    return None
                    
    def detect_max_pages(self, category_url):
        """自动检测分类的最大页数"""
        self.logger.info(f"检测分类最大页数: {category_url}")
        
        # 先获取第一页内容
        content = self.get_page_content(category_url)
        if not content:
            return 1
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # 查找分页链接的多种方式
        max_page = 1
        
        # 方式1: 查找分页导航
        pagination_patterns = [
            r'index_(\d+)\.html',
            r'page[_-]?(\d+)',
            r'/(\d+)\.html'
        ]
        
        for pattern in pagination_patterns:
            links = soup.find_all('a', href=re.compile(pattern))
            for link in links:
                href = link.get('href', '')
                matches = re.findall(pattern, href)
                for match in matches:
                    try:
                        page_num = int(match)
                        max_page = max(max_page, page_num)
                    except ValueError:
                        continue
        
        # 方式2: 查找"下一页"或"最后一页"链接
        next_page_texts = ['下一页', '下页', '末页', '最后一页', 'next', 'last']
        for text in next_page_texts:
            links = soup.find_all('a', string=re.compile(text, re.I))
            for link in links:
                href = link.get('href', '')
                matches = re.findall(r'index_(\d+)\.html', href)
                for match in matches:
                    try:
                        page_num = int(match)
                        max_page = max(max_page, page_num)
                    except ValueError:
                        continue
        
        # 方式3: 尝试访问更高页数来确定边界
        test_page = max_page + 1
        while test_page <= max_page + 10:  # 最多测试10页
            test_url = f"{category_url}index_{test_page}.html"
            test_content = self.get_page_content(test_url)
            if test_content and self.has_valid_content(test_content):
                max_page = test_page
                test_page += 1
            else:
                break
                
        self.logger.info(f"检测到最大页数: {max_page}")
        return max_page
        
    def has_valid_content(self, content):
        """检查页面是否有有效内容"""
        if not content:
            return False
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # 检查是否有图片链接
        image_links = soup.find_all('a', href=re.compile(r'pic\d+\.html'))
        return len(image_links) > 0
        
    def parse_category_all_pages(self, category_url, max_pages=None):
        """解析分类的所有页面，获取所有图片详情页链接"""
        if max_pages is None:
            max_pages = self.detect_max_pages(category_url)
        
        self.logger.info(f"开始解析分类所有页面，共 {max_pages} 页")
        
        all_detail_urls = []
        
        for page in range(1, max_pages + 1):
            if page == 1:
                url = category_url
            else:
                url = f"{category_url}index_{page}.html"
                
            self.logger.info(f"正在解析第 {page}/{max_pages} 页: {url}")
            
            content = self.get_page_content(url)
            if not content:
                self.logger.warning(f"跳过页面 {page}")
                continue
                
            soup = BeautifulSoup(content, 'html.parser')
            
            # 查找图片详情页链接
            image_links = []
            
            # 多种方式查找链接
            patterns = [
                r'/meinv/\w+/pic\d+\.html',
                r'pic\d+\.html'
            ]
            
            for pattern in patterns:
                links = soup.find_all('a', href=re.compile(pattern))
                image_links.extend(links)
            
            # 也查找class为特定值的链接
            class_patterns = ['imgw', 'pic-item', 'image-link']
            for class_name in class_patterns:
                links = soup.find_all('a', class_=class_name)
                image_links.extend(links)
                
            if not image_links:
                self.logger.warning(f"页面 {page} 没有找到图片链接")
                continue
                
            page_urls = []
            for link in image_links:
                href = link.get('href')
                if href:
                    if href.startswith('http'):
                        full_url = href
                    else:
                        full_url = urljoin(category_url, href)
                    if full_url not in all_detail_urls:
                        all_detail_urls.append(full_url)
                        page_urls.append(full_url)
                        
            self.logger.info(f"页面 {page} 找到 {len(page_urls)} 个新的图片详情页")
            time.sleep(DELAY_BETWEEN_REQUESTS)
            
        self.logger.info(f"总共找到 {len(all_detail_urls)} 个图片详情页")
        return all_detail_urls
        
    def get_all_images_from_detail_page(self, detail_url):
        """从详情页获取所有图片URL（包括分页的图片）"""
        self.logger.debug(f"解析详情页: {detail_url}")
        
        all_image_urls = []
        
        # 获取主页面
        content = self.get_page_content(detail_url)
        if not content:
            return []
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # 获取主图片
        main_images = self.extract_images_from_page(soup, detail_url)
        all_image_urls.extend(main_images)
        
        # 查找图片集中的其他图片链接
        # 查找类似 pic2192_1.html, pic2192_2.html 的链接
        base_pic_id = re.search(r'pic(\d+)', detail_url)
        if base_pic_id:
            pic_id = base_pic_id.group(1)
            
            # 查找同组图片链接
            sub_image_links = soup.find_all('a', href=re.compile(f'pic{pic_id}_\\d+\\.html'))
            
            for sub_link in sub_image_links:
                sub_href = sub_link.get('href')
                if sub_href:
                    if not sub_href.startswith('http'):
                        sub_href = urljoin(detail_url, sub_href)
                    
                    # 获取子页面的图片
                    sub_content = self.get_page_content(sub_href)
                    if sub_content:
                        sub_soup = BeautifulSoup(sub_content, 'html.parser')
                        sub_images = self.extract_images_from_page(sub_soup, sub_href)
                        all_image_urls.extend(sub_images)
                        time.sleep(0.5)  # 短暂延迟
        
        # 去重
        unique_urls = []
        for url in all_image_urls:
            if url not in unique_urls and self.is_valid_image_url(url):
                unique_urls.append(url)
                
        self.logger.debug(f"详情页 {detail_url} 找到 {len(unique_urls)} 张图片")
        return unique_urls
        
    def extract_images_from_page(self, soup, base_url):
        """从页面提取图片URL"""
        image_urls = []
        
        # 方式1: 查找img标签
        img_tags = soup.find_all('img')
        for img in img_tags:
            src = img.get('src') or img.get('data-src') or img.get('lay-src') or img.get('data-original')
            if src and self.is_valid_image_url(src):
                if not src.startswith('http'):
                    src = urljoin(base_url, src)
                image_urls.append(src)
        
        # 方式2: 查找JavaScript中的图片URL
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                urls = re.findall(r'https?://[^\s"\']+\.(?:jpg|jpeg|png|gif|webp)', script.string)
                for url in urls:
                    if self.is_valid_image_url(url):
                        image_urls.append(url)
        
        # 方式3: 查找特定域名的图片
        pic_domain_patterns = [
            r'https?://pic\.3gbizhi\.com/[^\s"\']+\.(?:jpg|jpeg|png|gif|webp)',
            r'https?://[^/]+\.3gbizhi\.com/[^\s"\']+\.(?:jpg|jpeg|png|gif|webp)'
        ]
        
        page_text = str(soup)
        for pattern in pic_domain_patterns:
            urls = re.findall(pattern, page_text)
            for url in urls:
                if self.is_valid_image_url(url):
                    image_urls.append(url)
        
        return image_urls
        
    def is_valid_image_url(self, url):
        """检查是否为有效的图片URL"""
        if not url:
            return False
        
        # 过滤掉明显不是图片的URL
        invalid_keywords = ['loading', 'icon', 'logo', 'avatar', 'thumb', 'favicon', 'xin_hui']
        for keyword in invalid_keywords:
            if keyword in url.lower():
                return False
                
        # 检查是否包含图片扩展名
        return any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'])
        
    def convert_webp_to_jpg(self, image_data):
        """将WebP格式转换为JPG格式"""
        try:
            # 使用PIL打开图片
            image = Image.open(io.BytesIO(image_data))
            
            # 如果是RGBA模式，转换为RGB
            if image.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # 保存为JPG格式
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=95)
            return output.getvalue()
            
        except Exception as e:
            self.logger.error(f"WebP转JPG失败: {e}")
            return image_data  # 返回原始数据
            
    def download_image(self, image_url, save_path, convert_webp=True):
        """下载单张图片，支持WebP转JPG"""
        try:
            response = self.session.get(image_url, timeout=30, stream=True)
            response.raise_for_status()
            
            # 读取图片数据
            image_data = b''
            for chunk in response.iter_content(chunk_size=8192):
                image_data += chunk
            
            # 检查是否为WebP格式并转换
            if convert_webp and (image_url.lower().endswith('.webp') or 
                               response.headers.get('content-type', '').startswith('image/webp')):
                self.logger.debug(f"转换WebP格式: {os.path.basename(save_path)}")
                image_data = self.convert_webp_to_jpg(image_data)
                
                # 更改文件扩展名为.jpg
                if save_path.lower().endswith('.webp'):
                    save_path = save_path[:-5] + '.jpg'
            
            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 保存文件
            with open(save_path, 'wb') as f:
                f.write(image_data)
                
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
            filename = f"image_{index:04d}.jpg"
        else:
            # 如果是webp格式，改为jpg
            if filename.lower().endswith('.webp'):
                filename = filename[:-5] + '.jpg'
        
        return filename
        
    def scrape_category_enhanced(self, category_code, category_name, max_pages=None, max_images=None):
        """增强版分类爬取，支持完整分页和格式转换"""
        self.logger.info(f"开始增强爬取分类: {category_name} ({category_code})")
        
        category_url = f"{BASE_URL}{category_code}/"
        save_dir = os.path.join(DOWNLOAD_DIR, category_name)
        
        # 获取所有页面的图片详情页链接
        detail_urls = self.parse_category_all_pages(category_url, max_pages)
        
        if not detail_urls:
            self.logger.warning(f"分类 {category_name} 没有找到任何图片")
            return 0
        
        self.logger.info(f"分类 {category_name} 找到 {len(detail_urls)} 个图片详情页")
        
        downloaded_count = 0
        max_images = max_images or MAX_IMAGES_PER_CATEGORY
        
        # 使用进度条
        with tqdm(total=min(len(detail_urls), max_images), desc=f"下载{category_name}") as pbar:
            for detail_url in detail_urls:
                if downloaded_count >= max_images:
                    break
                    
                # 获取详情页的所有图片
                image_urls = self.get_all_images_from_detail_page(detail_url)
                
                for image_url in image_urls:
                    if downloaded_count >= max_images:
                        break
                        
                    filename = self.get_image_filename(image_url, downloaded_count)
                    save_path = os.path.join(save_dir, filename)
                    
                    # 检查文件是否已存在
                    if os.path.exists(save_path):
                        self.logger.debug(f"文件已存在，跳过: {filename}")
                        continue
                        
                    if self.download_image(image_url, save_path, convert_webp=True):
                        downloaded_count += 1
                        self.logger.info(f"下载成功: {filename} (WebP→JPG)")
                        pbar.update(1)
                    else:
                        self.logger.warning(f"下载失败: {filename}")
                        
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                    
                # 详情页之间的延迟
                time.sleep(DELAY_BETWEEN_REQUESTS * 0.5)
                
        self.logger.info(f"分类 {category_name} 下载完成，共下载 {downloaded_count} 张图片")
        return downloaded_count
        
    def scrape_all_categories_enhanced(self, max_pages_per_category=None, max_images_per_category=None):
        """增强版爬取所有分类"""
        self.logger.info("开始增强爬取所有分类")
        
        total_downloaded = 0
        results = {}
        
        for category_code, category_name in CATEGORIES.items():
            try:
                self.logger.info(f"\n{'='*50}")
                self.logger.info(f"开始处理分类: {category_name}")
                self.logger.info(f"{'='*50}")
                
                count = self.scrape_category_enhanced(
                    category_code, 
                    category_name, 
                    max_pages_per_category,
                    max_images_per_category
                )
                
                total_downloaded += count
                results[category_name] = count
                
                self.logger.info(f"分类 {category_name} 完成，下载 {count} 张图片")
                
                # 分类之间的延迟
                time.sleep(2)
                
            except Exception as e:
                self.logger.error(f"爬取分类 {category_name} 失败: {e}")
                results[category_name] = 0
                
        # 输出总结
        self.logger.info(f"\n{'='*60}")
        self.logger.info("所有分类爬取完成！")
        self.logger.info(f"{'='*60}")
        self.logger.info(f"总共下载: {total_downloaded} 张图片")
        
        for category_name, count in results.items():
            self.logger.info(f"  {category_name}: {count} 张")
            
        return total_downloaded, results

def main():
    """主函数 - 演示增强爬虫功能"""
    scraper = EnhancedImageScraper()
    
    print("=== 增强版图片爬虫 ===")
    print("功能特点:")
    print("✅ 自动检测并下载所有分页")
    print("✅ 下载每个图片块的所有图片")
    print("✅ 自动将WebP格式转换为JPG")
    print("✅ 智能重试和错误处理")
    print()
    
    choice = input("选择操作:\n1. 爬取单个分类\n2. 爬取所有分类\n3. 测试单个详情页\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        # 显示可用分类
        print("\n可用分类:")
        for i, (code, name) in enumerate(CATEGORIES.items(), 1):
            print(f"  {i}. {name} ({code})")
        
        try:
            cat_index = int(input("\n请选择分类序号: ")) - 1
            categories_list = list(CATEGORIES.items())
            if 0 <= cat_index < len(categories_list):
                code, name = categories_list[cat_index]
                max_pages = input("最大页数 (回车使用自动检测): ").strip()
                max_pages = int(max_pages) if max_pages else None
                
                count = scraper.scrape_category_enhanced(code, name, max_pages)
                print(f"\n✅ 完成！共下载 {count} 张图片")
            else:
                print("❌ 无效的分类序号")
        except ValueError:
            print("❌ 输入格式错误")
            
    elif choice == "2":
        max_pages = input("每个分类最大页数 (回车使用自动检测): ").strip()
        max_pages = int(max_pages) if max_pages else None
        
        max_images = input(f"每个分类最大图片数 (回车使用默认{MAX_IMAGES_PER_CATEGORY}): ").strip()
        max_images = int(max_images) if max_images else None
        
        total, results = scraper.scrape_all_categories_enhanced(max_pages, max_images)
        print(f"\n✅ 全部完成！总共下载 {total} 张图片")
        
    elif choice == "3":
        test_url = input("请输入详情页URL: ").strip()
        if test_url:
            images = scraper.get_all_images_from_detail_page(test_url)
            print(f"\n找到 {len(images)} 张图片:")
            for i, url in enumerate(images, 1):
                print(f"  {i}. {url}")
        else:
            print("❌ URL不能为空")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main()