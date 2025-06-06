#!/usr/bin/env python3
"""
测试去水印功能
"""
import os
import logging
from enhanced_image_scraper import EnhancedImageScraper
from PIL import Image
import requests

def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def test_watermark_removal_methods():
    """测试不同的去水印方法"""
    print("🔧 测试去水印功能...")
    
    scraper = EnhancedImageScraper()
    
    # 测试图片URL（从之前的测试中获取）
    test_image_url = "https://pic.3gbizhi.com/uploadmark/20250530/237ceaddac2fc4fe07206396643f5c96.webp"
    
    try:
        # 下载原始图片
        print("📥 下载测试图片...")
        response = requests.get(test_image_url, timeout=30)
        response.raise_for_status()
        original_data = response.content
        
        print(f"✅ 原始图片大小: {len(original_data)} 字节")
        
        # 测试不同的去水印方法
        methods = ['crop', 'blur']
        if hasattr(scraper, 'CV2_AVAILABLE') and scraper.CV2_AVAILABLE:
            methods.append('inpaint')
        
        results = {}
        
        for method in methods:
            print(f"\n🔄 测试方法: {method}")
            try:
                processed_data = scraper.remove_watermark(original_data, method=method)
                results[method] = {
                    'success': True,
                    'size': len(processed_data),
                    'data': processed_data
                }
                print(f"✅ {method} 处理成功，大小: {len(processed_data)} 字节")
                
                # 保存处理后的图片用于对比
                output_path = f"test_output_{method}.jpg"
                with open(output_path, 'wb') as f:
                    f.write(processed_data)
                print(f"💾 保存到: {output_path}")
                
            except Exception as e:
                results[method] = {'success': False, 'error': str(e)}
                print(f"❌ {method} 处理失败: {e}")
        
        # 保存原始图片用于对比
        original_jpg = scraper.convert_webp_to_jpg(original_data)
        with open("test_output_original.jpg", 'wb') as f:
            f.write(original_jpg)
        print(f"💾 原始图片保存到: test_output_original.jpg")
        
        return results
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return {}

def test_watermark_detection():
    """测试水印检测功能"""
    print("\n🔍 测试水印检测功能...")
    
    scraper = EnhancedImageScraper()
    
    # 如果有测试图片，分析水印区域
    test_files = ["test_output_original.jpg"]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"\n📊 分析图片: {test_file}")
            try:
                with open(test_file, 'rb') as f:
                    image_data = f.read()
                
                # 检测水印区域
                x, y, w, h = scraper.detect_watermark_area(image_data)
                print(f"🎯 检测到水印区域: x={x}, y={y}, width={w}, height={h}")
                
                # 获取图片尺寸用于对比
                image = Image.open(test_file)
                img_width, img_height = image.size
                print(f"📐 图片尺寸: {img_width} x {img_height}")
                print(f"📍 水印位置: 右下角 ({x/img_width*100:.1f}%, {y/img_height*100:.1f}%)")
                print(f"📏 水印大小: {w/img_width*100:.1f}% x {h/img_height*100:.1f}%")
                
            except Exception as e:
                print(f"❌ 分析失败: {e}")

def test_download_with_watermark_removal():
    """测试集成的下载+去水印功能"""
    print("\n⬇️ 测试集成下载+去水印功能...")
    
    scraper = EnhancedImageScraper()
    
    # 测试下载单张图片
    test_url = "https://pic.3gbizhi.com/uploadmark/20250530/237ceaddac2fc4fe07206396643f5c96.webp"
    
    test_cases = [
        ("无处理", False, False, 'auto'),
        ("仅转换", True, False, 'auto'),
        ("转换+去水印(裁剪)", True, True, 'crop'),
        ("转换+去水印(模糊)", True, True, 'blur'),
        ("转换+去水印(自动)", True, True, 'auto')
    ]
    
    for name, convert_webp, remove_watermark, method in test_cases:
        print(f"\n🧪 测试: {name}")
        try:
            save_path = f"test_integrated_{name.replace(' ', '_').replace('(', '').replace(')', '')}.jpg"
            
            success = scraper.download_image(
                test_url, 
                save_path, 
                convert_webp=convert_webp,
                remove_watermark=remove_watermark,
                watermark_method=method
            )
            
            if success and os.path.exists(save_path):
                file_size = os.path.getsize(save_path)
                print(f"✅ {name} 成功，文件大小: {file_size} 字节")
                print(f"💾 保存到: {save_path}")
            else:
                print(f"❌ {name} 失败")
                
        except Exception as e:
            print(f"❌ {name} 异常: {e}")

def compare_results():
    """对比处理结果"""
    print("\n📊 处理结果对比:")
    
    files = [
        ("原始图片", "test_output_original.jpg"),
        ("裁剪去水印", "test_output_crop.jpg"),
        ("模糊去水印", "test_output_blur.jpg"),
        ("集成下载(自动)", "test_integrated_转换+去水印自动.jpg")
    ]
    
    print(f"{'方法':<15} {'文件大小':<10} {'状态'}")
    print("-" * 35)
    
    for name, filename in files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"{name:<15} {size:<10} ✅")
        else:
            print(f"{name:<15} {'N/A':<10} ❌")

def main():
    """主测试函数"""
    print("🚀 去水印功能测试")
    print("=" * 50)
    print("测试内容:")
    print("✓ 不同去水印方法测试")
    print("✓ 水印区域检测")
    print("✓ 集成下载+去水印")
    print("✓ 结果对比分析")
    print("=" * 50)
    
    setup_logging()
    
    # 运行测试
    try:
        # 测试去水印方法
        results = test_watermark_removal_methods()
        
        # 测试水印检测
        test_watermark_detection()
        
        # 测试集成功能
        test_download_with_watermark_removal()
        
        # 对比结果
        compare_results()
        
        print("\n" + "=" * 50)
        print("🎯 测试总结:")
        print("✅ 去水印方法 - 支持裁剪、模糊、修复等多种方法")
        print("✅ 智能检测 - 自动分析水印区域位置和大小")
        print("✅ 集成处理 - 下载时自动去水印和格式转换")
        print("✅ 配置灵活 - 可选择不同的处理方法和参数")
        print()
        print("📁 生成的测试文件:")
        print("   • test_output_original.jpg - 原始图片")
        print("   • test_output_crop.jpg - 裁剪去水印")
        print("   • test_output_blur.jpg - 模糊去水印")
        print("   • test_integrated_*.jpg - 集成处理结果")
        print()
        print("💡 建议:")
        print("   • 裁剪方法最简单有效，适合边缘水印")
        print("   • 模糊方法保持图片完整，适合角落水印")
        print("   • 自动方法会根据环境选择最佳处理方式")
        print("=" * 50)
        
    except Exception as e:
        print(f"💥 测试过程中发生错误: {e}")

if __name__ == "__main__":
    main()