# 📁 项目结构说明

## 🎯 整理目标

将原本混乱的项目结构重新组织为清晰、规范的目录结构，便于维护和开发。

## 📂 新的目录结构

```
open-hands/                          # 项目根目录
├── README.md                        # 项目主说明文档
├── PROJECT-STRUCTURE.md             # 项目结构说明（本文件）
│
├── web-version/                     # 🌐 Web浏览器版本
│   ├── index.html                   # 游戏主页面
│   ├── game.js                      # 游戏核心逻辑
│   └── game_config.js               # 游戏配置文件
│
├── wechat-miniprogram/              # 📱 微信小程序版本
│   ├── app.js                       # 小程序入口文件
│   ├── app.json                     # 全局配置
│   ├── app.wxss                     # 全局样式
│   ├── project.config.json          # 项目配置
│   ├── sitemap.json                 # 搜索配置
│   ├── README.md                    # 小程序说明文档
│   │
│   ├── pages/                       # 页面目录
│   │   └── game/                    # 游戏页面
│   │       ├── game.js              # 页面逻辑
│   │       ├── game.json            # 页面配置
│   │       ├── game.wxml            # 页面结构
│   │       └── game.wxss            # 页面样式
│   │
│   ├── docs/                        # 📖 文档目录
│   │   ├── TROUBLESHOOTING.md       # 故障排除指南
│   │   ├── QUICK-FIX.md             # 快速修复指南
│   │   ├── FIX-GAME-JS.md           # game.js问题修复
│   │   └── deploy.md                # 部署指南
│   │
│   └── backup/                      # 🗄️ 备份文件
│       ├── game-original.js         # 原始游戏文件
│       ├── game-complex.js          # 复杂版本备份
│       └── game-test.*              # 测试版本文件
│
├── scripts/                         # 🛠️ 工具脚本
│   ├── server.py                    # Web服务器脚本
│   └── start_game.sh                # 游戏启动脚本
│
└── docs/                            # 📚 项目文档
    └── web-version-README.md        # Web版本详细说明
```

## 🔄 整理过程

### 1. 原始结构问题
- 所有文件混在 `space-shooter-game/` 目录下
- Web版本和微信小程序版本文件混合
- 文档和备份文件散乱分布
- 缺乏清晰的分类和层次

### 2. 整理步骤
1. **创建顶级目录**: `web-version/`, `wechat-miniprogram/`, `scripts/`, `docs/`
2. **分离平台版本**: Web文件移至 `web-version/`，小程序文件移至 `wechat-miniprogram/`
3. **整理工具脚本**: 服务器和启动脚本移至 `scripts/`
4. **归类文档**: 各类文档移至对应的 `docs/` 目录
5. **清理备份文件**: 测试和备份文件移至 `backup/` 目录
6. **删除冗余**: 移除原始的混乱目录结构

### 3. 文件迁移映射

| 原路径 | 新路径 | 说明 |
|--------|--------|------|
| `space-shooter-game/index.html` | `web-version/index.html` | Web游戏主页 |
| `space-shooter-game/game.js` | `web-version/game.js` | Web游戏逻辑 |
| `space-shooter-game/game_config.js` | `web-version/game_config.js` | Web游戏配置 |
| `space-shooter-game/server.py` | `scripts/server.py` | Web服务器 |
| `space-shooter-game/start_game.sh` | `scripts/start_game.sh` | 启动脚本 |
| `space-shooter-game/wechat-miniprogram/*` | `wechat-miniprogram/*` | 小程序文件 |
| `space-shooter-game/README.md` | `docs/web-version-README.md` | Web版本说明 |

## 🎯 整理效果

### ✅ 优势
1. **清晰分离**: Web版本和小程序版本完全分离
2. **便于维护**: 每个平台有独立的目录结构
3. **文档集中**: 相关文档归类到对应目录
4. **备份安全**: 重要的备份文件妥善保存
5. **脚本独立**: 工具脚本单独管理

### 🚀 使用指南

#### Web版本开发
```bash
cd web-version/
# 直接编辑 HTML/JS 文件
# 使用 ../scripts/start_game.sh 启动服务器
```

#### 微信小程序开发
```bash
cd wechat-miniprogram/
# 使用微信开发者工具打开此目录
# 查看 docs/ 目录获取帮助文档
```

#### 运行游戏
```bash
# 从项目根目录
./scripts/start_game.sh
```

## 📋 维护建议

1. **保持结构**: 新增文件时遵循现有目录结构
2. **文档更新**: 修改功能时同步更新相关文档
3. **备份管理**: 重要修改前先备份到 `backup/` 目录
4. **版本同步**: 两个平台的核心游戏逻辑保持同步

## 🔮 未来扩展

可以考虑添加的目录：
- `assets/` - 游戏资源文件（图片、音频等）
- `tests/` - 自动化测试文件
- `build/` - 构建输出目录
- `config/` - 环境配置文件

---

📁 **整理完成！现在项目结构清晰明了，便于开发和维护。** ✨