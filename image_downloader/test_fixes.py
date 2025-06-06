#!/usr/bin/env python3
"""
测试修复效果
1. 分页下载完整性测试
2. 改进的水印去除效果测试
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

def test_pagination_completeness():
    """测试分页下载完整性"""
    print("🔍 测试分页下载完整性...")
    
    scraper = EnhancedImageScraper()
    
    # 测试一个有多页的分类
    category_url = "https://www.3gbizhi.com/meinv/xgmn/"
    
    try:
        # 检测总页数
        max_pages = scraper.detect_max_pages(category_url)
        print(f"✅ 检测到总页数: {max_pages}")
        
        # 测试解析前5页（如果有的话）
        test_pages = min(max_pages, 5)
        print(f"📄 测试解析前 {test_pages} 页...")
        
        detail_urls = scraper.parse_category_all_pages(category_url, max_pages=test_pages)
        
        expected_blocks = test_pages * 25  # 每页25个图块
        actual_blocks = len(detail_urls)
        
        print(f"📊 预期图块数: {expected_blocks}")
        print(f"📊 实际图块数: {actual_blocks}")
        print(f"📊 覆盖率: {actual_blocks/expected_blocks*100:.1f}%")
        
        if actual_blocks >= expected_blocks * 0.9:  # 90%以上认为成功
            print("✅ 分页解析测试通过")
            return True
        else:
            print("❌ 分页解析不完整")
            return False
            
    except Exception as e:
        print(f"❌ 分页测试失败: {e}")
        return False

def test_download_limit_fix():
    """测试下载限制修复"""
    print("\n📈 测试下载限制修复...")
    
    from config import MAX_IMAGES_PER_CATEGORY
    
    print(f"📊 当前最大下载限制: {MAX_IMAGES_PER_CATEGORY} 张")
    
    # 计算理论容量
    pages_capacity = MAX_IMAGES_PER_CATEGORY // (25 * 5)  # 25个图块/页 × 5张图片/块
    print(f"📊 理论支持页数: {pages_capacity} 页")
    
    if pages_capacity >= 15:  # 支持15页以上认为合理
        print("✅ 下载限制设置合理，支持大规模下载")
        return True
    else:
        print("⚠️ 下载限制可能仍然偏小")
        return False

def test_improved_watermark_removal():
    """测试改进的水印去除效果"""
    print("\n🔧 测试改进的水印去除效果...")
    
    # 先运行本地水印测试
    print("🎨 创建改进的测试水印...")
    
    from test_watermark_local import create_test_image_with_watermark
    
    try:
        # 创建带有更真实水印的测试图片
        test_image_path = create_test_image_with_watermark()
        
        if not os.path.exists(test_image_path):
            print("❌ 测试图片创建失败")
            return False
        
        # 读取测试图片
        with open(test_image_path, 'rb') as f:
            original_data = f.read()
        
        scraper = EnhancedImageScraper()
        
        # 测试改进的模糊方法
        print("🔄 测试改进的模糊去水印...")
        processed_data = scraper.remove_watermark(original_data, method='blur')
        
        # 保存处理结果
        output_path = "test_improved_blur_removal.jpg"
        with open(output_path, 'wb') as f:
            f.write(processed_data)
        
        print(f"💾 改进的模糊去水印结果保存到: {output_path}")
        
        # 测试水印检测
        print("🔍 测试改进的水印检测...")
        x, y, w, h = scraper.detect_watermark_area(original_data)
        
        from PIL import Image
        image = Image.open(test_image_path)
        img_width, img_height = image.size
        
        coverage_width = w / img_width * 100
        coverage_height = h / img_height * 100
        
        print(f"📐 检测到水印区域: {w} × {h} 像素")
        print(f"📊 覆盖范围: 宽度 {coverage_width:.1f}%, 高度 {coverage_height:.1f}%")
        
        # 检查覆盖范围是否足够大
        if coverage_width >= 25 and coverage_height >= 15:  # 至少覆盖25%宽度和15%高度
            print("✅ 水印检测范围充足，能够覆盖完整水印区域")
            return True
        else:
            print("⚠️ 水印检测范围可能仍然不足")
            return False
            
    except Exception as e:
        print(f"❌ 水印测试失败: {e}")
        return False

def test_small_scale_download():
    """测试小规模下载验证修复效果"""
    print("\n⬇️ 测试小规模下载验证修复...")
    
    scraper = EnhancedImageScraper()
    
    try:
        print("📥 开始小规模测试下载（1页，最多10张图片）...")
        
        # 测试下载1页，限制10张图片
        count = scraper.scrape_category_enhanced(
            "mnzp", 
            "测试美女照片", 
            max_pages=1, 
            max_images=10
        )
        
        print(f"📊 实际下载图片数: {count}")
        
        # 检查下载的文件
        download_dir = "downloads/测试美女照片"
        if os.path.exists(download_dir):
            files = [f for f in os.listdir(download_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            print(f"📁 下载目录中的文件数: {len(files)}")
            
            if len(files) > 0:
                print("✅ 下载功能正常工作")
                
                # 检查文件名格式
                sample_files = files[:3]
                print("📝 示例文件名:")
                for f in sample_files:
                    print(f"   • {f}")
                
                return True
            else:
                print("❌ 没有成功下载任何文件")
                return False
        else:
            print("❌ 下载目录不存在")
            return False
            
    except Exception as e:
        print(f"❌ 下载测试失败: {e}")
        return False

def compare_watermark_methods():
    """对比不同水印去除方法的效果"""
    print("\n📊 对比不同水印去除方法...")
    
    test_files = [
        ("原始图片", "test_image_with_watermark.jpg"),
        ("改进模糊", "test_improved_blur_removal.jpg"),
        ("原始模糊", "test_watermark_removed_blur.jpg"),
        ("裁剪方法", "test_watermark_removed_crop.jpg")
    ]
    
    print(f"{'方法':<12} {'文件大小':<12} {'图片尺寸':<12} {'状态'}")
    print("-" * 50)
    
    for name, filename in test_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            try:
                from PIL import Image
                image = Image.open(filename)
                dimensions = f"{image.size[0]}×{image.size[1]}"
                status = "✅"
            except:
                dimensions = "N/A"
                status = "⚠️"
            
            print(f"{name:<12} {size:<12} {dimensions:<12} {status}")
        else:
            print(f"{name:<12} {'N/A':<12} {'N/A':<12} ❌")

def main():
    """主测试函数"""
    print("🚀 修复效果验证测试")
    print("=" * 60)
    print("测试内容:")
    print("✓ 分页下载完整性")
    print("✓ 下载限制修复")
    print("✓ 改进的水印去除")
    print("✓ 小规模下载验证")
    print("=" * 60)
    
    setup_logging()
    
    results = {}
    
    # 运行测试
    tests = [
        ("分页完整性", test_pagination_completeness),
        ("下载限制", test_download_limit_fix),
        ("水印去除", test_improved_watermark_removal),
        ("下载验证", test_small_scale_download)
    ]
    
    for test_name, test_func in tests:
        print(f"\n🧪 开始测试: {test_name}")
        try:
            results[test_name] = test_func()
            status = "✅ 通过" if results[test_name] else "❌ 失败"
            print(f"📊 {test_name} 测试结果: {status}")
        except Exception as e:
            results[test_name] = False
            print(f"💥 {test_name} 测试异常: {e}")
    
    # 对比水印方法
    compare_watermark_methods()
    
    # 总结
    print("\n" + "=" * 60)
    print("🎯 修复效果总结:")
    
    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    print(f"📊 测试通过率: {passed_tests}/{total_tests} ({passed_tests/total_tests*100:.1f}%)")
    
    for test_name, result in results.items():
        status = "✅" if result else "❌"
        print(f"   {status} {test_name}")
    
    print("\n🔧 主要修复:")
    print("   • 提高下载限制到5000张，支持完整分类下载")
    print("   • 扩大水印模糊区域，覆盖更大范围（宽度1/3，高度1/4）")
    print("   • 增强模糊强度（radius=12），更好地隐藏水印")
    print("   • 改进水印检测算法，智能调整处理区域大小")
    
    print("\n💡 使用建议:")
    print("   • 大批量下载：现在支持完整分类下载（20+页）")
    print("   • 水印处理：推荐使用'auto'方法，自动选择最佳处理")
    print("   • 质量控制：模糊方法现在能更好地覆盖水印区域")
    print("=" * 60)

if __name__ == "__main__":
    main()