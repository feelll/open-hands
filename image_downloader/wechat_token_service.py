"""
微信公众号Token动态获取服务
基于Spring Boot风格的HTTP客户端实现
"""
import json
import time
import logging
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading
from config import WECHAT_APPID, WECHAT_SECRET


@dataclass
class TokenResponse:
    """Token响应数据类，对应Java中的TokenResp"""
    access_token: str
    expires_in: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TokenResponse':
        """从字典创建TokenResponse对象"""
        return cls(
            access_token=data.get('access_token', ''),
            expires_in=data.get('expires_in', 7200)
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'access_token': self.access_token,
            'expires_in': self.expires_in
        }


class WeChatTokenService:
    """
    微信Token服务类
    实现动态获取和缓存微信access_token
    """
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        """
        初始化Token服务
        
        Args:
            app_id: 微信公众号AppID
            app_secret: 微信公众号AppSecret
        """
        self.app_id = app_id or WECHAT_APPID
        self.app_secret = app_secret or WECHAT_SECRET
        self.logger = self._setup_logging()
        
        # Token缓存相关
        self._cached_token: Optional[TokenResponse] = None
        self._token_expires_at: Optional[datetime] = None
        self._lock = threading.Lock()
        
        # HTTP客户端配置
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'WeChatTokenService/1.0'
        })
        
        # 配置验证
        if not self.app_id or not self.app_secret:
            self.logger.error("微信公众号AppID或AppSecret未配置")
            raise ValueError("微信公众号配置不完整")
    
    def _setup_logging(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def get_access_token(self) -> Optional[TokenResponse]:
        """
        获取微信access_token
        实现自动缓存和刷新机制
        
        Returns:
            TokenResponse对象，包含access_token和expires_in
        """
        with self._lock:
            # 检查缓存的token是否仍然有效
            if self._is_token_valid():
                self.logger.debug("使用缓存的access_token")
                return self._cached_token
            
            # 获取新的token
            return self._fetch_new_token()
    
    def _is_token_valid(self) -> bool:
        """
        检查当前缓存的token是否有效
        
        Returns:
            bool: token是否有效
        """
        if not self._cached_token or not self._token_expires_at:
            return False
        
        # 提前5分钟刷新token，避免在使用时过期
        buffer_time = timedelta(minutes=5)
        return datetime.now() < (self._token_expires_at - buffer_time)
    
    def _fetch_new_token(self) -> Optional[TokenResponse]:
        """
        从微信API获取新的access_token
        
        Returns:
            TokenResponse对象或None
        """
        url = "https://api.weixin.qq.com/cgi-bin/token"
        params = {
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.app_secret
        }
        
        try:
            self.logger.info("正在获取新的access_token...")
            
            # 发送HTTP请求
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            # 解析响应
            data = response.json()
            self.logger.info(f"Token API响应: {data}")
            
            # 检查响应是否包含错误
            if 'errcode' in data:
                self.logger.error(f"获取access_token失败: {data}")
                return None
            
            # 创建TokenResponse对象
            token_resp = TokenResponse.from_dict(data)
            
            # 更新缓存
            self._cached_token = token_resp
            self._token_expires_at = datetime.now() + timedelta(seconds=token_resp.expires_in)
            
            self.logger.info(
                f"成功获取access_token，有效期至: {self._token_expires_at.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            
            return token_resp
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"HTTP请求异常: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析异常: {e}")
            return None
        except Exception as e:
            self.logger.error(f"获取access_token时发生未知异常: {e}")
            return None
    
    def get_token_string(self) -> Optional[str]:
        """
        获取access_token字符串
        
        Returns:
            access_token字符串或None
        """
        token_resp = self.get_access_token()
        return token_resp.access_token if token_resp else None
    
    def refresh_token(self) -> Optional[TokenResponse]:
        """
        强制刷新token
        
        Returns:
            新的TokenResponse对象或None
        """
        with self._lock:
            self.logger.info("强制刷新access_token")
            self._cached_token = None
            self._token_expires_at = None
            return self._fetch_new_token()
    
    def get_token_info(self) -> Dict[str, Any]:
        """
        获取token信息
        
        Returns:
            包含token状态信息的字典
        """
        info = {
            'has_cached_token': self._cached_token is not None,
            'token_valid': self._is_token_valid(),
            'expires_at': self._token_expires_at.isoformat() if self._token_expires_at else None,
            'app_id': self.app_id[:8] + '***' if self.app_id else None  # 部分隐藏AppID
        }
        
        if self._cached_token:
            info['token_preview'] = self._cached_token.access_token[:10] + '***'
            info['expires_in'] = self._cached_token.expires_in
        
        return info
    
    def clear_cache(self):
        """清除token缓存"""
        with self._lock:
            self.logger.info("清除token缓存")
            self._cached_token = None
            self._token_expires_at = None
    
    def __enter__(self):
        """上下文管理器入口"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        self.session.close()


# 全局单例实例
_token_service_instance: Optional[WeChatTokenService] = None
_instance_lock = threading.Lock()


def get_token_service() -> WeChatTokenService:
    """
    获取全局Token服务单例
    
    Returns:
        WeChatTokenService实例
    """
    global _token_service_instance
    
    if _token_service_instance is None:
        with _instance_lock:
            if _token_service_instance is None:
                _token_service_instance = WeChatTokenService()
    
    return _token_service_instance


def get_access_token() -> Optional[str]:
    """
    便捷函数：获取access_token字符串
    
    Returns:
        access_token字符串或None
    """
    return get_token_service().get_token_string()


def refresh_access_token() -> Optional[str]:
    """
    便捷函数：刷新并获取access_token字符串
    
    Returns:
        新的access_token字符串或None
    """
    token_resp = get_token_service().refresh_token()
    return token_resp.access_token if token_resp else None


if __name__ == "__main__":
    # 测试代码
    import os
    
    # 设置日志级别
    logging.basicConfig(level=logging.INFO)
    
    # 测试Token服务
    try:
        with WeChatTokenService() as service:
            print("=== 微信Token服务测试 ===")
            
            # 获取token信息
            info = service.get_token_info()
            print(f"Token服务信息: {json.dumps(info, indent=2, ensure_ascii=False)}")
            
            # 获取access_token
            token_resp = service.get_access_token()
            if token_resp:
                print(f"获取到access_token: {token_resp.access_token[:20]}...")
                print(f"有效期: {token_resp.expires_in}秒")
            else:
                print("获取access_token失败")
            
            # 测试缓存机制
            print("\n=== 测试缓存机制 ===")
            token_resp2 = service.get_access_token()
            if token_resp and token_resp2:
                print(f"两次获取的token是否相同: {token_resp.access_token == token_resp2.access_token}")
            
            # 获取最新token信息
            final_info = service.get_token_info()
            print(f"最终Token信息: {json.dumps(final_info, indent=2, ensure_ascii=False)}")
            
    except Exception as e:
        print(f"测试失败: {e}")