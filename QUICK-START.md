# 🚀 快速开始指南

## 🎯 选择适合您的发布平台

### 👤 个人开发者 (推荐)

如果您是个人开发者，请选择微信小程序：

```bash
# 使用个人开发者版本
cd wechat-miniprogram-personal/

# 查看发布指南
cat PERSONAL-PUBLISH-GUIDE.md
```

**特点**:
- ✅ 个人主体可以发布
- ✅ 注册简单，无需企业资质
- ✅ 完整的游戏功能
- ⚠️ 性能相对较低 (30FPS)

### 🏢 企业开发者

如果您有企业营业执照，可以选择微信小游戏：

```bash
# 使用企业开发者版本
cd wechat-minigame/

# 查看发布指南
cat PUBLISH-GUIDE.md
```

**特点**:
- ✅ 高性能游戏体验 (60FPS)
- ✅ 专业游戏API
- ✅ 支持内购和广告
- ⚠️ 需要企业营业执照

## 🌐 Web版本 (所有人可用)

无论您的身份如何，都可以直接运行Web版本：

```bash
# 启动Web服务器
./scripts/start_game.sh

# 或者直接运行Python服务器
python3 scripts/server.py
```

**访问地址**: https://work-1-rbvknchekxhhpkmp.prod-runtime.all-hands.dev

## 📋 发布主体对比

| 开发者类型 | 微信小程序 | 微信小游戏 | Web版本 |
|------------|------------|------------|---------|
| **个人开发者** | ✅ 支持 | ❌ 不支持 | ✅ 支持 |
| **企业开发者** | ✅ 支持 | ✅ 支持 | ✅ 支持 |

## 🎮 功能对比

| 功能特性 | 个人小程序 | 企业小游戏 | Web版本 |
|----------|------------|------------|---------|
| **游戏性能** | 30FPS | 60FPS | 60FPS |
| **触控操作** | ✅ | ✅ | ✅ |
| **本地存储** | ✅ | ✅ | ✅ |
| **分享功能** | ✅ | ✅ | ❌ |
| **支付功能** | ❌ | ✅ | ❌ |
| **广告变现** | ❌ | ✅ | ❌ |

## 📖 详细文档

- 👤 [个人开发者小程序指南](wechat-miniprogram-personal/PERSONAL-PUBLISH-GUIDE.md)
- 🎮 [企业开发者小游戏指南](wechat-minigame/PUBLISH-GUIDE.md)
- 🌐 [Web版本说明](docs/web-version-README.md)
- 📊 [平台对比详解](PLATFORM-COMPARISON.md)

---

🎯 **根据您的情况选择合适的平台，立即开始您的游戏发布之旅！**