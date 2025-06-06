#!/usr/bin/env python3
"""
自动化内容生产流水线
从图片下载到内容生成的完整自动化流程
"""
import os
import json
import time
import argparse
from datetime import datetime
from typing import Dict, List, Any

from enhanced_image_scraper import EnhancedImageScraper
from wechat_content_generator import WeChatContentGenerator
from content_config import CONTENT_CONFIG, AUTOMATION_CONFIG

class AutoContentPipeline:
    """自动化内容生产流水线"""
    
    def __init__(self):
        self.scraper = EnhancedImageScraper()
        self.generator = WeChatContentGenerator()
        self.config = CONTENT_CONFIG
        self.automation_config = AUTOMATION_CONFIG
        
    def run_full_pipeline(self, 
                         category_code: str,
                         category_name: str,
                         max_pages: int = 2,
                         theme: str = "精选",
                         auto_publish_prep: bool = True) -> Dict[str, Any]:
        """运行完整的内容生产流水线"""
        
        print("🚀 启动自动化内容生产流水线")
        print("=" * 60)
        
        pipeline_start = time.time()
        results = {
            "start_time": datetime.now().isoformat(),
            "category": category_name,
            "theme": theme,
            "steps": {}
        }
        
        try:
            # 步骤1: 下载图片
            print(f"📥 步骤1: 下载图片 - {category_name}")
            download_result = self._download_images(category_code, category_name, max_pages)
            results["steps"]["download"] = download_result
            
            if download_result["success"] and download_result["image_count"] > 0:
                print(f"✅ 下载完成: {download_result['image_count']} 张图片")
                
                # 步骤2: 生成内容
                print(f"\n📝 步骤2: 生成文章内容")
                content_result = self._generate_content(
                    category_name, 
                    download_result["image_count"], 
                    theme
                )
                results["steps"]["content"] = content_result
                print(f"✅ 内容生成完成: {content_result['title']}")
                
                # 步骤3: 处理图片
                print(f"\n🖼️ 步骤3: 处理图片")
                image_result = self._process_images(download_result["download_dir"])
                results["steps"]["images"] = image_result
                print(f"✅ 图片处理完成: {len(image_result['processed_images'])} 张")
                
                # 步骤4: 生成发布材料
                if auto_publish_prep:
                    print(f"\n📄 步骤4: 生成发布材料")
                    publish_result = self._prepare_publishing_materials(
                        content_result["content"], 
                        image_result["processed_images"]
                    )
                    results["steps"]["publishing"] = publish_result
                    print(f"✅ 发布材料生成完成")
                
                # 步骤5: 生成总结报告
                print(f"\n📊 步骤5: 生成总结报告")
                report_result = self._generate_summary_report(results)
                results["steps"]["report"] = report_result
                
                results["success"] = True
                results["total_time"] = time.time() - pipeline_start
                
                print(f"\n🎉 流水线执行完成!")
                print(f"⏱️ 总耗时: {results['total_time']:.2f} 秒")
                
            else:
                results["success"] = False
                results["error"] = "图片下载失败或数量不足"
                print("❌ 图片下载失败，流水线终止")
                
        except Exception as e:
            results["success"] = False
            results["error"] = str(e)
            print(f"💥 流水线执行失败: {e}")
        
        finally:
            results["end_time"] = datetime.now().isoformat()
            
        return results
    
    def _download_images(self, category_code: str, category_name: str, max_pages: int) -> Dict[str, Any]:
        """下载图片"""
        try:
            download_count = self.scraper.scrape_category_enhanced(
                category_code=category_code,
                category_name=category_name,
                max_pages=max_pages
            )
            
            download_dir = os.path.join("downloads", category_name)
            
            return {
                "success": True,
                "image_count": download_count,
                "download_dir": download_dir,
                "category_code": category_code,
                "max_pages": max_pages
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "image_count": 0
            }
    
    def _generate_content(self, category_name: str, image_count: int, theme: str) -> Dict[str, Any]:
        """生成文章内容"""
        try:
            content = self.generator.generate_article_content(
                category=category_name,
                image_count=image_count,
                theme=theme
            )
            
            return {
                "success": True,
                "content": content,
                "title": content["title"],
                "publish_time": content["publish_time"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _process_images(self, download_dir: str) -> Dict[str, Any]:
        """处理图片"""
        try:
            processed_images = self.generator.prepare_images_for_upload(
                image_dir=download_dir,
                output_dir="wechat_ready",
                add_watermark=True,
                create_thumbnails=True
            )
            
            return {
                "success": True,
                "processed_images": processed_images,
                "output_dir": "wechat_ready",
                "total_files": sum(len(img["processed_files"]) for img in processed_images)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "processed_images": []
            }
    
    def _prepare_publishing_materials(self, content: Dict[str, Any], images: List[Dict[str, Any]]) -> Dict[str, Any]:
        """准备发布材料"""
        try:
            # 生成文章草稿
            draft_file = self.generator.generate_wechat_article_draft(content, images)
            
            # 生成检查清单
            checklist_file = self.generator.create_publishing_checklist(content, images)
            
            # 生成素材清单
            materials_file = self._create_materials_list(content, images)
            
            return {
                "success": True,
                "draft_file": draft_file,
                "checklist_file": checklist_file,
                "materials_file": materials_file
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_materials_list(self, content: Dict[str, Any], images: List[Dict[str, Any]]) -> str:
        """创建素材清单"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        materials_file = f"materials_list_{timestamp}.json"
        
        materials = {
            "article_info": {
                "title": content["title"],
                "category": content["category"],
                "theme": content["theme"],
                "publish_time": content["publish_time"],
                "tags": content["tags"]
            },
            "images": [],
            "upload_instructions": [
                "1. 登录微信公众平台",
                "2. 进入素材管理",
                "3. 上传所有图片文件",
                "4. 记录每张图片的media_id",
                "5. 在文章编辑器中插入图片"
            ]
        }
        
        for img_info in images:
            img_data = {
                "index": img_info["index"],
                "files": img_info["processed_files"],
                "original_size": img_info["original_size"],
                "usage": []
            }
            
            # 确定图片用途
            if "cover" in img_info["processed_files"]:
                img_data["usage"].append("封面图")
            if "main" in img_info["processed_files"]:
                img_data["usage"].append("正文图片")
            if "thumbnail" in img_info["processed_files"]:
                img_data["usage"].append("缩略图")
            
            materials["images"].append(img_data)
        
        with open(materials_file, 'w', encoding='utf-8') as f:
            json.dump(materials, f, ensure_ascii=False, indent=2)
        
        return materials_file
    
    def _generate_summary_report(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """生成总结报告"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"pipeline_report_{timestamp}.md"
            
            report_lines = [
                "# 🚀 自动化内容生产流水线报告\n",
                f"**执行时间**: {results['start_time']} - {results['end_time']}",
                f"**分类**: {results['category']}",
                f"**主题**: {results['theme']}",
                f"**状态**: {'✅ 成功' if results['success'] else '❌ 失败'}\n"
            ]
            
            if results["success"]:
                download_step = results["steps"]["download"]
                content_step = results["steps"]["content"]
                images_step = results["steps"]["images"]
                
                report_lines.extend([
                    "## 📊 执行结果\n",
                    f"- **下载图片**: {download_step['image_count']} 张",
                    f"- **处理文件**: {images_step['total_files']} 个",
                    f"- **文章标题**: {content_step['title']}",
                    f"- **建议发布时间**: {content_step['publish_time']}",
                    f"- **总耗时**: {results['total_time']:.2f} 秒\n"
                ])
                
                if "publishing" in results["steps"]:
                    pub_step = results["steps"]["publishing"]
                    report_lines.extend([
                        "## 📁 生成文件\n",
                        f"- **文章草稿**: {pub_step['draft_file']}",
                        f"- **检查清单**: {pub_step['checklist_file']}",
                        f"- **素材清单**: {pub_step['materials_file']}",
                        f"- **图片目录**: wechat_ready/\n"
                    ])
                
                report_lines.extend([
                    "## 📋 下一步操作\n",
                    "1. 查看生成的文章草稿",
                    "2. 上传图片到微信公众平台素材库",
                    "3. 在编辑器中组装文章",
                    "4. 按照检查清单完成发布前检查",
                    "5. 定时发布文章\n"
                ])
            else:
                report_lines.extend([
                    "## ❌ 错误信息\n",
                    f"```\n{results.get('error', '未知错误')}\n```\n"
                ])
            
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write("\n".join(report_lines))
            
            return {
                "success": True,
                "report_file": report_file
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def run_batch_pipeline(self, categories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量运行流水线"""
        print("🔄 启动批量内容生产流水线")
        print(f"📊 计划处理 {len(categories)} 个分类")
        
        batch_results = []
        
        for i, category in enumerate(categories, 1):
            print(f"\n{'='*60}")
            print(f"📂 处理分类 {i}/{len(categories)}: {category['name']}")
            
            result = self.run_full_pipeline(
                category_code=category["code"],
                category_name=category["name"],
                max_pages=category.get("max_pages", 2),
                theme=category.get("theme", "精选")
            )
            
            result["batch_index"] = i
            batch_results.append(result)
            
            # 批次间延迟
            if i < len(categories):
                delay = category.get("delay", 60)  # 默认60秒延迟
                print(f"⏱️ 等待 {delay} 秒后处理下一个分类...")
                time.sleep(delay)
        
        # 生成批量报告
        self._generate_batch_report(batch_results)
        
        return batch_results
    
    def _generate_batch_report(self, batch_results: List[Dict[str, Any]]):
        """生成批量处理报告"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"batch_pipeline_report_{timestamp}.md"
        
        successful = [r for r in batch_results if r["success"]]
        failed = [r for r in batch_results if not r["success"]]
        
        report_lines = [
            "# 📊 批量内容生产流水线报告\n",
            f"**执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**总分类数**: {len(batch_results)}",
            f"**成功**: {len(successful)} 个",
            f"**失败**: {len(failed)} 个",
            f"**成功率**: {len(successful)/len(batch_results)*100:.1f}%\n"
        ]
        
        if successful:
            report_lines.extend([
                "## ✅ 成功处理的分类\n",
                "| 分类 | 图片数 | 文章标题 | 发布时间 |",
                "|------|--------|----------|----------|"
            ])
            
            for result in successful:
                download_info = result["steps"]["download"]
                content_info = result["steps"]["content"]
                report_lines.append(
                    f"| {result['category']} | {download_info['image_count']} | "
                    f"{content_info['title'][:30]}... | {content_info['publish_time']} |"
                )
        
        if failed:
            report_lines.extend([
                "\n## ❌ 失败的分类\n",
                "| 分类 | 错误信息 |",
                "|------|----------|"
            ])
            
            for result in failed:
                error_msg = result.get("error", "未知错误")[:50]
                report_lines.append(f"| {result['category']} | {error_msg}... |")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))
        
        print(f"\n📄 批量报告已生成: {report_file}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="自动化内容生产流水线")
    parser.add_argument("--category", "-c", help="分类代码")
    parser.add_argument("--name", "-n", help="分类名称")
    parser.add_argument("--pages", "-p", type=int, default=2, help="最大页数")
    parser.add_argument("--theme", "-t", default="精选", help="主题")
    parser.add_argument("--batch", "-b", help="批量配置文件")
    
    args = parser.parse_args()
    
    pipeline = AutoContentPipeline()
    
    if args.batch:
        # 批量处理模式
        try:
            with open(args.batch, 'r', encoding='utf-8') as f:
                categories = json.load(f)
            pipeline.run_batch_pipeline(categories)
        except Exception as e:
            print(f"❌ 批量配置文件错误: {e}")
    
    elif args.category and args.name:
        # 单个分类处理模式
        pipeline.run_full_pipeline(
            category_code=args.category,
            category_name=args.name,
            max_pages=args.pages,
            theme=args.theme
        )
    
    else:
        # 演示模式
        print("🎯 演示模式 - 处理美女照片分类")
        pipeline.run_full_pipeline(
            category_code="mnzp",
            category_name="美女照片",
            max_pages=1,
            theme="清新"
        )

if __name__ == "__main__":
    main()