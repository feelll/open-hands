"""
微信公众号图片上传模块
"""
import os
import json
import requests
import time
import logging
from config import *

class WeChatUploader:
    def __init__(self):
        self.access_token = None
        self.token_expires_at = 0
        self.setup_logging()
        
    def setup_logging(self):
        """设置日志"""
        self.logger = logging.getLogger(__name__)
        
    def get_access_token(self):
        """获取微信公众号access_token"""
        if not WECHAT_APPID or not WECHAT_SECRET:
            self.logger.error("微信公众号配置不完整")
            return None
            
        # 检查token是否过期
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
            
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            'grant_type': 'client_credential',
            'appid': WECHAT_APPID,
            'secret': WECHAT_SECRET
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'access_token' in data:
                self.access_token = data['access_token']
                self.token_expires_at = time.time() + data.get('expires_in', 7200) - 300  # 提前5分钟过期
                self.logger.info("获取access_token成功")
                return self.access_token
            else:
                self.logger.error(f"获取access_token失败: {data}")
                return None
                
        except Exception as e:
            self.logger.error(f"获取access_token异常: {e}")
            return None
            
    def upload_image(self, image_path):
        """上传图片到微信公众号素材库"""
        access_token = self.get_access_token()
        if not access_token:
            return False
            
        url = f"https://api.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image"
        
        try:
            with open(image_path, 'rb') as f:
                files = {'media': (os.path.basename(image_path), f, 'image/jpeg')}
                response = requests.post(url, files=files)
                
            data = response.json()
            
            if 'media_id' in data:
                self.logger.info(f"图片上传成功: {os.path.basename(image_path)} -> {data['media_id']}")
                return data['media_id']
            else:
                self.logger.error(f"图片上传失败: {data}")
                return None
                
        except Exception as e:
            self.logger.error(f"上传图片异常 {image_path}: {e}")
            return None
            
    def upload_permanent_image(self, image_path):
        """上传永久素材图片"""
        access_token = self.get_access_token()
        if not access_token:
            return False
            
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
        
        try:
            with open(image_path, 'rb') as f:
                files = {'media': (os.path.basename(image_path), f, 'image/jpeg')}
                response = requests.post(url, files=files)
                
            data = response.json()
            
            if 'media_id' in data:
                self.logger.info(f"永久图片上传成功: {os.path.basename(image_path)} -> {data['media_id']}")
                return data['media_id']
            else:
                self.logger.error(f"永久图片上传失败: {data}")
                return None
                
        except Exception as e:
            self.logger.error(f"上传永久图片异常 {image_path}: {e}")
            return None
            
    def upload_images_from_directory(self, directory_path, permanent=True):
        """批量上传目录中的图片"""
        if not os.path.exists(directory_path):
            self.logger.error(f"目录不存在: {directory_path}")
            return []
            
        uploaded_media_ids = []
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            # 检查是否为图片文件
            if not any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                continue
                
            if permanent:
                media_id = self.upload_permanent_image(file_path)
            else:
                media_id = self.upload_image(file_path)
                
            if media_id:
                uploaded_media_ids.append({
                    'filename': filename,
                    'media_id': media_id,
                    'category': os.path.basename(directory_path)
                })
                
            # 避免请求过于频繁
            time.sleep(1)
            
        return uploaded_media_ids
        
    def upload_all_categories(self, base_directory=DOWNLOAD_DIR):
        """上传所有分类的图片"""
        all_uploaded = []
        
        if not os.path.exists(base_directory):
            self.logger.error(f"下载目录不存在: {base_directory}")
            return all_uploaded
            
        for category_name in CATEGORIES.values():
            category_dir = os.path.join(base_directory, category_name)
            
            if os.path.exists(category_dir):
                self.logger.info(f"开始上传分类: {category_name}")
                uploaded = self.upload_images_from_directory(category_dir)
                all_uploaded.extend(uploaded)
                self.logger.info(f"分类 {category_name} 上传完成，共上传 {len(uploaded)} 张图片")
            else:
                self.logger.warning(f"分类目录不存在: {category_dir}")
                
        return all_uploaded
        
    def save_upload_log(self, uploaded_data, log_file="upload_log.json"):
        """保存上传日志"""
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(uploaded_data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"上传日志已保存到: {log_file}")
        except Exception as e:
            self.logger.error(f"保存上传日志失败: {e}")
            
    def get_material_count(self):
        """获取素材总数"""
        access_token = self.get_access_token()
        if not access_token:
            return None
            
        url = f"https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token={access_token}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if 'voice_count' in data:  # 成功响应包含各种素材数量
                self.logger.info(f"素材库统计: {data}")
                return data
            else:
                self.logger.error(f"获取素材统计失败: {data}")
                return None
                
        except Exception as e:
            self.logger.error(f"获取素材统计异常: {e}")
            return None