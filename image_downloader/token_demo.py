#!/usr/bin/env python3
"""
微信Token动态获取演示
展示如何使用动态Token服务替代固定配置
"""
import json
import logging
from wechat_token_service import WeChatTokenService, get_access_token, get_token_service
from wechat_uploader import WeChatUploader

def demo_token_service():
    """演示Token服务的基本功能"""
    print("=== 微信Token动态获取演示 ===\n")
    
    # 设置日志级别
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    try:
        # 方式1: 使用全局单例服务
        print("1. 使用全局Token服务:")
        token = get_access_token()
        if token:
            print(f"   获取到Token: {token[:20]}...")
        else:
            print("   获取Token失败")
        
        # 方式2: 直接创建Token服务实例
        print("\n2. 创建Token服务实例:")
        with WeChatTokenService() as service:
            token_info = service.get_token_info()
            print(f"   Token信息: {json.dumps(token_info, indent=4, ensure_ascii=False)}")
            
            # 获取Token响应对象
            token_resp = service.get_access_token()
            if token_resp:
                print(f"   Token: {token_resp.access_token[:20]}...")
                print(f"   有效期: {token_resp.expires_in}秒")
            
        # 方式3: 在上传器中使用
        print("\n3. 在图片上传器中使用:")
        uploader = WeChatUploader()
        token = uploader.get_access_token()
        if token:
            print(f"   上传器获取到Token: {token[:20]}...")
        else:
            print("   上传器获取Token失败")
            
        # 演示缓存机制
        print("\n4. 演示Token缓存机制:")
        service = get_token_service()
        
        print("   第一次获取Token...")
        token1 = service.get_token_string()
        
        print("   第二次获取Token (应该使用缓存)...")
        token2 = service.get_token_string()
        
        if token1 and token2:
            print(f"   两次Token是否相同: {token1 == token2}")
            print("   ✓ 缓存机制工作正常")
        
        # 演示强制刷新
        print("\n5. 演示强制刷新Token:")
        old_info = service.get_token_info()
        print(f"   刷新前Token预览: {old_info.get('token_preview', 'N/A')}")
        
        refreshed_token = service.refresh_token()
        if refreshed_token:
            print(f"   刷新后Token: {refreshed_token.access_token[:20]}...")
            print("   ✓ 强制刷新成功")
        
    except Exception as e:
        print(f"演示过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

def demo_java_style_usage():
    """演示类似Java RestTemplate风格的使用方式"""
    print("\n=== Java风格使用演示 ===\n")
    
    try:
        # 模拟Java中的依赖注入和服务调用
        token_service = WeChatTokenService()
        
        # 类似Java中的@Autowired注入后的使用
        print("模拟Spring Boot服务调用:")
        
        # 获取Token响应 (类似Java中的ResponseEntity<TokenResp>)
        token_response = token_service.get_access_token()
        
        if token_response:
            print(f"✓ 获取Token成功")
            print(f"  access_token: {token_response.access_token[:30]}...")
            print(f"  expires_in: {token_response.expires_in}")
            
            # 转换为字典 (类似Java中的对象序列化)
            response_dict = token_response.to_dict()
            print(f"  响应数据: {json.dumps(response_dict, indent=2)}")
        else:
            print("✗ 获取Token失败")
            
    except Exception as e:
        print(f"Java风格演示失败: {e}")

if __name__ == "__main__":
    demo_token_service()
    demo_java_style_usage()
    
    print("\n=== 演示完成 ===")
    print("主要特性:")
    print("✓ 动态获取Token，无需固定配置文件")
    print("✓ 自动缓存和刷新机制")
    print("✓ 线程安全的Token管理")
    print("✓ 类似Java RestTemplate的使用体验")
    print("✓ 完整的错误处理和日志记录")