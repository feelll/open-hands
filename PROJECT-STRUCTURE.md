# 📁 项目结构详解

## 🎯 设计理念

采用清晰的分层架构，将不同平台版本、工具脚本和文档分别组织，便于开发、维护和扩展。

## 📂 目录结构

```
📦 open-hands/                       # 项目根目录
├── 📄 README.md                     # 项目主说明文档
├── 📄 PROJECT-STRUCTURE.md          # 项目结构说明（本文件）
│
├── 🌐 web-version/                  # Web浏览器版本
│   ├── 🏠 index.html                # 游戏主页面
│   ├── 🎮 game.js                   # 游戏核心逻辑
│   └── ⚙️ game_config.js            # 游戏配置文件
│
├── 📱 wechat-miniprogram/           # 微信小程序版本
│   ├── 🚀 app.js                    # 小程序入口文件
│   ├── ⚙️ app.json                  # 全局配置
│   ├── 🎨 app.wxss                  # 全局样式
│   ├── 🔧 project.config.json       # 项目配置
│   ├── 🗺️ sitemap.json              # 搜索配置
│   ├── 📖 README.md                 # 小程序说明文档
│   │
│   ├── 📄 pages/                    # 页面目录
│   │   └── game/                    # 游戏页面
│   │       ├── 🎮 game.js           # 页面逻辑
│   │       ├── ⚙️ game.json         # 页面配置
│   │       ├── 🏗️ game.wxml         # 页面结构
│   │       └── 🎨 game.wxss         # 页面样式
│   │
│   ├── 📚 docs/                     # 文档目录
│   │   ├── 🔧 TROUBLESHOOTING.md    # 故障排除指南
│   │   ├── ⚡ QUICK-FIX.md          # 快速修复指南
│   │   ├── 🛠️ FIX-GAME-JS.md        # game.js问题修复
│   │   └── 🚀 deploy.md             # 部署指南
│   │
│   └── 🗄️ backup/                   # 备份文件
│       ├── game-original.js         # 原始游戏文件
│       ├── game-complex.js          # 复杂版本备份
│       └── game-test.*              # 测试版本文件
│
├── 🛠️ scripts/                      # 工具脚本
│   ├── 🌐 server.py                 # Web服务器脚本
│   └── 🚀 start_game.sh             # 游戏启动脚本
│
└── 📚 docs/                         # 项目文档
    └── 📖 web-version-README.md     # Web版本详细说明
```

## 🏗️ 架构设计

### 🌐 Web版本架构
```
web-version/
├── index.html      # 游戏入口页面
├── game.js         # 游戏引擎核心
└── game_config.js  # 配置参数
```

**特点：**
- 🎯 **简洁明了** - 最小化文件结构
- 🔧 **易于修改** - 配置与逻辑分离
- 🚀 **快速部署** - 静态文件直接运行

### 📱 微信小程序架构
```
wechat-miniprogram/
├── app.*           # 应用全局文件
├── pages/game/     # 游戏页面
├── docs/           # 文档支持
└── backup/         # 版本备份
```

**特点：**
- 📋 **标准结构** - 遵循小程序规范
- 📚 **文档完善** - 详细的使用指南
- 🔄 **版本管理** - 完整的备份机制

## 🎯 设计优势

### ✅ 平台分离
- **独立开发** - 两个平台完全分离，互不干扰
- **专门优化** - 每个平台都有针对性的优化
- **维护简单** - 修改一个平台不影响另一个

### ✅ 结构清晰
- **功能分组** - 按功能和用途分组文件
- **层次分明** - 清晰的目录层次结构
- **易于导航** - 快速找到需要的文件

### ✅ 扩展性强
- **模块化设计** - 便于添加新功能
- **标准化结构** - 遵循最佳实践
- **文档支持** - 完善的文档体系

## 🚀 使用指南

### Web版本开发
```bash
# 进入Web版本目录
cd web-version/

# 启动开发服务器
../scripts/start_game.sh

# 或手动启动
python3 -m http.server 12000
```

### 微信小程序开发
```bash
# 使用微信开发者工具
# 1. 打开微信开发者工具
# 2. 导入项目：选择 wechat-miniprogram/ 目录
# 3. 配置AppID并开始开发
```

### 工具脚本使用
```bash
# 启动Web服务器
./scripts/start_game.sh

# 查看服务器代码
cat scripts/server.py
```

## 📋 维护建议

### 🔄 日常维护
1. **保持结构** - 新增文件时遵循现有结构
2. **文档同步** - 修改功能时更新相关文档
3. **版本备份** - 重要修改前先备份
4. **代码同步** - 保持两个平台核心逻辑一致

### 🔮 未来扩展
可以考虑添加的目录：
- `assets/` - 游戏资源文件（图片、音频）
- `tests/` - 自动化测试文件
- `build/` - 构建输出目录
- `config/` - 环境配置文件
- `utils/` - 通用工具函数

## 📊 文件统计

| 目录 | 文件数 | 主要类型 | 用途 |
|------|--------|----------|------|
| web-version/ | 3 | HTML, JS | Web游戏 |
| wechat-miniprogram/ | 10+ | JS, JSON, WXML, WXSS | 小程序 |
| scripts/ | 2 | Python, Bash | 工具脚本 |
| docs/ | 5+ | Markdown | 文档说明 |

---

📁 **结构清晰，开发高效！** ✨