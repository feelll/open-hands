"""
Java Spring Boot风格的微信Token获取演示
模拟Java中的RestTemplate和ResponseEntity使用方式
"""
import json
import logging
from typing import Optional, Dict, Any, TypeVar, Generic
from dataclasses import dataclass
import requests
from wechat_token_service import TokenResponse, WeChatTokenService

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')

@dataclass
class HttpHeaders:
    """模拟Spring Boot的HttpHeaders"""
    headers: Dict[str, str]
    
    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'JavaStyleDemo/1.0'
        }
    
    def add(self, key: str, value: str):
        """添加请求头"""
        self.headers[key] = value

@dataclass
class HttpEntity(Generic[T]):
    """模拟Spring Boot的HttpEntity"""
    body: Optional[T]
    headers: HttpHeaders
    
    def __init__(self, body: Optional[T] = None, headers: HttpHeaders = None):
        self.body = body
        self.headers = headers or HttpHeaders()

@dataclass
class ResponseEntity(Generic[T]):
    """模拟Spring Boot的ResponseEntity"""
    body: Optional[T]
    status_code: int
    headers: Dict[str, str]
    
    def __init__(self, body: Optional[T], status_code: int, headers: Dict[str, str] = None):
        self.body = body
        self.status_code = status_code
        self.headers = headers or {}

class RestTemplate:
    """模拟Spring Boot的RestTemplate"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def exchange(self, 
                url: str, 
                method: str, 
                request_entity: HttpEntity, 
                response_type: type) -> ResponseEntity:
        """
        模拟RestTemplate.exchange方法
        
        Args:
            url: 请求URL
            method: HTTP方法
            request_entity: 请求实体
            response_type: 响应类型
            
        Returns:
            ResponseEntity对象
        """
        try:
            # 准备请求参数
            kwargs = {
                'headers': request_entity.headers.headers,
                'timeout': 30
            }
            
            if request_entity.body is not None:
                kwargs['json'] = request_entity.body
            
            # 发送请求
            if method.upper() == 'GET':
                response = self.session.get(url, **kwargs)
            elif method.upper() == 'POST':
                response = self.session.post(url, **kwargs)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            # 解析响应
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = None
            
            # 创建ResponseEntity
            if response_type == TokenResponse:
                body = TokenResponse.from_dict(response_data) if response_data else None
            else:
                body = response_data
            
            return ResponseEntity(
                body=body,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
            
        except Exception as e:
            logger.error(f"请求异常: {e}")
            return ResponseEntity(
                body=None,
                status_code=500,
                headers={}
            )

class JavaStyleWeChatTokenService:
    """
    Java Spring Boot风格的微信Token服务
    完全模拟您提供的Java代码结构
    """
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.rest_template = RestTemplate()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def get_access_token(self) -> Optional[TokenResponse]:
        """
        获取微信access_token
        完全按照您提供的Java代码逻辑实现
        """
        # 构建请求URL（与Java代码完全一致）
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        
        # 创建请求头
        headers = HttpHeaders()
        
        # 创建请求实体（对应Java中的HttpEntity<GetAlbumsReq>）
        request_entity = HttpEntity(body=None, headers=headers)
        
        # 发送请求（对应Java中的restTemplate.exchange）
        resp = self.rest_template.exchange(
            url=url,
            method="POST",  # 与Java代码一致使用POST
            request_entity=request_entity,
            response_type=TokenResponse
        )
        
        # 记录响应日志（对应Java中的log.info）
        self.logger.info(f"getAccessToken, resp: {resp}")
        
        # 获取响应体（对应Java中的resp.getBody()）
        body = resp.body
        
        return body

def demo_java_style_usage():
    """演示Java风格的使用方式"""
    print("=== Java Spring Boot风格演示 ===")
    
    # 模拟从配置中获取参数
    app_id = "demo_app_id"  # 在实际使用中从配置文件获取
    app_secret = "demo_app_secret"  # 在实际使用中从配置文件获取
    
    try:
        # 创建服务实例（对应Java中的@Autowired或构造函数注入）
        service = JavaStyleWeChatTokenService(app_id, app_secret)
        
        # 调用获取token方法（完全对应您的Java代码）
        token_resp = service.get_access_token()
        
        if token_resp:
            print(f"✅ 成功获取Token:")
            print(f"   access_token: {token_resp.access_token[:20]}...")
            print(f"   expires_in: {token_resp.expires_in}")
            
            # 转换为字典（对应Java中的JSON序列化）
            token_dict = token_resp.to_dict()
            print(f"   JSON格式: {json.dumps(token_dict, indent=2)}")
        else:
            print("❌ 获取Token失败")
            
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback
        traceback.print_exc()

def demo_comparison():
    """对比Java风格和Python风格的实现"""
    print("\n=== 实现方式对比 ===")
    
    print("Java风格特点:")
    print("✓ 使用RestTemplate进行HTTP请求")
    print("✓ 使用HttpEntity封装请求")
    print("✓ 使用ResponseEntity封装响应")
    print("✓ 强类型的数据传输对象(DTO)")
    print("✓ 详细的日志记录")
    
    print("\nPython风格特点:")
    print("✓ 使用requests库进行HTTP请求")
    print("✓ 使用dataclass定义数据结构")
    print("✓ 内置缓存和自动刷新机制")
    print("✓ 线程安全的单例模式")
    print("✓ 更简洁的API接口")

def demo_integration():
    """演示与现有系统的集成"""
    print("\n=== 集成演示 ===")
    
    # 方式1: 使用Java风格的服务
    print("1. Java风格集成:")
    try:
        java_service = JavaStyleWeChatTokenService("demo_id", "demo_secret")
        token = java_service.get_access_token()
        print(f"   Java风格结果: {'成功' if token else '失败'}")
    except Exception as e:
        print(f"   Java风格异常: {e}")
    
    # 方式2: 使用Python风格的服务
    print("2. Python风格集成:")
    try:
        from wechat_token_service import get_access_token
        token = get_access_token()
        print(f"   Python风格结果: {'成功' if token else '失败'}")
    except Exception as e:
        print(f"   Python风格异常: {e}")

if __name__ == "__main__":
    print("🚀 Java Spring Boot风格微信Token服务演示")
    print("=" * 60)
    
    # Java风格使用演示
    demo_java_style_usage()
    
    # 实现方式对比
    demo_comparison()
    
    # 集成演示
    demo_integration()
    
    print("\n" + "=" * 60)
    print("🏁 演示完成")
    
    print("\n💡 使用建议:")
    print("- 如果团队熟悉Java Spring Boot，可以使用JavaStyleWeChatTokenService")
    print("- 如果追求Python的简洁性，推荐使用WeChatTokenService")
    print("- 两种方式都支持，可以根据项目需求选择")