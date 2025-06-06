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
        
        # 方式1: 查找分页导航中的index_数字.html模式
        pagination_links = soup.find_all('a', href=re.compile(r'index_(\d+)\.html'))
        for link in pagination_links:
            href = link.get('href', '')
            matches = re.findall(r'index_(\d+)\.html', href)
            for match in matches:
                try:
                    page_num = int(match)
                    max_page = max(max_page, page_num)
                except ValueError:
                    continue
        
        # 方式2: 查找分页导航区域
        # 查找包含分页的div或ul元素
        pagination_containers = soup.find_all(['div', 'ul'], class_=re.compile(r'page|pagination'))
        for container in pagination_containers:
            links = container.find_all('a', href=re.compile(r'index_(\d+)\.html'))
            for link in links:
                href = link.get('href', '')
                matches = re.findall(r'index_(\d+)\.html', href)
                for match in matches:
                    try:
                        page_num = int(match)
                        max_page = max(max_page, page_num)
                    except ValueError:
                        continue
        
        # 方式3: 查找"下一页"或"最后一页"链接
        next_page_texts = ['下一页', '下页', '末页', '最后一页', 'next', 'last', '尾页']
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
        
        # 方式4: 如果没有找到分页链接，尝试测试几页
        if max_page == 1:
            self.logger.info("未找到分页链接，尝试测试页面存在性")
            for test_page in range(2, 6):  # 测试2-5页
                test_url = f"{category_url}index_{test_page}.html"
                test_content = self.get_page_content(test_url)
                if test_content and self.has_valid_content(test_content):
                    max_page = test_page
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
            
            # 重点查找 class="imgw" 的链接
            imgw_links = soup.find_all('a', class_='imgw')
            
            if not imgw_links:
                # 备用方案：查找其他可能的链接
                patterns = [
                    r'/meinv/\w+/pic\d+\.html',
                    r'pic\d+\.html'
                ]
                
                imgw_links = []
                for pattern in patterns:
                    links = soup.find_all('a', href=re.compile(pattern))
                    imgw_links.extend(links)
                
                # 也查找其他class
                class_patterns = ['pic-item', 'image-link']
                for class_name in class_patterns:
                    links = soup.find_all('a', class_=class_name)
                    imgw_links.extend(links)
                
            if not imgw_links:
                self.logger.warning(f"页面 {page} 没有找到图片链接")
                continue
                
            page_urls = []
            for link in imgw_links:
                href = link.get('href')
                if href and 'pic' in href and '.html' in href:
                    if href.startswith('http'):
                        full_url = href
                    else:
                        full_url = urljoin(category_url, href)
                    
                    # 只添加主图片页面（不包含_数字的）
                    if not re.search(r'pic\d+_\d+\.html', full_url):
                        if full_url not in all_detail_urls:
                            all_detail_urls.append(full_url)
                            page_urls.append(full_url)
                        
            self.logger.info(f"页面 {page} 找到 {len(page_urls)} 个新的图片详情页")
            time.sleep(DELAY_BETWEEN_REQUESTS)
            
        self.logger.info(f"总共找到 {len(all_detail_urls)} 个图片详情页")
        return all_detail_urls
        
    def get_all_images_from_detail_page(self, detail_url):
        """从详情页获取所有图片URL（包括图片集中的所有图片）"""
        self.logger.debug(f"解析详情页: {detail_url}")
        
        all_image_urls = []
        processed_urls = set()
        
        # 获取主页面图片
        main_image = self.extract_wallphotos_image(detail_url)
        if main_image:
            all_image_urls.append(main_image)
            processed_urls.add(detail_url)
        
        # 查找图片集中的其他图片
        # 从URL中提取pic ID，如pic2192 -> 2192
        base_pic_match = re.search(r'pic(\d+)\.html', detail_url)
        if base_pic_match:
            pic_id = base_pic_match.group(1)
            base_url = detail_url.replace(f'pic{pic_id}.html', '')
            
            # 固定获取图片集中的所有图片（每个图块固定最多5张）
            for i in range(2, 6):  # 从_2到_5，固定5张图片
                sub_url = f"{base_url}pic{pic_id}_{i}.html"
                
                if sub_url in processed_urls:
                    continue
                    
                sub_image = self.extract_wallphotos_image(sub_url)
                if sub_image:
                    all_image_urls.append(sub_image)
                    processed_urls.add(sub_url)
                    self.logger.debug(f"找到子图片: pic{pic_id}_{i}")
                
                time.sleep(0.1)  # 短暂延迟避免请求过快
        
        # 去重并验证
        unique_urls = []
        for url in all_image_urls:
            if url and url not in unique_urls and self.is_valid_image_url(url):
                unique_urls.append(url)
                
        self.logger.info(f"详情页 {detail_url} 找到 {len(unique_urls)} 张图片")
        return unique_urls
        
    def extract_wallphotos_image(self, page_url):
        """从页面中提取 wallphotos 图片URL"""
        try:
            content = self.get_page_content(page_url)
            if not content:
                return None
                
            soup = BeautifulSoup(content, 'html.parser')
            
            # 查找 class="img-table-cell wallphotos" 中的图片
            wallphotos_div = soup.find('div', class_='img-table-cell wallphotos')
            if wallphotos_div:
                img_tag = wallphotos_div.find('img')
                if img_tag:
                    img_src = img_tag.get('src')
                    if img_src and self.is_valid_image_url(img_src):
                        if not img_src.startswith('http'):
                            img_src = urljoin(page_url, img_src)
                        return img_src
            
            # 备用方案：查找其他可能的图片
            # 查找包含 uploadmark 或 uploads 的图片URL
            img_tags = soup.find_all('img')
            for img in img_tags:
                src = img.get('src')
                if src and ('uploadmark' in src or 'uploads' in src) and self.is_valid_image_url(src):
                    if not src.startswith('http'):
                        src = urljoin(page_url, src)
                    return src
            
            return None
            
        except Exception as e:
            self.logger.debug(f"提取图片失败 {page_url}: {e}")
            return None
        
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
            
    def get_image_filename(self, image_url, detail_url=None, sub_index=None):
        """生成有意义的图片文件名"""
        parsed_url = urlparse(image_url)
        original_filename = os.path.basename(parsed_url.path)
        
        # 尝试从详情页URL提取pic ID
        pic_id = None
        if detail_url:
            pic_match = re.search(r'pic(\d+)', detail_url)
            if pic_match:
                pic_id = pic_match.group(1)
        
        # 如果有原始文件名且包含有效信息
        if original_filename and '.' in original_filename:
            name, ext = os.path.splitext(original_filename)
            
            # 如果是webp格式，改为jpg
            if ext.lower() == '.webp':
                ext = '.jpg'
            
            # 如果有pic ID，添加到文件名前缀
            if pic_id:
                if sub_index is not None:
                    filename = f"pic{pic_id}_{sub_index}_{name}{ext}"
                else:
                    filename = f"pic{pic_id}_{name}{ext}"
            else:
                filename = f"{name}{ext}"
        else:
            # 无法从URL获取文件名，使用pic ID生成
            if pic_id:
                if sub_index is not None:
                    filename = f"pic{pic_id}_{sub_index}.jpg"
                else:
                    filename = f"pic{pic_id}.jpg"
            else:
                # 最后备用方案
                timestamp = int(time.time())
                filename = f"image_{timestamp}.jpg"
        
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
        processed_blocks = 0
        max_images = max_images or MAX_IMAGES_PER_CATEGORY
        
        # 计算预期图片数量（每个图块5张图片）
        expected_images_per_block = 5
        total_expected = len(detail_urls) * expected_images_per_block
        
        self.logger.info(f"预期下载图片数量: {len(detail_urls)} 个图块 × {expected_images_per_block} 张/块 = {total_expected} 张")
        
        # 使用进度条，显示图块进度
        with tqdm(total=len(detail_urls), desc=f"下载{category_name}图块", unit="块") as pbar:
            for detail_url in detail_urls:
                if downloaded_count >= max_images:
                    break
                    
                # 获取详情页的所有图片（固定5张）
                image_urls = self.get_all_images_from_detail_page(detail_url)
                
                if not image_urls:
                    self.logger.warning(f"图块没有找到图片: {detail_url}")
                    pbar.update(1)
                    continue
                
                block_downloaded = 0
                # 下载该图块的所有图片
                for i, image_url in enumerate(image_urls):
                    if downloaded_count >= max_images:
                        break
                    
                    # 生成有意义的文件名
                    sub_index = i + 1 if len(image_urls) > 1 else None
                    filename = self.get_image_filename(image_url, detail_url, sub_index)
                    save_path = os.path.join(save_dir, filename)
                    
                    # 检查文件是否已存在
                    if os.path.exists(save_path):
                        self.logger.debug(f"文件已存在，跳过: {filename}")
                        block_downloaded += 1
                        downloaded_count += 1
                        continue
                        
                    if self.download_image(image_url, save_path, convert_webp=True):
                        downloaded_count += 1
                        block_downloaded += 1
                        self.logger.debug(f"下载成功: {filename} (WebP→JPG)")
                    else:
                        self.logger.warning(f"下载失败: {filename}")
                        
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                
                processed_blocks += 1
                pbar.set_postfix({
                    '已下载': f"{downloaded_count}张",
                    '本块': f"{block_downloaded}/{len(image_urls)}张"
                })
                pbar.update(1)
                    
                # 图块之间的延迟
                time.sleep(DELAY_BETWEEN_REQUESTS * 0.3)
                
        self.logger.info(f"分类 {category_name} 下载完成:")
        self.logger.info(f"  处理图块: {processed_blocks}/{len(detail_urls)}")
        self.logger.info(f"  下载图片: {downloaded_count} 张")
        self.logger.info(f"  平均每块: {downloaded_count/processed_blocks:.1f} 张" if processed_blocks > 0 else "  平均每块: 0 张")
        
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