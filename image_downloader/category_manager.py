#!/usr/bin/env python3
"""
微信公众号图片分类管理工具
提供分类上传、查询、报告生成等功能
"""
import os
import json
import time
import logging
from typing import List, Dict, Optional
from wechat_uploader import WeChatUploader
from config import DOWNLOAD_DIR, CATEGORIES

class CategoryManager:
    """分类管理器"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.uploader = WeChatUploader()
            self.upload_enabled = True
        except Exception as e:
            self.logger.warning(f"微信上传功能不可用: {e}")
            self.uploader = None
            self.upload_enabled = False
        
    def get_available_categories(self) -> List[Dict]:
        """
        获取可用的分类目录
        
        Returns:
            List[Dict]: 分类信息列表
        """
        categories = []
        
        if not os.path.exists(DOWNLOAD_DIR):
            self.logger.warning(f"下载目录不存在: {DOWNLOAD_DIR}")
            return categories
        
        for item in os.listdir(DOWNLOAD_DIR):
            item_path = os.path.join(DOWNLOAD_DIR, item)
            if os.path.isdir(item_path):
                # 统计图片数量
                image_files = [f for f in os.listdir(item_path) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'))]
                
                categories.append({
                    'name': item,
                    'path': item_path,
                    'image_count': len(image_files),
                    'images': image_files
                })
        
        return sorted(categories, key=lambda x: x['name'])
    
    def upload_category(self, category_name: str, permanent: bool = True) -> Optional[List[Dict]]:
        """
        上传指定分类的图片
        
        Args:
            category_name: 分类名称
            permanent: 是否上传为永久素材
            
        Returns:
            List[Dict]: 上传结果列表
        """
        if not self.upload_enabled:
            self.logger.error("微信上传功能不可用，请检查配置")
            return None
            
        category_path = os.path.join(DOWNLOAD_DIR, category_name)
        
        if not os.path.exists(category_path):
            self.logger.error(f"分类目录不存在: {category_path}")
            return None
        
        self.logger.info(f"开始上传分类: {category_name}")
        result = self.uploader.upload_images_from_directory(category_path, permanent)
        self.logger.info(f"分类 {category_name} 上传完成，共 {len(result)} 张图片")
        
        return result
    
    def upload_multiple_categories(self, category_names: List[str], permanent: bool = True) -> List[Dict]:
        """
        上传多个分类的图片
        
        Args:
            category_names: 分类名称列表
            permanent: 是否上传为永久素材
            
        Returns:
            List[Dict]: 所有上传结果
        """
        all_results = []
        
        for category_name in category_names:
            result = self.upload_category(category_name, permanent)
            if result:
                all_results.extend(result)
        
        return all_results
    
    def upload_all_categories(self, permanent: bool = True) -> List[Dict]:
        """
        上传所有分类的图片
        
        Args:
            permanent: 是否上传为永久素材
            
        Returns:
            List[Dict]: 所有上传结果
        """
        return self.uploader.upload_all_categories(DOWNLOAD_DIR)
    
    def generate_upload_plan(self) -> Dict:
        """
        生成上传计划
        
        Returns:
            Dict: 上传计划信息
        """
        categories = self.get_available_categories()
        
        plan = {
            'total_categories': len(categories),
            'total_images': sum(cat['image_count'] for cat in categories),
            'categories': categories,
            'estimated_time': sum(cat['image_count'] for cat in categories) * 2,  # 每张图片约2秒
            'plan_time': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return plan
    
    def save_results_with_report(self, upload_results: List[Dict], prefix: str = "upload") -> Dict[str, str]:
        """
        保存上传结果并生成报告
        
        Args:
            upload_results: 上传结果列表
            prefix: 文件名前缀
            
        Returns:
            Dict[str, str]: 生成的文件路径
        """
        timestamp = int(time.time())
        
        # 保存JSON日志
        log_file = f"{prefix}_log_{timestamp}.json"
        self.uploader.save_upload_log(upload_results, log_file)
        
        # 生成Markdown报告
        report_file = f"{prefix}_report_{timestamp}.md"
        self.uploader.generate_category_report(upload_results, report_file)
        
        return {
            'log_file': log_file,
            'report_file': report_file
        }
    
    def get_category_statistics(self) -> Dict:
        """
        获取分类统计信息
        
        Returns:
            Dict: 统计信息
        """
        categories = self.get_available_categories()
        
        stats = {
            'total_categories': len(categories),
            'total_images': sum(cat['image_count'] for cat in categories),
            'categories_detail': {},
            'largest_category': None,
            'smallest_category': None,
            'average_images_per_category': 0
        }
        
        if categories:
            # 详细统计
            for cat in categories:
                stats['categories_detail'][cat['name']] = {
                    'image_count': cat['image_count'],
                    'path': cat['path']
                }
            
            # 最大最小分类
            stats['largest_category'] = max(categories, key=lambda x: x['image_count'])
            stats['smallest_category'] = min(categories, key=lambda x: x['image_count'])
            
            # 平均值
            stats['average_images_per_category'] = stats['total_images'] / len(categories)
        
        return stats
    
    def search_images_by_category(self, category_name: str) -> Optional[Dict]:
        """
        按分类搜索图片
        
        Args:
            category_name: 分类名称
            
        Returns:
            Dict: 分类信息和图片列表
        """
        categories = self.get_available_categories()
        
        for cat in categories:
            if cat['name'] == category_name:
                return cat
        
        return None
    
    def preview_upload_filenames(self, category_names: List[str] = None) -> Dict:
        """
        预览上传后的文件名
        
        Args:
            category_names: 指定分类名称列表，None表示所有分类
            
        Returns:
            Dict: 预览信息
        """
        categories = self.get_available_categories()
        
        if category_names:
            categories = [cat for cat in categories if cat['name'] in category_names]
        
        preview = {
            'categories': {},
            'total_images': 0
        }
        
        for cat in categories:
            category_preview = {
                'original_count': cat['image_count'],
                'upload_filenames': []
            }
            
            for img_file in cat['images']:
                name, ext = os.path.splitext(img_file)
                upload_filename = f"[{cat['name']}]{name}{ext}"
                category_preview['upload_filenames'].append({
                    'original': img_file,
                    'upload': upload_filename
                })
            
            preview['categories'][cat['name']] = category_preview
            preview['total_images'] += cat['image_count']
        
        return preview

def main():
    """主函数 - 命令行界面"""
    import argparse
    
    parser = argparse.ArgumentParser(description='微信公众号图片分类管理工具')
    parser.add_argument('--action', choices=['list', 'upload', 'plan', 'stats', 'preview'], 
                       default='list', help='执行的操作')
    parser.add_argument('--categories', nargs='+', help='指定分类名称')
    parser.add_argument('--all', action='store_true', help='处理所有分类')
    parser.add_argument('--permanent', action='store_true', default=True, help='上传为永久素材')
    
    args = parser.parse_args()
    
    # 设置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    manager = CategoryManager()
    
    if args.action == 'list':
        # 列出所有分类
        categories = manager.get_available_categories()
        print(f"📁 发现 {len(categories)} 个分类:")
        for i, cat in enumerate(categories, 1):
            print(f"  {i:2d}. {cat['name']} ({cat['image_count']} 张图片)")
    
    elif args.action == 'upload':
        # 上传图片
        if args.all:
            print("🚀 上传所有分类...")
            results = manager.upload_all_categories(args.permanent)
        elif args.categories:
            print(f"🚀 上传指定分类: {', '.join(args.categories)}")
            results = manager.upload_multiple_categories(args.categories, args.permanent)
        else:
            print("❌ 请指定要上传的分类或使用 --all 上传所有分类")
            return
        
        if results:
            files = manager.save_results_with_report(results, "category_upload")
            print(f"✅ 上传完成！共 {len(results)} 张图片")
            print(f"📄 报告文件: {files['report_file']}")
            print(f"📋 日志文件: {files['log_file']}")
    
    elif args.action == 'plan':
        # 生成上传计划
        plan = manager.generate_upload_plan()
        print("📋 上传计划:")
        print(f"  总分类数: {plan['total_categories']}")
        print(f"  总图片数: {plan['total_images']}")
        print(f"  预计耗时: {plan['estimated_time']} 秒 ({plan['estimated_time']//60} 分钟)")
        print("  分类详情:")
        for cat in plan['categories']:
            print(f"    - {cat['name']}: {cat['image_count']} 张")
    
    elif args.action == 'stats':
        # 显示统计信息
        stats = manager.get_category_statistics()
        print("📊 分类统计:")
        print(f"  总分类数: {stats['total_categories']}")
        print(f"  总图片数: {stats['total_images']}")
        if stats['total_categories'] > 0:
            print(f"  平均每分类: {stats['average_images_per_category']:.1f} 张")
            print(f"  最大分类: {stats['largest_category']['name']} ({stats['largest_category']['image_count']} 张)")
            print(f"  最小分类: {stats['smallest_category']['name']} ({stats['smallest_category']['image_count']} 张)")
    
    elif args.action == 'preview':
        # 预览上传文件名
        preview = manager.preview_upload_filenames(args.categories)
        print("👀 上传文件名预览:")
        for cat_name, cat_info in preview['categories'].items():
            print(f"\n📁 {cat_name} ({cat_info['original_count']} 张):")
            for i, file_info in enumerate(cat_info['upload_filenames'][:3], 1):
                print(f"  {i}. {file_info['original']} → {file_info['upload']}")
            if cat_info['original_count'] > 3:
                print(f"  ... 还有 {cat_info['original_count'] - 3} 张图片")

if __name__ == "__main__":
    main()