# 🚀 太空射击游戏 - Space Shooter Game

一款完整的太空射击游戏，支持Web浏览器和微信小程序两个平台。

## 📁 项目结构

```
open-hands/
├── README.md                    # 项目主说明文档
├── web-version/                 # Web浏览器版本
│   ├── index.html              # 游戏主页面
│   ├── game.js                 # 游戏核心逻辑
│   └── game_config.js          # 游戏配置文件
├── wechat-miniprogram/         # 微信小程序版本
│   ├── app.js                  # 小程序入口文件
│   ├── app.json                # 全局配置
│   ├── app.wxss                # 全局样式
│   ├── pages/game/             # 游戏页面
│   ├── project.config.json     # 项目配置
│   ├── sitemap.json           # 搜索配置
│   ├── docs/                   # 文档目录
│   └── backup/                 # 备份文件
├── scripts/                    # 工具脚本
│   ├── server.py              # Web服务器
│   └── start_game.sh          # 启动脚本
└── docs/                       # 项目文档
    └── web-version-README.md   # Web版本说明
```

## 🎮 游戏特性

### 核心功能
- 🚀 流畅的飞船控制
- 🎯 精准的射击系统
- 👾 多种敌人类型
- 💥 炫酷的爆炸效果
- 🌟 动态星空背景
- 📊 分数和等级系统
- 💾 最高分记录

### 平台特性
- **Web版本**: 键盘控制，全屏游戏体验
- **微信小程序版本**: 触控操作，移动端优化

## 🚀 快速开始

### Web版本
```bash
cd web-version
python3 -m http.server 8000
# 访问 http://localhost:8000
```

### 微信小程序版本
1. 使用微信开发者工具打开 `wechat-miniprogram` 目录
2. 配置 AppID: `wx111e2c910275e57d`
3. 编译并预览

## 📖 详细文档

- [Web版本说明](docs/web-version-README.md)
- [微信小程序说明](wechat-miniprogram/README.md)
- [故障排除指南](wechat-miniprogram/docs/TROUBLESHOOTING.md)
- [部署指南](wechat-miniprogram/docs/deploy.md)

## 🛠️ 技术栈

- **Web版本**: HTML5 Canvas, JavaScript ES6+
- **微信小程序版本**: Canvas 2D API, 微信小程序框架
- **工具**: Python HTTP服务器, Bash脚本

## 📱 兼容性

- **Web浏览器**: Chrome 60+, Firefox 55+, Safari 12+
- **微信小程序**: 基础库 3.0.2+, iOS 9.0+, Android 5.0+

## 🎯 游戏控制

### Web版本
- **移动**: WASD 或 方向键
- **射击**: 空格键
- **暂停**: P键

### 微信小程序版本
- **移动**: 触摸屏幕拖拽 或 虚拟按键
- **射击**: 点击射击按钮 或 触摸屏幕
- **暂停**: 点击暂停按钮

## 🏆 游戏目标

- 消灭敌人获得分数
- 避免碰撞保持生命值
- 挑战更高等级和分数
- 创造个人最高记录

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进游戏！

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

🎮 **开始游戏，享受太空射击的乐趣！** 🚀