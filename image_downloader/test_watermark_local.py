#!/usr/bin/env python3
"""
本地去水印功能测试
创建带水印的测试图片并验证去水印效果
"""
import os
import logging
from enhanced_image_scraper import EnhancedImageScraper
from PIL import Image, ImageDraw, ImageFont
import io

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def create_test_image_with_watermark():
    """创建带水印的测试图片"""
    print("🎨 创建带水印的测试图片...")
    
    # 创建一个测试图片 (800x600)
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color='lightblue')
    draw = ImageDraw.Draw(image)
    
    # 绘制一些内容
    for i in range(0, width, 50):
        for j in range(0, height, 50):
            color = (i % 255, j % 255, (i+j) % 255)
            draw.rectangle([i, j, i+40, j+40], fill=color)
    
    # 在右下角添加水印
    watermark_text = "WATERMARK"
    try:
        # 尝试使用默认字体
        font = ImageFont.load_default()
    except:
        font = None
    
    # 水印位置（右下角）
    watermark_x = width - 150
    watermark_y = height - 50
    
    # 绘制水印背景
    draw.rectangle([watermark_x-10, watermark_y-10, width-10, height-10], 
                  fill='white', outline='black', width=2)
    
    # 绘制水印文字
    draw.text((watermark_x, watermark_y), watermark_text, fill='red', font=font)
    
    # 保存测试图片
    test_image_path = "test_image_with_watermark.jpg"
    image.save(test_image_path, 'JPEG', quality=95)
    
    print(f"✅ 测试图片已创建: {test_image_path}")
    print(f"📐 图片尺寸: {width} x {height}")
    print(f"💧 水印位置: 右下角 ({watermark_x}, {watermark_y})")
    
    return test_image_path

def test_watermark_removal_on_local_image():
    """在本地图片上测试去水印功能"""
    print("\n🔧 测试去水印功能...")
    
    # 创建测试图片
    test_image_path = create_test_image_with_watermark()
    
    if not os.path.exists(test_image_path):
        print("❌ 测试图片创建失败")
        return
    
    # 读取测试图片数据
    with open(test_image_path, 'rb') as f:
        original_data = f.read()
    
    print(f"📊 原始图片大小: {len(original_data)} 字节")
    
    scraper = EnhancedImageScraper()
    
    # 测试不同的去水印方法
    methods = ['crop', 'blur']
    
    results = {}
    
    for method in methods:
        print(f"\n🔄 测试方法: {method}")
        try:
            processed_data = scraper.remove_watermark(original_data, method=method)
            
            # 保存处理后的图片
            output_path = f"test_watermark_removed_{method}.jpg"
            with open(output_path, 'wb') as f:
                f.write(processed_data)
            
            # 获取处理后图片的尺寸
            processed_image = Image.open(io.BytesIO(processed_data))
            processed_width, processed_height = processed_image.size
            
            results[method] = {
                'success': True,
                'size': len(processed_data),
                'dimensions': (processed_width, processed_height),
                'file': output_path
            }
            
            print(f"✅ {method} 处理成功")
            print(f"📊 文件大小: {len(processed_data)} 字节")
            print(f"📐 图片尺寸: {processed_width} x {processed_height}")
            print(f"💾 保存到: {output_path}")
            
        except Exception as e:
            results[method] = {'success': False, 'error': str(e)}
            print(f"❌ {method} 处理失败: {e}")
    
    return results

def test_watermark_detection_on_local():
    """测试本地图片的水印检测"""
    print("\n🔍 测试水印检测功能...")
    
    test_files = [
        "test_image_with_watermark.jpg",
        "test_watermark_removed_crop.jpg",
        "test_watermark_removed_blur.jpg"
    ]
    
    scraper = EnhancedImageScraper()
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📊 分析图片: {test_file}")
            try:
                with open(test_file, 'rb') as f:
                    image_data = f.read()
                
                # 检测水印区域
                x, y, w, h = scraper.detect_watermark_area(image_data)
                
                # 获取图片尺寸
                image = Image.open(test_file)
                img_width, img_height = image.size
                
                print(f"📐 图片尺寸: {img_width} x {img_height}")
                print(f"🎯 检测水印区域: x={x}, y={y}, width={w}, height={h}")
                print(f"📍 相对位置: ({x/img_width*100:.1f}%, {y/img_height*100:.1f}%)")
                print(f"📏 相对大小: {w/img_width*100:.1f}% x {h/img_height*100:.1f}%")
                
            except Exception as e:
                print(f"❌ 分析失败: {e}")

def compare_local_results():
    """对比本地处理结果"""
    print("\n📊 处理结果对比:")
    
    files = [
        ("原始图片(带水印)", "test_image_with_watermark.jpg"),
        ("裁剪去水印", "test_watermark_removed_crop.jpg"),
        ("模糊去水印", "test_watermark_removed_blur.jpg")
    ]
    
    print(f"{'方法':<20} {'文件大小':<12} {'图片尺寸':<15} {'状态'}")
    print("-" * 60)
    
    for name, filename in files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            try:
                image = Image.open(filename)
                dimensions = f"{image.size[0]}x{image.size[1]}"
                status = "✅"
            except:
                dimensions = "N/A"
                status = "⚠️"
            
            print(f"{name:<20} {size:<12} {dimensions:<15} {status}")
        else:
            print(f"{name:<20} {'N/A':<12} {'N/A':<15} ❌")

def analyze_watermark_effectiveness():
    """分析去水印效果"""
    print("\n🔬 去水印效果分析:")
    
    original_file = "test_image_with_watermark.jpg"
    processed_files = [
        ("裁剪方法", "test_watermark_removed_crop.jpg"),
        ("模糊方法", "test_watermark_removed_blur.jpg")
    ]
    
    if not os.path.exists(original_file):
        print("❌ 原始文件不存在")
        return
    
    original_image = Image.open(original_file)
    original_width, original_height = original_image.size
    
    print(f"📐 原始图片: {original_width} x {original_height}")
    
    for method_name, processed_file in processed_files:
        if os.path.exists(processed_file):
            processed_image = Image.open(processed_file)
            processed_width, processed_height = processed_image.size
            
            # 计算尺寸变化
            width_ratio = processed_width / original_width
            height_ratio = processed_height / original_height
            area_ratio = (processed_width * processed_height) / (original_width * original_height)
            
            print(f"\n🔧 {method_name}:")
            print(f"   📐 处理后尺寸: {processed_width} x {processed_height}")
            print(f"   📊 尺寸保留率: 宽度 {width_ratio*100:.1f}%, 高度 {height_ratio*100:.1f}%")
            print(f"   📈 面积保留率: {area_ratio*100:.1f}%")
            
            if method_name == "裁剪方法":
                if width_ratio < 1.0 or height_ratio < 1.0:
                    print(f"   ✅ 成功裁剪水印区域")
                else:
                    print(f"   ⚠️ 未检测到裁剪效果")
            elif method_name == "模糊方法":
                if width_ratio == 1.0 and height_ratio == 1.0:
                    print(f"   ✅ 保持原始尺寸，仅处理水印区域")
                else:
                    print(f"   ⚠️ 意外的尺寸变化")

def main():
    """主测试函数"""
    print("🚀 本地去水印功能测试")
    print("=" * 60)
    print("测试内容:")
    print("✓ 创建带水印的测试图片")
    print("✓ 测试不同去水印方法")
    print("✓ 水印区域检测分析")
    print("✓ 处理效果对比")
    print("=" * 60)
    
    setup_logging()
    
    try:
        # 测试去水印功能
        results = test_watermark_removal_on_local_image()
        
        # 测试水印检测
        test_watermark_detection_on_local()
        
        # 对比结果
        compare_local_results()
        
        # 分析效果
        analyze_watermark_effectiveness()
        
        print("\n" + "=" * 60)
        print("🎯 测试总结:")
        
        if results:
            successful_methods = [method for method, result in results.items() if result.get('success')]
            failed_methods = [method for method, result in results.items() if not result.get('success')]
            
            print(f"✅ 成功的方法: {', '.join(successful_methods) if successful_methods else '无'}")
            if failed_methods:
                print(f"❌ 失败的方法: {', '.join(failed_methods)}")
        
        print("\n📁 生成的测试文件:")
        print("   • test_image_with_watermark.jpg - 带水印的原始测试图片")
        print("   • test_watermark_removed_crop.jpg - 裁剪去水印结果")
        print("   • test_watermark_removed_blur.jpg - 模糊去水印结果")
        
        print("\n💡 方法特点:")
        print("   • 裁剪方法: 直接移除右下角区域，简单有效")
        print("   • 模糊方法: 保持图片完整，模糊处理水印区域")
        print("   • 自动方法: 根据环境自动选择最佳处理方式")
        
        print("\n🔧 集成说明:")
        print("   • 去水印功能已集成到下载流程中")
        print("   • 可通过配置文件控制是否启用和选择方法")
        print("   • 支持与WebP转JPG功能同时使用")
        print("=" * 60)
        
    except Exception as e:
        print(f"💥 测试过程中发生错误: {e}")

if __name__ == "__main__":
    main()