#!/usr/bin/env python3
"""
完整工作流程脚本
集成增强下载 + 分类上传功能
"""
import os
import time
import logging
from enhanced_image_scraper import EnhancedImageScraper
from category_manager import CategoryManager
from config import CATEGORIES, MAX_IMAGES_PER_CATEGORY

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('complete_workflow.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def print_banner():
    """打印横幅"""
    print("🎯 完整图片工作流程")
    print("=" * 60)
    print("功能包括:")
    print("📥 1. 增强下载 - 完整分页 + WebP转JPG")
    print("📤 2. 分类上传 - 自动分类标记上传到微信")
    print("📊 3. 详细报告 - 下载和上传统计报告")
    print("=" * 60)

def show_categories():
    """显示可用分类"""
    print(f"\n📁 可用分类 ({len(CATEGORIES)} 个):")
    for i, (code, name) in enumerate(CATEGORIES.items(), 1):
        print(f"   {i:2d}. {name} ({code})")

def download_phase(scraper, selected_categories=None, max_pages=None, max_images=None):
    """下载阶段"""
    print("\n" + "🔽" * 20 + " 下载阶段 " + "🔽" * 20)
    
    if selected_categories:
        # 下载选定分类
        total_downloaded = 0
        download_results = {}
        
        for code, name in selected_categories:
            print(f"\n📁 正在下载分类: {name}")
            count = scraper.scrape_category_enhanced(code, name, max_pages, max_images)
            total_downloaded += count
            download_results[name] = count
            print(f"✅ {name} 下载完成: {count} 张图片")
            
    else:
        # 下载所有分类
        print("\n🚀 开始下载所有分类...")
        total_downloaded, download_results = scraper.scrape_all_categories_enhanced(max_pages, max_images)
    
    print(f"\n📊 下载阶段完成:")
    print(f"   总下载: {total_downloaded} 张图片")
    for category, count in download_results.items():
        status = "✅" if count > 0 else "❌"
        print(f"   {status} {category}: {count} 张")
    
    return total_downloaded, download_results

def upload_phase(manager, selected_categories=None):
    """上传阶段"""
    print("\n" + "🔼" * 20 + " 上传阶段 " + "🔼" * 20)
    
    if not manager.upload_enabled:
        print("⚠️ 微信上传功能不可用，跳过上传阶段")
        print("   请配置 WECHAT_APPID 和 WECHAT_SECRET 环境变量")
        return 0, {}
    
    if selected_categories:
        # 上传选定分类
        category_names = [name for code, name in selected_categories]
        upload_results = manager.upload_multiple_categories(category_names)
    else:
        # 上传所有分类
        upload_results = manager.upload_all_categories()
    
    if upload_results:
        # 生成上传报告
        timestamp = int(time.time())
        files = manager.save_results_with_report(upload_results, f"complete_workflow_{timestamp}")
        
        # 获取上传摘要
        summary = manager.get_category_summary(upload_results)
        
        print(f"\n📊 上传阶段完成:")
        print(f"   总上传: {summary['total_count']} 张图片")
        print(f"   分类数: {summary['category_count']} 个")
        
        for category, info in summary['categories'].items():
            print(f"   ✅ {category}: {info['count']} 张")
        
        print(f"\n📄 报告文件:")
        print(f"   📋 JSON日志: {files['log_file']}")
        print(f"   📊 分类报告: {files['report_file']}")
        
        return summary['total_count'], summary['categories']
    else:
        print("❌ 没有图片被上传")
        return 0, {}

def generate_final_report(download_results, upload_results, start_time, end_time):
    """生成最终报告"""
    print("\n" + "📋" * 20 + " 最终报告 " + "📋" * 20)
    
    total_time = end_time - start_time
    total_downloaded = sum(download_results.values())
    total_uploaded = sum(info['count'] if isinstance(info, dict) else info for info in upload_results.values())
    
    print(f"⏱️  总耗时: {total_time:.1f} 秒 ({total_time/60:.1f} 分钟)")
    print(f"📥 总下载: {total_downloaded} 张图片")
    print(f"📤 总上传: {total_uploaded} 张图片")
    print(f"📊 成功率: {(total_uploaded/total_downloaded*100):.1f}%" if total_downloaded > 0 else "N/A")
    
    print(f"\n📋 分类详情:")
    all_categories = set(download_results.keys()) | set(upload_results.keys())
    
    for category in sorted(all_categories):
        downloaded = download_results.get(category, 0)
        uploaded = upload_results.get(category, {}).get('count', 0) if isinstance(upload_results.get(category), dict) else upload_results.get(category, 0)
        
        print(f"   📁 {category}:")
        print(f"      📥 下载: {downloaded} 张")
        print(f"      📤 上传: {uploaded} 张")
        
        if downloaded > 0:
            success_rate = (uploaded / downloaded * 100)
            print(f"      ✅ 成功率: {success_rate:.1f}%")

def main():
    """主函数"""
    print_banner()
    setup_logging()
    
    # 初始化组件
    scraper = EnhancedImageScraper()
    manager = CategoryManager()
    
    show_categories()
    
    print("\n请选择工作流程:")
    print("1. 完整流程 (下载 + 上传所有分类)")
    print("2. 选择分类 (下载 + 上传指定分类)")
    print("3. 仅下载 (不上传)")
    print("4. 仅上传 (使用现有图片)")
    print("5. 自定义配置")
    
    choice = input("\n请输入选择 (1-5): ").strip()
    
    start_time = time.time()
    download_results = {}
    upload_results = {}
    
    try:
        if choice == "1":
            # 完整流程 - 所有分类
            print("\n🚀 开始完整工作流程 (所有分类)")
            
            confirm = input("确认开始? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("❌ 取消操作")
                return
            
            # 下载阶段
            total_downloaded, download_results = download_phase(scraper)
            
            # 上传阶段
            if total_downloaded > 0:
                total_uploaded, upload_results = upload_phase(manager)
            else:
                print("⚠️ 没有下载到图片，跳过上传阶段")
                
        elif choice == "2":
            # 选择分类
            print("\n请选择要处理的分类 (输入序号，多个用逗号分隔):")
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
                
                print(f"\n🎯 选中的分类:")
                for code, name in selected_categories:
                    print(f"   - {name}")
                
                confirm = input("\n确认开始? (y/N): ").strip().lower()
                if confirm not in ['y', 'yes']:
                    print("❌ 取消操作")
                    return
                
                # 下载阶段
                total_downloaded, download_results = download_phase(scraper, selected_categories)
                
                # 上传阶段
                if total_downloaded > 0:
                    total_uploaded, upload_results = upload_phase(manager, selected_categories)
                else:
                    print("⚠️ 没有下载到图片，跳过上传阶段")
                    
            except ValueError:
                print("❌ 输入格式错误")
                return
                
        elif choice == "3":
            # 仅下载
            print("\n📥 仅下载模式")
            
            max_pages = input("每分类最大页数 (回车使用自动检测): ").strip()
            max_pages = int(max_pages) if max_pages else None
            
            max_images = input(f"每分类最大图片数 (回车使用默认{MAX_IMAGES_PER_CATEGORY}): ").strip()
            max_images = int(max_images) if max_images else None
            
            total_downloaded, download_results = download_phase(scraper, None, max_pages, max_images)
            
        elif choice == "4":
            # 仅上传
            print("\n📤 仅上传模式 (使用downloads目录中的现有图片)")
            
            confirm = input("确认开始上传? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("❌ 取消操作")
                return
                
            total_uploaded, upload_results = upload_phase(manager)
            
        elif choice == "5":
            # 自定义配置
            print("\n⚙️ 自定义配置模式")
            
            # 配置参数
            max_pages = input("每分类最大页数 (回车使用自动检测): ").strip()
            max_pages = int(max_pages) if max_pages else None
            
            max_images = input(f"每分类最大图片数 (回车使用默认{MAX_IMAGES_PER_CATEGORY}): ").strip()
            max_images = int(max_images) if max_images else None
            
            upload_choice = input("是否上传到微信? (y/N): ").strip().lower()
            should_upload = upload_choice in ['y', 'yes']
            
            print(f"\n📋 配置确认:")
            print(f"   最大页数: {'自动检测' if max_pages is None else max_pages}")
            print(f"   最大图片数: {max_images}")
            print(f"   上传微信: {'是' if should_upload else '否'}")
            
            confirm = input("\n确认开始? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                print("❌ 取消操作")
                return
            
            # 下载阶段
            total_downloaded, download_results = download_phase(scraper, None, max_pages, max_images)
            
            # 上传阶段
            if should_upload and total_downloaded > 0:
                total_uploaded, upload_results = upload_phase(manager)
            elif not should_upload:
                print("⏭️ 跳过上传阶段")
            else:
                print("⚠️ 没有下载到图片，跳过上传阶段")
                
        else:
            print("❌ 无效选择")
            return
            
    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断操作")
        print("已处理的内容已保存")
    except Exception as e:
        print(f"\n❌ 操作过程中发生错误: {e}")
        logging.exception("工作流程错误")
    
    # 生成最终报告
    end_time = time.time()
    if download_results or upload_results:
        generate_final_report(download_results, upload_results, start_time, end_time)
    
    print(f"\n📁 图片保存位置: downloads/ 目录")
    print(f"📄 详细日志: complete_workflow.log")
    print("\n🎉 工作流程完成!")

if __name__ == "__main__":
    main()