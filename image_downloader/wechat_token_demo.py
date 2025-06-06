"""
微信Token服务演示脚本
展示如何使用动态Token获取服务
"""
import json
import time
import logging
from wechat_token_service import (
    WeChatTokenService, 
    get_token_service, 
    get_access_token, 
    refresh_access_token
)

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def demo_basic_usage():
    """演示基本用法"""
    print("=== 基本用法演示 ===")
    
    # 方式1: 使用便捷函数
    token = get_access_token()
    if token:
        print(f"✅ 获取到access_token: {token[:20]}...")
    else:
        print("❌ 获取access_token失败")
    
    # 方式2: 使用全局单例
    service = get_token_service()
    token_info = service.get_token_info()
    print(f"📊 Token信息: {json.dumps(token_info, indent=2, ensure_ascii=False)}")

def demo_advanced_usage():
    """演示高级用法"""
    print("\n=== 高级用法演示 ===")
    
    # 创建独立的Token服务实例
    with WeChatTokenService() as service:
        print("🔧 创建独立Token服务实例")
        
        # 获取完整的Token响应
        token_resp = service.get_access_token()
        if token_resp:
            print(f"✅ Token: {token_resp.access_token[:20]}...")
            print(f"⏰ 有效期: {token_resp.expires_in}秒")
            
            # 转换为字典
            token_dict = token_resp.to_dict()
            print(f"📄 Token字典: {token_dict}")
        
        # 测试缓存机制
        print("\n🧪 测试缓存机制...")
        start_time = time.time()
        token1 = service.get_token_string()
        time1 = time.time() - start_time
        
        start_time = time.time()
        token2 = service.get_token_string()
        time2 = time.time() - start_time
        
        print(f"首次获取耗时: {time1:.3f}秒")
        print(f"缓存获取耗时: {time2:.3f}秒")
        print(f"Token相同: {token1 == token2}")
        
        # 强制刷新Token
        print("\n🔄 强制刷新Token...")
        new_token_resp = service.refresh_token()
        if new_token_resp:
            print(f"✅ 新Token: {new_token_resp.access_token[:20]}...")

def demo_error_handling():
    """演示错误处理"""
    print("\n=== 错误处理演示 ===")
    
    try:
        # 使用无效的配置创建服务
        invalid_service = WeChatTokenService(app_id="invalid", app_secret="invalid")
        token = invalid_service.get_token_string()
        if token:
            print(f"意外获取到Token: {token}")
        else:
            print("❌ 如预期，无效配置无法获取Token")
    except ValueError as e:
        print(f"⚠️ 配置验证错误: {e}")
    except Exception as e:
        print(f"❌ 其他错误: {e}")

def demo_integration_with_uploader():
    """演示与上传器的集成"""
    print("\n=== 与上传器集成演示 ===")
    
    try:
        from wechat_uploader import WeChatUploader
        
        uploader = WeChatUploader()
        token = uploader.get_access_token()
        
        if token:
            print(f"✅ 上传器获取Token成功: {token[:20]}...")
            
            # 获取素材统计
            material_count = uploader.get_material_count()
            if material_count:
                print(f"📊 素材库统计: {material_count}")
            else:
                print("❌ 获取素材统计失败")
        else:
            print("❌ 上传器获取Token失败")
            
    except ImportError as e:
        print(f"⚠️ 导入上传器失败: {e}")
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")

def demo_token_monitoring():
    """演示Token监控"""
    print("\n=== Token监控演示 ===")
    
    service = get_token_service()
    
    # 监控Token状态
    for i in range(3):
        info = service.get_token_info()
        print(f"📊 监控轮次 {i+1}: {json.dumps(info, indent=2, ensure_ascii=False)}")
        
        if i < 2:
            time.sleep(1)  # 等待1秒

def main():
    """主函数"""
    print("🚀 微信Token服务演示开始")
    print("=" * 50)
    
    try:
        # 基本用法
        demo_basic_usage()
        
        # 高级用法
        demo_advanced_usage()
        
        # 错误处理
        demo_error_handling()
        
        # 与上传器集成
        demo_integration_with_uploader()
        
        # Token监控
        demo_token_monitoring()
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🏁 微信Token服务演示结束")

if __name__ == "__main__":
    main()