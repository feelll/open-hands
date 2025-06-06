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
WECHAT_APPID = os.getenv('WECHAT_APPID', '')
WECHAT_SECRET = os.getenv('WECHAT_SECRET', '')
WECHAT_ACCESS_TOKEN = os.getenv('WECHAT_ACCESS_TOKEN', '')

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
MAX_IMAGES_PER_CATEGORY = 5