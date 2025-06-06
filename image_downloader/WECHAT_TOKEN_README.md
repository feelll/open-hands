# 微信公众号动态Token获取服务

## 概述

本项目实现了一个基于Spring Boot风格的微信公众号access_token动态获取服务，替代了原有的静态配置方式。新系统具有以下特点：

- 🔄 **动态获取**: 自动从微信API获取access_token
- 💾 **智能缓存**: 内存缓存token，避免频繁请求
- 🔒 **线程安全**: 支持多线程并发访问
- ⏰ **自动刷新**: token过期前自动刷新
- 🛡️ **错误处理**: 完善的异常处理和重试机制
- 📊 **监控支持**: 提供token状态监控接口

## 核心组件

### 1. TokenResponse 数据类

```python
@dataclass
class TokenResponse:
    access_token: str
    expires_in: int
```

对应Java中的TokenResp类，用于封装微信API返回的token数据。

### 2. WeChatTokenService 服务类

主要的token管理服务，提供以下功能：

- `get_access_token()`: 获取TokenResponse对象
- `get_token_string()`: 获取access_token字符串
- `refresh_token()`: 强制刷新token
- `get_token_info()`: 获取token状态信息
- `clear_cache()`: 清除缓存

### 3. 便捷函数

```python
# 获取access_token字符串
token = get_access_token()

# 刷新token
new_token = refresh_access_token()

# 获取服务实例
service = get_token_service()
```

## 使用方法

### 基本用法

```python
from wechat_token_service import get_access_token

# 获取access_token
token = get_access_token()
if token:
    print(f"获取到token: {token}")
else:
    print("获取token失败")
```

### 高级用法

```python
from wechat_token_service import WeChatTokenService

# 创建独立的服务实例
with WeChatTokenService() as service:
    # 获取完整的token响应
    token_resp = service.get_access_token()
    if token_resp:
        print(f"Token: {token_resp.access_token}")
        print(f"有效期: {token_resp.expires_in}秒")
    
    # 获取token状态信息
    info = service.get_token_info()
    print(f"Token信息: {info}")
    
    # 强制刷新token
    new_token = service.refresh_token()
```

### 与现有上传器集成

```python
from wechat_uploader import WeChatUploader

# 上传器会自动使用新的token服务
uploader = WeChatUploader()
token = uploader.get_access_token()  # 内部使用动态token服务
```

## 配置说明

### 环境变量配置

在`.env`文件中配置：

```bash
# 微信公众号AppID
WECHAT_APPID=your_wechat_appid_here

# 微信公众号AppSecret
WECHAT_SECRET=your_wechat_secret_here

# 注意：不再需要配置WECHAT_ACCESS_TOKEN
```

### 代码配置

```python
# 使用自定义配置创建服务
service = WeChatTokenService(
    app_id="your_app_id",
    app_secret="your_app_secret"
)
```

## 缓存机制

### 缓存策略

1. **内存缓存**: token存储在内存中，避免重复请求
2. **过期检查**: 每次获取前检查token是否过期
3. **提前刷新**: token过期前5分钟自动刷新
4. **线程安全**: 使用锁机制保证并发安全

### 缓存生命周期

```
获取token -> 检查缓存 -> 缓存有效? -> 返回缓存token
                |              |
                |              v
                |         缓存无效/不存在
                |              |
                |              v
                |         请求新token
                |              |
                |              v
                |         更新缓存
                |              |
                v              v
            返回新token <-------
```

## 错误处理

### 常见错误类型

1. **配置错误**: AppID或AppSecret未配置
2. **网络错误**: 请求微信API失败
3. **API错误**: 微信API返回错误码
4. **解析错误**: 响应数据格式错误

### 错误处理示例

```python
try:
    token = get_access_token()
    if not token:
        print("获取token失败，请检查配置")
except ValueError as e:
    print(f"配置错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

## 监控和调试

### 获取token状态

```python
service = get_token_service()
info = service.get_token_info()
print(f"Token状态: {info}")
```

返回信息包括：
- `has_cached_token`: 是否有缓存token
- `token_valid`: token是否有效
- `expires_at`: token过期时间
- `token_preview`: token预览（部分隐藏）

### 日志配置

```python
import logging

# 设置日志级别
logging.basicConfig(level=logging.INFO)

# 查看详细调试信息
logging.getLogger('wechat_token_service').setLevel(logging.DEBUG)
```

## 性能优化

### 单例模式

系统使用单例模式管理全局token服务，避免重复创建实例：

```python
# 多次调用返回同一个实例
service1 = get_token_service()
service2 = get_token_service()
assert service1 is service2  # True
```

### 连接池

内部使用`requests.Session`管理HTTP连接，提高请求效率。

### 缓存优化

- 内存缓存避免重复网络请求
- 提前刷新机制避免token过期
- 线程安全保证并发访问正确性

## 迁移指南

### 从静态配置迁移

**旧方式**:
```python
# 手动配置access_token
WECHAT_ACCESS_TOKEN = "your_static_token"
```

**新方式**:
```python
# 动态获取access_token
from wechat_token_service import get_access_token
token = get_access_token()
```

### 更新现有代码

1. **移除静态token配置**:
   - 删除`.env`中的`WECHAT_ACCESS_TOKEN`
   - 确保`WECHAT_APPID`和`WECHAT_SECRET`正确配置

2. **更新代码调用**:
   ```python
   # 旧代码
   token = WECHAT_ACCESS_TOKEN
   
   # 新代码
   from wechat_token_service import get_access_token
   token = get_access_token()
   ```

3. **测试验证**:
   ```bash
   python wechat_token_demo.py
   ```

## 测试和验证

### 运行演示脚本

```bash
cd image_downloader
python wechat_token_demo.py
```

演示脚本包括：
- 基本用法演示
- 高级功能演示
- 错误处理演示
- 集成测试演示
- 监控功能演示

### 单元测试

```python
# 测试token获取
def test_get_token():
    token = get_access_token()
    assert token is not None
    assert len(token) > 0

# 测试缓存机制
def test_cache():
    service = get_token_service()
    token1 = service.get_token_string()
    token2 = service.get_token_string()
    assert token1 == token2  # 应该返回缓存的token
```

## 最佳实践

### 1. 配置管理
- 使用环境变量管理敏感配置
- 不要在代码中硬编码AppID和AppSecret
- 定期轮换AppSecret

### 2. 错误处理
- 始终检查token获取结果
- 实现适当的重试机制
- 记录详细的错误日志

### 3. 性能优化
- 使用全局单例服务
- 避免频繁创建新的服务实例
- 合理设置日志级别

### 4. 监控告警
- 定期检查token获取状态
- 监控API调用频率
- 设置token获取失败告警

## 常见问题

### Q: token获取失败怎么办？
A: 检查以下几点：
1. AppID和AppSecret是否正确
2. 网络连接是否正常
3. 微信公众号是否正常
4. 查看详细错误日志

### Q: 如何提高token获取速度？
A: 系统已经实现了缓存机制，第二次及后续获取会直接返回缓存的token，速度很快。

### Q: 支持多个公众号吗？
A: 可以创建多个`WeChatTokenService`实例，每个实例使用不同的AppID和AppSecret。

### Q: token会自动刷新吗？
A: 是的，系统会在token过期前5分钟自动刷新，无需手动干预。

## 技术架构

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   应用层        │    │    服务层        │    │    数据层       │
│                 │    │                  │    │                 │
│ WeChatUploader  │───▶│ WeChatTokenService│───▶│  微信API       │
│ 其他业务模块    │    │                  │    │                 │
│                 │    │ - 缓存管理       │    │ - token获取     │
└─────────────────┘    │ - 自动刷新       │    │ - 错误响应      │
                       │ - 线程安全       │    │                 │
                       └──────────────────┘    └─────────────────┘
```

## 更新日志

### v1.0.0 (2024-06-06)
- 🎉 初始版本发布
- ✨ 实现动态token获取
- 💾 添加智能缓存机制
- 🔒 支持线程安全访问
- 📊 提供监控接口
- 🛡️ 完善错误处理
- 📚 提供详细文档和示例