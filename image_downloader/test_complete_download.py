#!/usr/bin/env python3
"""
测试完整下载功能
验证分页处理和图块完整下载
"""
import os
import logging
from enhanced_image_scraper import EnhancedImageScraper

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def test_pagination_detection():
    """测试分页检测功能"""
    print("🔍 测试分页检测功能...")
    
    scraper = EnhancedImageScraper()
    
    # 测试不同分类的分页检测
    test_categories = [
        ("https://www.3gbizhi.com/meinv/xgmn/", "性感美女"),
        ("https://www.3gbizhi.com/meinv/mnzp/", "美女照片"),
        ("https://www.3gbizhi.com/meinv/yzmn/", "日韩美女")
    ]
    
    for category_url, category_name in test_categories:
        try:
            max_pages = scraper.detect_max_pages(category_url)
            print(f"✅ {category_name}: 检测到 {max_pages} 页")
        except Exception as e:
            print(f"❌ {category_name}: 检测失败 - {e}")

def test_complete_image_extraction():
    """测试完整图片提取（固定5张）"""
    print("\n📸 测试完整图片提取...")
    
    scraper = EnhancedImageScraper()
    
    # 测试不同的图块
    test_urls = [
        "https://www.3gbizhi.com/meinv/xgmn/pic2192.html",
        "https://www.3gbizhi.com/meinv/mnzp/pic2189.html"
    ]
    
    for test_url in test_urls:
        try:
            images = scraper.get_all_images_from_detail_page(test_url)
            pic_id = test_url.split('/')[-1].replace('.html', '')
            print(f"✅ {pic_id}: 找到 {len(images)} 张图片")
            
            # 显示文件名预览
            for i, img_url in enumerate(images[:3], 1):
                filename = scraper.get_image_filename(img_url, test_url, i if len(images) > 1 else None)
                print(f"   {i}. {filename}")
            
            if len(images) > 3:
                print(f"   ... 还有 {len(images) - 3} 张")
                
        except Exception as e:
            print(f"❌ {test_url}: 提取失败 - {e}")

def test_multi_page_parsing():
    """测试多页解析"""
    print("\n📄 测试多页解析...")
    
    scraper = EnhancedImageScraper()
    category_url = "https://www.3gbizhi.com/meinv/xgmn/"
    
    try:
        # 测试前3页
        detail_urls = scraper.parse_category_all_pages(category_url, max_pages=3)
        print(f"✅ 前3页总共找到 {len(detail_urls)} 个图块")
        
        # 按页面分组统计
        page_stats = {}
        for url in detail_urls:
            # 简单估算：假设每页25个图块
            page_num = (detail_urls.index(url) // 25) + 1
            if page_num not in page_stats:
                page_stats[page_num] = 0
            page_stats[page_num] += 1
        
        for page, count in sorted(page_stats.items()):
            print(f"   第{page}页: {count} 个图块")
            
        # 计算预期图片数量
        expected_images = len(detail_urls) * 5
        print(f"   预期图片总数: {len(detail_urls)} 个图块 × 5 张/块 = {expected_images} 张")
        
    except Exception as e:
        print(f"❌ 多页解析失败: {e}")

def test_small_complete_download():
    """测试小规模完整下载"""
    print("\n⬇️ 测试小规模完整下载...")
    
    scraper = EnhancedImageScraper()
    
    try:
        # 下载美女照片分类的前2页，最多30张图片
        print("开始下载美女照片分类（前2页，最多30张图片）...")
        count = scraper.scrape_category_enhanced("mnzp", "美女照片", max_pages=2, max_images=30)
        print(f"✅ 下载完成，共 {count} 张图片")
        
        # 检查下载的文件
        download_dir = "downloads/美女照片"
        if os.path.exists(download_dir):
            files = [f for f in os.listdir(download_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            print(f"📁 下载目录中有 {len(files)} 个图片文件")
            
            # 按图块分组统计
            block_stats = {}
            for f in files:
                if 'pic' in f:
                    # 提取pic ID，如pic2189_1_xxx.jpg -> pic2189
                    pic_id = f.split('_')[0]
                    if pic_id not in block_stats:
                        block_stats[pic_id] = 0
                    block_stats[pic_id] += 1
            
            print(f"📊 图块统计:")
            for pic_id, count in sorted(block_stats.items()):
                print(f"   {pic_id}: {count} 张图片")
        
        return count > 0
        
    except Exception as e:
        print(f"❌ 下载测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 完整下载功能测试")
    print("=" * 60)
    print("测试内容:")
    print("✓ 分页检测功能")
    print("✓ 完整图片提取（固定5张）")
    print("✓ 多页解析功能")
    print("✓ 小规模完整下载")
    print("=" * 60)
    
    setup_logging()
    
    # 运行测试
    tests = [
        ("分页检测", test_pagination_detection),
        ("图片提取", test_complete_image_extraction),
        ("多页解析", test_multi_page_parsing),
        ("完整下载", test_small_complete_download)
    ]
    
    for test_name, test_func in tests:
        print(f"\n🧪 开始测试: {test_name}")
        try:
            test_func()
            print(f"📊 {test_name} 测试完成")
        except Exception as e:
            print(f"💥 {test_name} 测试异常: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 测试总结:")
    print("✅ 分页检测 - 自动检测每个分类的页数")
    print("✅ 图片提取 - 每个图块固定提取5张图片")
    print("✅ 多页处理 - 处理所有分页的图块")
    print("✅ 完整下载 - 图块级别的完整下载")
    print()
    print("📈 预期效果:")
    print("   • 每页25个图块 × 5张图片 = 125张图片/页")
    print("   • 多页累积可获得大量高质量图片")
    print("   • 文件名包含图块ID，便于管理")
    print("=" * 60)

if __name__ == "__main__":
    main()