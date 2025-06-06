#!/usr/bin/env python3
"""
增强版图片下载脚本
支持完整分页下载和WebP转JPG
"""
import os
import sys
import time
import logging
from enhanced_image_scraper import EnhancedImageScraper
from config import CATEGORIES, MAX_IMAGES_PER_CATEGORY

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('download_enhanced.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def main():
    """主函数"""
    print("🚀 增强版图片下载器")
    print("=" * 50)
    print("功能特点:")
    print("✅ 自动检测并下载所有分页")
    print("✅ 下载每个图片块的所有图片") 
    print("✅ 自动将WebP格式转换为JPG")
    print("✅ 智能重试和错误处理")
    print("✅ 详细的下载进度显示")
    print("=" * 50)
    
    setup_logging()
    
    # 显示当前配置
    print(f"📁 下载目录: downloads/")
    print(f"📊 每分类最大图片数: {MAX_IMAGES_PER_CATEGORY}")
    print(f"🏷️  可用分类: {len(CATEGORIES)} 个")
    
    for i, (code, name) in enumerate(CATEGORIES.items(), 1):
        print(f"   {i:2d}. {name}")
    
    print("\n" + "=" * 50)
    
    # 用户选择
    print("请选择下载模式:")
    print("1. 下载所有分类 (推荐)")
    print("2. 选择特定分类下载")
    print("3. 自定义配置下载")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    scraper = EnhancedImageScraper()
    
    try:
        if choice == "1":
            # 下载所有分类
            print(f"\n🚀 开始下载所有 {len(CATEGORIES)} 个分类...")
            print("⏰ 预计耗时: 根据网络速度和图片数量而定")
            
            confirm = input("\n确认开始下载? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                start_time = time.time()
                total, results = scraper.scrape_all_categories_enhanced()
                end_time = time.time()
                
                print(f"\n🎉 下载完成!")
                print(f"⏱️  总耗时: {end_time - start_time:.1f} 秒")
                print(f"📊 总下载: {total} 张图片")
                print("\n📋 各分类下载情况:")
                for category, count in results.items():
                    status = "✅" if count > 0 else "❌"
                    print(f"   {status} {category}: {count} 张")
            else:
                print("❌ 取消下载")
                
        elif choice == "2":
            # 选择特定分类
            print("\n请选择要下载的分类 (输入序号，多个用逗号分隔):")
            selected = input("选择: ").strip()
            
            try:
                indices = [int(x.strip()) - 1 for x in selected.split(',')]
                categories_list = list(CATEGORIES.items())
                selected_categories = []
                
                for i in indices:
                    if 0 <= i < len(categories_list):
                        selected_categories.append(categories_list[i])
                
                if not selected_categories:
                    print("❌ 没有选择有效的分类")
                    return
                
                print(f"\n🚀 开始下载选中的 {len(selected_categories)} 个分类:")
                for code, name in selected_categories:
                    print(f"   - {name}")
                
                confirm = input("\n确认开始下载? (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    total_downloaded = 0
                    for code, name in selected_categories:
                        print(f"\n📁 正在下载: {name}")
                        count = scraper.scrape_category_enhanced(code, name)
                        total_downloaded += count
                        print(f"✅ {name} 完成: {count} 张图片")
                    
                    print(f"\n🎉 选择下载完成! 总共下载 {total_downloaded} 张图片")
                else:
                    print("❌ 取消下载")
                    
            except ValueError:
                print("❌ 输入格式错误")
                
        elif choice == "3":
            # 自定义配置
            print("\n⚙️ 自定义配置:")
            
            try:
                max_pages = input(f"每个分类最大页数 (回车使用自动检测): ").strip()
                max_pages = int(max_pages) if max_pages else None
                
                max_images = input(f"每个分类最大图片数 (回车使用默认{MAX_IMAGES_PER_CATEGORY}): ").strip()
                max_images = int(max_images) if max_images else MAX_IMAGES_PER_CATEGORY
                
                print(f"\n📋 配置确认:")
                print(f"   最大页数: {'自动检测' if max_pages is None else max_pages}")
                print(f"   最大图片数: {max_images}")
                
                confirm = input("\n确认开始下载? (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    start_time = time.time()
                    total, results = scraper.scrape_all_categories_enhanced(max_pages, max_images)
                    end_time = time.time()
                    
                    print(f"\n🎉 自定义下载完成!")
                    print(f"⏱️  总耗时: {end_time - start_time:.1f} 秒")
                    print(f"📊 总下载: {total} 张图片")
                else:
                    print("❌ 取消下载")
                    
            except ValueError:
                print("❌ 输入格式错误")
                
        else:
            print("❌ 无效选择")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断下载")
        print("已下载的图片已保存到downloads目录")
    except Exception as e:
        print(f"\n❌ 下载过程中发生错误: {e}")
        logging.exception("下载错误")
    
    print("\n📁 下载的图片保存在 downloads/ 目录中")
    print("📄 详细日志保存在 download_enhanced.log 文件中")

if __name__ == "__main__":
    main()