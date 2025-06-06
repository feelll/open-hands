"""
配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 基础配置
BASE_URL = "https://www.3gbizhi.com/meinv/"
DOWNLOAD_DIR = "downloads"
MAX_WORKERS = 5
DELAY_BETWEEN_REQUESTS = 1  # 秒

# 图片分类配置
CATEGORIES = {
    "xgmn": "性感美女",
    "mnxz": "美女写真", 
    "yzmn": "日韩美女",
    "ommn": "欧美美女",
    "mnzp": "美女照片",
    "wgmn": "外国美女",
    "bjnmn": "比基尼美女",
    "dmmn": "翘臀美女"
}

# 微信公众号配置
# 注意: 现在使用动态Token服务，不再需要手动配置WECHAT_ACCESS_TOKEN
# Token会自动从微信API获取并缓存，类似Java RestTemplate的实现方式
WECHAT_APPID = os.getenv('WECHAT_APPID', '')
WECHAT_SECRET = os.getenv('WECHAT_SECRET', '')
# WECHAT_ACCESS_TOKEN 已弃用 - 现在使用 wechat_token_service 动态获取

# 请求头配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# 图片文件扩展名
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']

# 最大下载图片数量（每个分类）
MAX_IMAGES_PER_CATEGORY = 250  # 增加到250张，支持更多页面下载

# 增强爬虫配置
AUTO_DETECT_MAX_PAGES = True  # 自动检测最大页数
CONVERT_WEBP_TO_JPG = True    # 自动转换WebP为JPG
MAX_PAGES_PER_CATEGORY = None # 每个分类最大页数，None表示自动检测
DOWNLOAD_RETRY_TIMES = 3      # 下载重试次数
PAGE_DETECTION_LIMIT = 20     # 页数检测上限