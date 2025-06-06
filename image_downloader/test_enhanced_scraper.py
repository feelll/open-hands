#!/usr/bin/env python3
"""
测试增强版爬虫功能
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

def test_single_detail_page():
    """测试单个详情页的图片提取"""
    print("🔍 测试单个详情页图片提取...")
    
    scraper = EnhancedImageScraper()
    test_url = "https://www.3gbizhi.com/meinv/xgmn/pic2192.html"
    
    try:
        images = scraper.get_all_images_from_detail_page(test_url)
        print(f"✅ 找到 {len(images)} 张图片:")
        
        for i, img_url in enumerate(images, 1):
            filename = scraper.get_image_filename(img_url, test_url, i if len(images) > 1 else None)
            print(f"   {i}. {filename}")
            print(f"      URL: {img_url[:80]}...")
            
        return len(images) > 0
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_category_parsing():
    """测试分类页面解析"""
    print("\n📄 测试分类页面解析...")
    
    scraper = EnhancedImageScraper()
    category_url = "https://www.3gbizhi.com/meinv/xgmn/"
    
    try:
        # 只测试第一页
        detail_urls = scraper.parse_category_all_pages(category_url, max_pages=1)
        print(f"✅ 第一页找到 {len(detail_urls)} 个详情页:")
        
        for i, url in enumerate(detail_urls[:5], 1):  # 只显示前5个
            print(f"   {i}. {url}")
            
        if len(detail_urls) > 5:
            print(f"   ... 还有 {len(detail_urls) - 5} 个")
            
        return len(detail_urls) > 0
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def test_small_download():
    """测试小规模下载"""
    print("\n⬇️ 测试小规模下载...")
    
    scraper = EnhancedImageScraper()
    
    try:
        # 下载性感美女分类的前3张图片
        count = scraper.scrape_category_enhanced("xgmn", "性感美女", max_pages=1, max_images=3)
        print(f"✅ 下载完成，共 {count} 张图片")
        
        # 检查下载的文件
        download_dir = "downloads/性感美女"
        if os.path.exists(download_dir):
            files = [f for f in os.listdir(download_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            print(f"📁 下载目录中有 {len(files)} 个图片文件:")
            for f in files:
                print(f"   - {f}")
        
        return count > 0
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 增强版图片爬虫功能测试")
    print("=" * 50)
    
    setup_logging()
    
    # 运行测试
    tests = [
        ("详情页图片提取", test_single_detail_page),
        ("分类页面解析", test_category_parsing),
        ("小规模下载", test_small_download)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 开始测试: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ 通过" if result else "❌ 失败"
            print(f"📊 测试结果: {status}")
        except Exception as e:
            print(f"💥 测试异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 50)
    print("📋 测试总结:")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅" if result else "❌"
        print(f"   {status} {test_name}")
    
    print(f"\n🎯 通过率: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 所有测试通过！增强版爬虫功能正常")
    else:
        print("⚠️ 部分测试失败，请检查网络连接或代码逻辑")

if __name__ == "__main__":
    main()