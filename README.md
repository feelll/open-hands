# 🎮 太空射击游戏 - Space Shooter Game

一款精心制作的休闲射击游戏，支持Web浏览器和微信小程序双平台运行。

## ✨ 项目亮点

🚀 **多平台支持** - Web浏览器 + 微信小程序 + 微信小游戏  
🎯 **完整游戏体验** - 射击、躲避、升级、挑战  
🎨 **精美视觉效果** - 粒子系统、爆炸动画、动态背景  
🎵 **沉浸式音效** - 射击音效、爆炸声效  
📱 **移动端优化** - 触控操作、响应式设计  

## 🎮 游戏特性

### 核心玩法
- 🛸 **飞船控制** - 流畅的移动和射击操作
- 👾 **多样敌人** - 不同类型敌机，各具特色
- 💥 **爽快射击** - 连续射击，精准打击
- 🏆 **分数挑战** - 实时分数，最高记录保存
- 🌟 **视觉盛宴** - 炫酷特效，沉浸体验

### 技术特色
- 🎨 **HTML5 Canvas** - 高性能2D渲染
- 📱 **响应式设计** - 完美适配各种设备
- 🔧 **模块化架构** - 清晰的代码结构
- 💾 **本地存储** - 游戏进度自动保存
- 🔄 **实时更新** - 60FPS流畅游戏体验

## 📁 项目结构

```
📦 open-hands/
├── 📄 README.md                     # 项目说明
├── 📄 PROJECT-STRUCTURE.md          # 结构详解
│
├── 🌐 web-version/                  # Web浏览器版本
│   ├── 🏠 index.html                # 游戏主页
│   ├── 🎮 game.js                   # 游戏引擎
│   └── ⚙️ game_config.js            # 配置文件
│
├── 📱 wechat-miniprogram/           # 微信小程序版本 (原版)
├── 👤 wechat-miniprogram-personal/  # 微信小程序版本 (个人开发者)
├── 🎮 wechat-minigame/              # 微信小游戏版本 (企业开发者)
│   ├── 🚀 app.js                    # 应用入口
│   ├── ⚙️ app.json                  # 全局配置
│   ├── 🎨 app.wxss                  # 全局样式
│   ├── 🔧 project.config.json       # 项目配置
│   │
│   ├── 📄 pages/game/               # 游戏页面
│   │   ├── 🎮 game.js               # 页面逻辑
│   │   ├── ⚙️ game.json             # 页面配置
│   │   ├── 🏗️ game.wxml             # 页面结构
│   │   └── 🎨 game.wxss             # 页面样式
│   │
│   ├── 📚 docs/                     # 文档目录
│   └── 🗄️ backup/                   # 备份文件
│
├── 🛠️ scripts/                      # 工具脚本
│   ├── 🌐 server.py                 # Web服务器
│   └── 🚀 start_game.sh             # 启动脚本
│
└── 📚 docs/                         # 项目文档
    └── 📖 web-version-README.md     # Web版详细说明
```

## 🚀 快速开始

### 🌐 Web版本

```bash
# 1. 启动游戏服务器
./scripts/start_game.sh

# 2. 打开浏览器访问
# http://localhost:12000
```

**游戏控制：**
- `W/A/S/D` - 移动飞船
- `空格键` - 射击
- `R` - 重新开始

### 👤 微信小程序版本 (个人开发者推荐)

✅ **适合个人开发者** - 个人主体可以发布微信小程序

1. **准备环境**
   - 下载微信开发者工具
   - 注册**小程序**开发者账号 (选择个人主体)

2. **导入项目**
   - 打开微信开发者工具
   - 选择**小程序**项目类型
   - 导入 `wechat-miniprogram-personal/` 目录
   - 输入小程序AppID

3. **开始游戏**
   - 点击编译运行
   - 在模拟器或真机上体验

📖 **详细发布指南**: 查看 `wechat-miniprogram-personal/PERSONAL-PUBLISH-GUIDE.md`  
🪟 **Windows 用户**: 查看 `wechat-miniprogram-personal/WINDOWS-GUIDE.md`

### 🎮 微信小游戏版本 (企业开发者)

⚠️ **需要企业主体** - 个人开发者无法发布小游戏

1. **准备环境**
   - 下载微信开发者工具
   - 注册**小游戏**开发者账号 (需要企业主体)

2. **导入项目**
   - 打开微信开发者工具
   - 选择**小游戏**项目类型
   - 导入 `wechat-minigame/` 目录
   - 输入小游戏AppID

📖 **详细发布指南**: 查看 `wechat-minigame/PUBLISH-GUIDE.md`

## 🎯 游戏玩法

### 基础操作
🛸 **移动** - 控制飞船灵活移动  
🔫 **射击** - 发射子弹消灭敌机  
🛡️ **躲避** - 避免与敌机碰撞  

### 得分系统
- 🎯 小型敌机：+10分
- 🎯 中型敌机：+20分  
- 🎯 大型敌机：+50分
- 🔥 连击奖励：额外加分

### 游戏目标
🏆 消灭更多敌机，获得更高分数，挑战自己的极限！

## 🛠️ 技术架构

### Web版本
- **HTML5 Canvas** - 高性能2D渲染
- **JavaScript ES6+** - 现代化游戏逻辑
- **Web Audio API** - 音效播放系统
- **CSS3** - 响应式界面设计

### 微信小游戏版本
- **Canvas 2D API** - 高性能游戏渲染
- **小游戏API** - 专业游戏开发接口
- **微信API** - 本地存储、分享功能
- **触控优化** - 移动端交互体验
- **60FPS** - 流畅游戏体验

## 📱 兼容性

### 🌐 Web浏览器
✅ Chrome 60+  
✅ Firefox 55+  
✅ Safari 11+  
✅ Edge 79+  
✅ 移动端浏览器  

### 🎮 微信小游戏
✅ iOS 微信 7.0+  
✅ Android 微信 7.0+  
✅ 基础库 2.19.4+  
✅ Canvas 2D 游戏引擎  

## 🔧 开发指南

### 本地开发
1. 克隆项目到本地
2. 选择对应平台版本
3. 按照快速开始指南运行
4. 开始开发和调试

### 自定义配置
- 修改 `game_config.js` 调整游戏参数
- 自定义敌机类型和行为模式
- 调整难度曲线和分数规则

## 📚 文档资源

- 📖 [项目结构详解](PROJECT-STRUCTURE.md)
- 🌐 [Web版本说明](docs/web-version-README.md)
- 👤 [个人开发者小程序指南](wechat-miniprogram-personal/PERSONAL-PUBLISH-GUIDE.md) ⭐
- 🎮 [企业开发者小游戏指南](wechat-minigame/PUBLISH-GUIDE.md)
- 📱 [微信小程序说明](wechat-miniprogram/README.md)

## 📄 许可证

本项目采用 MIT 许可证开源。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

🎮 **开始你的太空冒险之旅！** ✨