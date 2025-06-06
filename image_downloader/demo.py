"""
演示程序 - 展示完整的下载和上传流程
"""
import os
import json
import time
from image_scraper import ImageScraper
from wechat_uploader import WeChatUploader
from config import *

def demo_download():
    """演示下载功能"""
    print("=== 图片下载演示 ===")
    
    scraper = ImageScraper()
    
    # 下载一个分类的图片（少量）
    category_code = "xgmn"
    category_name = CATEGORIES[category_code]
    
    print(f"正在下载分类: {category_name}")
    count = scraper.scrape_category(category_code, category_name)
    print(f"下载完成，共下载 {count} 张图片")
    
    return count

def demo_upload_simulation():
    """演示上传功能（模拟）"""
    print("\n=== 微信公众号上传演示（模拟） ===")
    
    # 模拟上传过程
    download_dir = os.path.join(DOWNLOAD_DIR, "性感美女")
    
    if not os.path.exists(download_dir):
        print("没有找到下载的图片")
        return
        
    image_files = [f for f in os.listdir(download_dir) 
                   if any(f.lower().endswith(ext) for ext in IMAGE_EXTENSIONS)]
    
    print(f"找到 {len(image_files)} 张图片待上传")
    
    # 模拟上传结果
    upload_results = []
    for i, filename in enumerate(image_files):
        # 模拟上传延迟
        time.sleep(0.5)
        
        # 生成模拟的media_id
        media_id = f"mock_media_id_{i+1:03d}_{int(time.time())}"
        
        upload_results.append({
            'filename': filename,
            'media_id': media_id,
            'category': '性感美女',
            'upload_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'success'
        })
        
        print(f"✓ 上传成功: {filename} -> {media_id}")
    
    # 保存上传日志
    log_file = "demo_upload_log.json"
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(upload_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n上传完成，共上传 {len(upload_results)} 张图片")
    print(f"上传日志已保存到: {log_file}")
    
    return upload_results

def demo_real_wechat_config():
    """演示真实微信配置检查"""
    print("\n=== 微信公众号配置检查 ===")
    
    if WECHAT_APPID and WECHAT_SECRET:
        print("✓ 微信配置已设置")
        uploader = WeChatUploader()
        
        # 尝试获取access_token
        token = uploader.get_access_token()
        if token:
            print("✓ 微信API连接成功")
            
            # 获取素材统计
            material_count = uploader.get_material_count()
            if material_count:
                print(f"✓ 素材库统计: {material_count}")
            else:
                print("⚠ 无法获取素材库统计")
        else:
            print("✗ 微信API连接失败")
    else:
        print("⚠ 微信配置未设置，使用模拟模式")
        print("要使用真实上传功能，请：")
        print("1. 复制 .env.example 为 .env")
        print("2. 在 .env 中填入真实的微信公众号 AppID 和 Secret")

def show_project_structure():
    """显示项目结构"""
    print("\n=== 项目结构 ===")
    
    structure = {
        "配置文件": ["config.py", ".env.example"],
        "核心模块": ["image_scraper.py", "wechat_uploader.py"],
        "主程序": ["main.py", "demo.py"],
        "文档": ["README.md"],
        "依赖": ["requirements.txt"],
        "下载目录": ["downloads/"],
        "日志文件": ["app.log", "scraper.log", "upload_log.json"]
    }
    
    for category, files in structure.items():
        print(f"\n{category}:")
        for file in files:
            if os.path.exists(file):
                print(f"  ✓ {file}")
            else:
                print(f"  - {file} (将在运行时生成)")

def main():
    """主演示函数"""
    print("🖼️  图片下载和微信公众号上传工具演示")
    print("=" * 50)
    
    # 显示项目结构
    show_project_structure()
    
    # 检查微信配置
    demo_real_wechat_config()
    
    # 下载演示
    download_count = demo_download()
    
    if download_count > 0:
        # 上传演示（模拟）
        upload_results = demo_upload_simulation()
        
        print("\n=== 演示总结 ===")
        print(f"✓ 成功下载 {download_count} 张图片")
        print(f"✓ 模拟上传 {len(upload_results)} 张图片")
        print("✓ 图片已按分类整理到 downloads/ 目录")
        print("✓ 上传日志已保存")
        
        print("\n=== 使用说明 ===")
        print("1. 配置微信公众号信息后可进行真实上传")
        print("2. 使用 python main.py --help 查看所有选项")
        print("3. 使用 python main.py --check-config 检查配置")
        print("4. 使用 python main.py --download --category xgmn 下载指定分类")
        print("5. 使用 python main.py --upload 上传到微信公众号")
    else:
        print("\n⚠ 没有成功下载图片，请检查网络连接")

if __name__ == "__main__":
    main()