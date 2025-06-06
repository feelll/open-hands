# 图片下载和微信公众号上传工具

这是一个自动化工具，可以从 3gbizhi.com 网站下载美女图片，并按分类整理后自动上传到微信公众号图片库。

## 功能特性

- 🖼️ 自动下载指定网站的图片
- 📁 按网站分类自动整理图片到不同目录
- 📤 自动上传图片到微信公众号素材库
- 🔄 支持断点续传，避免重复下载
- 📊 详细的日志记录和进度显示
- ⚙️ 灵活的配置选项

## 支持的图片分类

- 性感美女 (xgmn)
- 美女写真 (mnxz)
- 日韩美女 (yzmn)
- 欧美美女 (ommn)
- 美女照片 (mnzp)
- 外国美女 (wgmn)
- 比基尼美女 (bjnmn)
- 翘臀美女 (dmmn)

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制配置文件模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入微信公众号信息：
```
WECHAT_APPID=your_wechat_appid
WECHAT_SECRET=your_wechat_secret
```

## 使用方法

### 检查配置
```bash
python main.py --check-config
```

### 下载所有分类的图片
```bash
python main.py --download
```

### 下载指定分类的图片
```bash
python main.py --download --category xgmn
```

### 上传图片到微信公众号
```bash
python main.py --upload
```

### 下载并上传（完整流程）
```bash
python main.py --all
```

### 指定分类的完整流程
```bash
python main.py --category xgmn
```

## 目录结构

```
image_downloader/
├── main.py              # 主程序入口
├── image_scraper.py     # 图片爬虫模块
├── wechat_uploader.py   # 微信上传模块
├── config.py            # 配置文件
├── requirements.txt     # 依赖包列表
├── .env                 # 环境变量配置
├── downloads/           # 图片下载目录
│   ├── 性感美女/
│   ├── 美女写真/
│   └── ...
├── app.log             # 应用日志
├── scraper.log         # 爬虫日志
└── upload_log.json     # 上传记录
```

## 配置说明

### 基础配置 (config.py)

- `MAX_IMAGES_PER_CATEGORY`: 每个分类最大下载图片数量
- `DELAY_BETWEEN_REQUESTS`: 请求间隔时间（秒）
- `MAX_WORKERS`: 最大并发线程数

### 微信公众号配置

需要在微信公众平台获取：
- `WECHAT_APPID`: 公众号的AppID
- `WECHAT_SECRET`: 公众号的AppSecret

## 注意事项

1. **合规使用**: 请确保下载的图片用途合法合规
2. **频率控制**: 程序已内置请求频率控制，避免对目标网站造成压力
3. **微信限制**: 微信公众号素材库有数量限制，请注意管理
4. **网络环境**: 确保网络连接稳定，支持访问目标网站和微信API

## 日志文件

- `app.log`: 主程序日志
- `scraper.log`: 爬虫详细日志
- `upload_log.json`: 上传记录（包含media_id等信息）

## 故障排除

### 下载失败
- 检查网络连接
- 确认目标网站可访问
- 查看 `scraper.log` 了解详细错误

### 上传失败
- 检查微信公众号配置
- 确认AppID和Secret正确
- 检查网络是否能访问微信API

### 权限问题
- 确保有写入下载目录的权限
- 检查日志文件的写入权限

## 开发说明

### 添加新的图片源
1. 在 `config.py` 中添加新的分类
2. 在 `image_scraper.py` 中适配新网站的HTML结构
3. 更新解析逻辑

### 扩展上传功能
可以在 `wechat_uploader.py` 中添加其他平台的上传功能，如：
- 微博图床
- 七牛云存储
- 阿里云OSS

## 许可证

本项目仅供学习和研究使用，请遵守相关法律法规和网站使用条款。