#!/usr/bin/env python3
"""
微信公众号分类上传演示
展示如何根据downloads目录结构进行分类上传
"""
import os
import json
import logging
from wechat_uploader import WeChatUploader
from config import DOWNLOAD_DIR

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('category_upload.log', encoding='utf-8')
        ]
    )

def demo_category_upload():
    """演示分类上传功能"""
    print("=== 微信公众号分类上传演示 ===\n")
    
    setup_logging()
    
    try:
        # 创建上传器实例
        uploader = WeChatUploader()
        
        # 检查下载目录
        if not os.path.exists(DOWNLOAD_DIR):
            print(f"❌ 下载目录不存在: {DOWNLOAD_DIR}")
            return
        
        # 获取所有分类目录
        categories = []
        for item in os.listdir(DOWNLOAD_DIR):
            item_path = os.path.join(DOWNLOAD_DIR, item)
            if os.path.isdir(item_path):
                categories.append(item)
        
        if not categories:
            print(f"❌ 在 {DOWNLOAD_DIR} 中没有找到分类目录")
            return
        
        print(f"📁 发现 {len(categories)} 个分类目录:")
        for i, category in enumerate(categories, 1):
            category_path = os.path.join(DOWNLOAD_DIR, category)
            image_count = len([f for f in os.listdir(category_path) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'))])
            print(f"   {i}. {category} ({image_count} 张图片)")
        
        print("\n" + "="*50)
        
        # 选择上传方式
        print("请选择上传方式:")
        print("1. 上传所有分类")
        print("2. 选择特定分类上传")
        print("3. 仅生成上传预览（不实际上传）")
        
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == "1":
            # 上传所有分类
            print("\n🚀 开始上传所有分类...")
            all_uploaded = uploader.upload_all_categories(DOWNLOAD_DIR)
            process_upload_results(uploader, all_uploaded)
            
        elif choice == "2":
            # 选择特定分类
            print("\n请选择要上传的分类 (输入序号，多个用逗号分隔):")
            selected = input("选择: ").strip()
            
            try:
                indices = [int(x.strip()) - 1 for x in selected.split(',')]
                selected_categories = [categories[i] for i in indices if 0 <= i < len(categories)]
                
                if not selected_categories:
                    print("❌ 没有选择有效的分类")
                    return
                
                print(f"\n🚀 开始上传选中的 {len(selected_categories)} 个分类...")
                all_uploaded = []
                
                for category in selected_categories:
                    category_path = os.path.join(DOWNLOAD_DIR, category)
                    uploaded = uploader.upload_images_from_directory(category_path)
                    all_uploaded.extend(uploaded)
                
                process_upload_results(uploader, all_uploaded)
                
            except ValueError:
                print("❌ 输入格式错误")
                return
                
        elif choice == "3":
            # 仅预览
            print("\n👀 生成上传预览...")
            preview_upload(categories)
            
        else:
            print("❌ 无效选择")
            
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

def process_upload_results(uploader, uploaded_data):
    """处理上传结果"""
    if not uploaded_data:
        print("❌ 没有成功上传任何图片")
        return
    
    print(f"\n✅ 上传完成！总计上传 {len(uploaded_data)} 张图片")
    
    # 保存上传日志
    log_file = f"category_upload_log_{int(time.time())}.json"
    uploader.save_upload_log(uploaded_data, log_file)
    
    # 生成分类报告
    report_file = f"category_report_{int(time.time())}.md"
    uploader.generate_category_report(uploaded_data, report_file)
    
    # 显示分类摘要
    summary = uploader.get_category_summary(uploaded_data)
    print("\n📊 上传摘要:")
    print(f"   总图片数: {summary['total_count']}")
    print(f"   分类数: {summary['category_count']}")
    print("   各分类详情:")
    
    for category, info in summary['categories'].items():
        print(f"     - {category}: {info['count']} 张")
        print(f"       文件名示例: {info['upload_filenames'][0] if info['upload_filenames'] else 'N/A'}")
    
    print(f"\n📄 详细报告已生成: {report_file}")
    print(f"📋 上传日志已保存: {log_file}")
    
    # 显示微信后台查找提示
    print("\n🔍 微信后台查找提示:")
    print("在微信公众号后台素材管理中，您可以:")
    for category in summary['categories'].keys():
        print(f"   - 搜索 '[{category}]' 查看该分类的所有图片")

def preview_upload(categories):
    """预览上传内容"""
    print("\n📋 上传预览:")
    
    total_images = 0
    for category in categories:
        category_path = os.path.join(DOWNLOAD_DIR, category)
        images = [f for f in os.listdir(category_path) 
                 if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'))]
        
        total_images += len(images)
        print(f"\n📁 分类: {category}")
        print(f"   图片数量: {len(images)}")
        print("   上传后的文件名示例:")
        
        for i, img in enumerate(images[:3]):  # 只显示前3个示例
            name, ext = os.path.splitext(img)
            upload_name = f"[{category}]{name}{ext}"
            print(f"     {i+1}. {img} → {upload_name}")
        
        if len(images) > 3:
            print(f"     ... 还有 {len(images) - 3} 张图片")
    
    print(f"\n📊 预览摘要:")
    print(f"   总分类数: {len(categories)}")
    print(f"   总图片数: {total_images}")
    print(f"   平均每分类: {total_images // len(categories) if categories else 0} 张")

def show_wechat_search_guide():
    """显示微信后台搜索指南"""
    print("\n" + "="*60)
    print("🔍 微信公众号后台图片查找指南")
    print("="*60)
    print()
    print("上传完成后，在微信公众号后台素材管理中，您可以通过以下方式快速找到图片：")
    print()
    print("1. 📝 按文件名搜索:")
    print("   - 所有图片文件名都以 [分类名] 开头")
    print("   - 例如：搜索 '[性感美女]' 可以找到该分类的所有图片")
    print()
    print("2. 🎯 按Media ID搜索:")
    print("   - 使用生成的报告中的Media ID进行精确查找")
    print("   - Media ID是微信分配的唯一标识符")
    print()
    print("3. ⏰ 按上传时间筛选:")
    print("   - 根据上传时间范围筛选图片")
    print("   - 同一批次上传的图片时间相近")
    print()
    print("4. 📊 使用生成的分类报告:")
    print("   - 查看 category_report_*.md 文件")
    print("   - 包含完整的分类信息和Media ID列表")
    print()

if __name__ == "__main__":
    import time
    
    demo_category_upload()
    show_wechat_search_guide()
    
    print("\n" + "="*60)
    print("✨ 分类上传功能特点:")
    print("✅ 自动根据目录名设置分类")
    print("✅ 文件名添加分类前缀，便于搜索")
    print("✅ 生成详细的分类报告")
    print("✅ 支持批量和选择性上传")
    print("✅ 完整的上传日志记录")
    print("="*60)