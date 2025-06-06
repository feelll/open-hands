"""
微信公众号图片上传模块
"""
import os
import json
import requests
import time
import logging
from config import *
from wechat_token_service import get_token_service

class WeChatUploader:
    def __init__(self):
        self.setup_logging()
        # 使用新的Token服务
        self.token_service = get_token_service()
        
    def setup_logging(self):
        """设置日志"""
        self.logger = logging.getLogger(__name__)
        
    def get_access_token(self):
        """获取微信公众号access_token - 使用动态Token服务"""
        try:
            token = self.token_service.get_token_string()
            if token:
                self.logger.debug("通过Token服务获取access_token成功")
                return token
            else:
                self.logger.error("通过Token服务获取access_token失败")
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
            
    def upload_permanent_image(self, image_path, category_name=None):
        """
        上传永久素材图片，支持分类标记
        
        Args:
            image_path: 图片路径
            category_name: 分类名称，会添加到文件名前缀中
        """
        access_token = self.get_access_token()
        if not access_token:
            return None
            
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={access_token}&type=image"
        
        try:
            # 获取原始文件名
            original_filename = os.path.basename(image_path)
            
            # 如果有分类名称，添加到文件名前缀
            if category_name:
                name, ext = os.path.splitext(original_filename)
                # 创建带分类前缀的文件名，格式：[分类]原文件名
                upload_filename = f"[{category_name}]{name}{ext}"
            else:
                upload_filename = original_filename
            
            with open(image_path, 'rb') as f:
                files = {'media': (upload_filename, f, 'image/jpeg')}
                response = requests.post(url, files=files)
                
            data = response.json()
            
            if 'media_id' in data:
                self.logger.info(f"永久图片上传成功: {upload_filename} -> {data['media_id']}")
                return {
                    'media_id': data['media_id'],
                    'url': data.get('url', ''),
                    'original_filename': original_filename,
                    'upload_filename': upload_filename,
                    'category': category_name
                }
            else:
                self.logger.error(f"永久图片上传失败: {data}")
                return None
                
        except Exception as e:
            self.logger.error(f"上传永久图片异常 {image_path}: {e}")
            return None
            
    def upload_images_from_directory(self, directory_path, permanent=True):
        """
        批量上传目录中的图片，自动根据目录名设置分类
        
        Args:
            directory_path: 图片目录路径
            permanent: 是否上传为永久素材
        """
        if not os.path.exists(directory_path):
            self.logger.error(f"目录不存在: {directory_path}")
            return []
            
        uploaded_media_ids = []
        category_name = os.path.basename(directory_path)  # 使用目录名作为分类名
        
        self.logger.info(f"开始上传分类 [{category_name}] 的图片...")
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            # 检查是否为图片文件
            if not any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                continue
                
            if permanent:
                # 传递分类名称到上传方法
                result = self.upload_permanent_image(file_path, category_name)
                if result:
                    uploaded_media_ids.append({
                        'original_filename': result['original_filename'],
                        'upload_filename': result['upload_filename'],
                        'media_id': result['media_id'],
                        'url': result.get('url', ''),
                        'category': category_name,
                        'file_path': file_path,
                        'upload_time': time.strftime('%Y-%m-%d %H:%M:%S')
                    })
            else:
                media_id = self.upload_image(file_path)
                if media_id:
                    uploaded_media_ids.append({
                        'original_filename': filename,
                        'upload_filename': f"[{category_name}]{filename}",
                        'media_id': media_id,
                        'url': '',
                        'category': category_name,
                        'file_path': file_path,
                        'upload_time': time.strftime('%Y-%m-%d %H:%M:%S')
                    })
                
            # 避免请求过于频繁
            time.sleep(1)
            
        self.logger.info(f"分类 [{category_name}] 上传完成，共上传 {len(uploaded_media_ids)} 张图片")
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
            
    def generate_category_report(self, uploaded_data, report_file="category_report.md"):
        """
        生成分类报告，方便在微信后台查找图片
        
        Args:
            uploaded_data: 上传数据列表
            report_file: 报告文件名
        """
        try:
            # 按分类整理数据
            categories = {}
            for item in uploaded_data:
                category = item.get('category', '未分类')
                if category not in categories:
                    categories[category] = []
                categories[category].append(item)
            
            # 生成Markdown报告
            report_content = []
            report_content.append("# 微信公众号图片分类上传报告\n")
            report_content.append(f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            report_content.append(f"总计上传图片: {len(uploaded_data)} 张\n")
            report_content.append(f"分类数量: {len(categories)} 个\n\n")
            
            # 分类统计
            report_content.append("## 📊 分类统计\n")
            for category, items in categories.items():
                report_content.append(f"- **{category}**: {len(items)} 张图片")
            report_content.append("\n")
            
            # 详细分类信息
            report_content.append("## 📁 分类详情\n")
            for category, items in categories.items():
                report_content.append(f"### {category} ({len(items)} 张)\n")
                report_content.append("| 上传文件名 | Media ID | 上传时间 |")
                report_content.append("|-----------|----------|----------|")
                
                for item in items:
                    upload_filename = item.get('upload_filename', item.get('original_filename', ''))
                    media_id = item.get('media_id', '')
                    upload_time = item.get('upload_time', '')
                    report_content.append(f"| {upload_filename} | `{media_id}` | {upload_time} |")
                
                report_content.append("\n")
            
            # 查找指南
            report_content.append("## 🔍 微信后台查找指南\n")
            report_content.append("在微信公众号后台素材管理中，您可以通过以下方式快速找到对应分类的图片：\n")
            report_content.append("1. **按文件名搜索**: 所有图片都以 `[分类名]` 开头，如 `[性感美女]`")
            report_content.append("2. **按Media ID搜索**: 使用上表中的Media ID进行精确查找")
            report_content.append("3. **按上传时间筛选**: 根据上传时间范围筛选\n")
            
            # 分类快速搜索
            report_content.append("## 🚀 快速搜索关键词\n")
            for category in categories.keys():
                report_content.append(f"- 搜索 `[{category}]` 查看该分类所有图片")
            
            # 写入文件
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_content))
            
            self.logger.info(f"分类报告已生成: {report_file}")
            return report_file
            
        except Exception as e:
            self.logger.error(f"生成分类报告失败: {e}")
            return None
            
    def get_category_summary(self, uploaded_data):
        """
        获取分类摘要信息
        
        Args:
            uploaded_data: 上传数据列表
            
        Returns:
            dict: 分类摘要信息
        """
        categories = {}
        total_count = len(uploaded_data)
        
        for item in uploaded_data:
            category = item.get('category', '未分类')
            if category not in categories:
                categories[category] = {
                    'count': 0,
                    'media_ids': [],
                    'upload_filenames': []
                }
            
            categories[category]['count'] += 1
            categories[category]['media_ids'].append(item.get('media_id', ''))
            categories[category]['upload_filenames'].append(
                item.get('upload_filename', item.get('original_filename', ''))
            )
        
        return {
            'total_count': total_count,
            'category_count': len(categories),
            'categories': categories,
            'summary_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
            
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