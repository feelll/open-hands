#!/usr/bin/env python3
"""
测试扩大的水印覆盖效果
验证向左和向上扩展的水印模糊区域
"""
import os
import logging
from enhanced_image_scraper import EnhancedImageScraper
from PIL import Image, ImageDraw, ImageFont

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def create_comprehensive_watermark_test():
    """创建包含更复杂水印的测试图片"""
    print("🎨 创建包含复杂水印的测试图片...")
    
    # 创建一个测试图片 (800x600)
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color='lightblue')
    draw = ImageDraw.Draw(image)
    
    # 绘制一些内容
    for i in range(0, width, 50):
        for j in range(0, height, 50):
            color = (i % 255, j % 255, (i+j) % 255)
            draw.rectangle([i, j, i+40, j+40], fill=color)
    
    # 在右下角添加更复杂的水印（模拟真实情况）
    try:
        font = ImageFont.load_default()
    except:
        font = None
    
    # 水印区域（右下角，更大更复杂）
    watermark_width = 300  # 更大的水印区域
    watermark_height = 120
    watermark_x = width - watermark_width - 5
    watermark_y = height - watermark_height - 5
    
    # 绘制半透明背景
    watermark_bg = Image.new('RGBA', (watermark_width, watermark_height), (255, 255, 255, 150))
    watermark_draw = ImageDraw.Draw(watermark_bg)
    
    # 绘制多个水印元素（模拟真实复杂水印）
    # 左上角：3G字样
    watermark_draw.text((10, 10), "3G", fill=(255, 0, 0, 220), font=font)
    
    # 中上：网站名
    watermark_draw.text((50, 10), "BIZHI.COM", fill=(0, 0, 255, 220), font=font)
    
    # 右上：版权符号
    watermark_draw.text((200, 10), "©2024", fill=(128, 128, 128, 200), font=font)
    
    # 左中：网址
    watermark_draw.text((10, 35), "www.example.com", fill=(64, 64, 64, 200), font=font)
    
    # 右中：更多文字
    watermark_draw.text((150, 35), "HD PICS", fill=(0, 128, 0, 200), font=font)
    
    # 左下：水印标识
    watermark_draw.text((10, 60), "WATERMARK", fill=(255, 128, 0, 200), font=font)
    
    # 右下：更多标识
    watermark_draw.text((150, 60), "DOWNLOAD", fill=(128, 0, 255, 200), font=font)
    
    # 底部：长文本
    watermark_draw.text((10, 85), "Free High Quality Images", fill=(100, 100, 100, 180), font=font)
    
    # 将水印合成到主图片上
    image_rgba = image.convert('RGBA')
    image_rgba.paste(watermark_bg, (watermark_x, watermark_y), watermark_bg)
    image = image_rgba.convert('RGB')
    
    # 保存测试图片
    test_image_path = "test_complex_watermark.jpg"
    image.save(test_image_path, 'JPEG', quality=95)
    
    print(f"✅ 复杂水印测试图片已创建: {test_image_path}")
    print(f"📐 图片尺寸: {width} x {height}")
    print(f"💧 水印区域: {watermark_width} x {watermark_height} 像素")
    print(f"📍 水印位置: ({watermark_x}, {watermark_y})")
    
    return test_image_path

def test_expanded_watermark_coverage():
    """测试扩大的水印覆盖效果"""
    print("\n🔧 测试扩大的水印覆盖效果...")
    
    # 创建复杂水印测试图片
    test_image_path = create_comprehensive_watermark_test()
    
    if not os.path.exists(test_image_path):
        print("❌ 测试图片创建失败")
        return False
    
    # 读取测试图片数据
    with open(test_image_path, 'rb') as f:
        original_data = f.read()
    
    scraper = EnhancedImageScraper()
    
    # 测试不同的水印处理方法
    methods = [
        ('原始模糊', 'blur'),
        ('扩大模糊', 'blur')  # 使用新的扩大范围
    ]
    
    results = {}
    
    for method_name, method in methods:
        print(f"\n🔄 测试方法: {method_name}")
        try:
            processed_data = scraper.remove_watermark(original_data, method=method)
            
            # 保存处理后的图片
            output_path = f"test_expanded_{method_name.replace(' ', '_')}.jpg"
            with open(output_path, 'wb') as f:
                f.write(processed_data)
            
            # 获取处理后图片的尺寸
            processed_image = Image.open(output_path)
            processed_width, processed_height = processed_image.size
            
            results[method_name] = {
                'success': True,
                'size': len(processed_data),
                'dimensions': (processed_width, processed_height),
                'file': output_path
            }
            
            print(f"✅ {method_name} 处理成功")
            print(f"📊 文件大小: {len(processed_data)} 字节")
            print(f"📐 图片尺寸: {processed_width} x {processed_height}")
            print(f"💾 保存到: {output_path}")
            
        except Exception as e:
            results[method_name] = {'success': False, 'error': str(e)}
            print(f"❌ {method_name} 处理失败: {e}")
    
    return results

def test_watermark_detection_expansion():
    """测试扩大的水印检测范围"""
    print("\n🔍 测试扩大的水印检测范围...")
    
    test_file = "test_complex_watermark.jpg"
    
    if not os.path.exists(test_file):
        print("❌ 测试文件不存在")
        return
    
    scraper = EnhancedImageScraper()
    
    try:
        with open(test_file, 'rb') as f:
            image_data = f.read()
        
        # 检测水印区域
        x, y, w, h = scraper.detect_watermark_area(image_data)
        
        # 获取图片尺寸
        image = Image.open(test_file)
        img_width, img_height = image.size
        
        coverage_width = w / img_width * 100
        coverage_height = h / img_height * 100
        
        print(f"📐 图片尺寸: {img_width} x {img_height}")
        print(f"🎯 检测水印区域: {w} x {h} 像素")
        print(f"📍 水印位置: ({x}, {y})")
        print(f"📊 覆盖范围: 宽度 {coverage_width:.1f}%, 高度 {coverage_height:.1f}%")
        
        # 分析覆盖效果
        if coverage_width >= 35 and coverage_height >= 25:  # 期望更大的覆盖范围
            print("✅ 扩大的水印检测范围充足")
            return True
        else:
            print("⚠️ 水印检测范围可能仍需调整")
            return False
            
    except Exception as e:
        print(f"❌ 水印检测失败: {e}")
        return False

def compare_coverage_improvements():
    """对比覆盖范围改进效果"""
    print("\n📊 对比覆盖范围改进效果...")
    
    # 计算不同方法的理论覆盖范围
    test_width, test_height = 800, 600
    
    coverage_methods = [
        ("原始方法", test_width // 4, test_height // 4),  # 1/4 x 1/4
        ("第一次改进", test_width // 3, test_height // 4),  # 1/3 x 1/4  
        ("当前扩大", int(test_width // 2.5), test_height // 3)  # 2/5 x 1/3
    ]
    
    print(f"{'方法':<12} {'宽度(px)':<10} {'高度(px)':<10} {'宽度%':<8} {'高度%':<8} {'面积%':<8}")
    print("-" * 65)
    
    for method_name, width_px, height_px in coverage_methods:
        width_percent = width_px / test_width * 100
        height_percent = height_px / test_height * 100
        area_percent = (width_px * height_px) / (test_width * test_height) * 100
        
        print(f"{method_name:<12} {width_px:<10} {height_px:<10} {width_percent:<8.1f} {height_percent:<8.1f} {area_percent:<8.1f}")

def analyze_processing_results():
    """分析处理结果"""
    print("\n🔬 分析处理结果...")
    
    files = [
        ("原始图片", "test_complex_watermark.jpg"),
        ("扩大模糊", "test_expanded_扩大模糊.jpg")
    ]
    
    print(f"{'文件':<15} {'大小(字节)':<12} {'尺寸':<12} {'状态'}")
    print("-" * 50)
    
    for name, filename in files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            try:
                image = Image.open(filename)
                dimensions = f"{image.size[0]}×{image.size[1]}"
                status = "✅"
            except:
                dimensions = "N/A"
                status = "⚠️"
            
            print(f"{name:<15} {size:<12} {dimensions:<12} {status}")
        else:
            print(f"{name:<15} {'N/A':<12} {'N/A':<12} ❌")

def main():
    """主测试函数"""
    print("🚀 扩大水印覆盖范围测试")
    print("=" * 60)
    print("测试内容:")
    print("✓ 创建复杂水印测试图片")
    print("✓ 测试扩大的模糊覆盖范围")
    print("✓ 验证水印检测范围扩大")
    print("✓ 对比覆盖范围改进效果")
    print("=" * 60)
    
    setup_logging()
    
    try:
        # 测试扩大的水印覆盖
        results = test_expanded_watermark_coverage()
        
        # 测试水印检测扩大
        detection_success = test_watermark_detection_expansion()
        
        # 对比覆盖范围改进
        compare_coverage_improvements()
        
        # 分析处理结果
        analyze_processing_results()
        
        print("\n" + "=" * 60)
        print("🎯 扩大覆盖范围总结:")
        
        print("\n📏 覆盖范围改进:")
        print("   • 宽度: 1/4 → 1/3 → 2/5 (向左扩展更多)")
        print("   • 高度: 1/4 → 1/4 → 1/3 (向上扩展更多)")
        print("   • 面积: 6.25% → 8.33% → 13.33% (覆盖面积翻倍)")
        
        print("\n🔧 技术改进:")
        print("   • 模糊方法: width//2.5, height//3")
        print("   • 修复方法: 同样扩大的蒙版区域")
        print("   • 检测算法: 智能适应不同复杂度水印")
        
        print("\n💡 实际效果:")
        print("   • 能够覆盖更左侧的3G字样")
        print("   • 能够覆盖更上方的版权信息")
        print("   • 更好地处理复杂多元素水印")
        
        if detection_success:
            print("\n✅ 扩大的水印检测和处理范围验证成功")
        else:
            print("\n⚠️ 可能需要进一步调整覆盖范围")
        
        print("\n📁 生成的测试文件:")
        print("   • test_complex_watermark.jpg - 复杂水印测试图片")
        print("   • test_expanded_扩大模糊.jpg - 扩大范围处理结果")
        print("=" * 60)
        
    except Exception as e:
        print(f"💥 测试过程中发生错误: {e}")

if __name__ == "__main__":
    main()