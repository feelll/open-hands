# 微信公众号图片分类上传指南

## 🎯 功能概述

本系统现在支持根据 `downloads` 目录下的文件夹名称，自动将图片按分类上传到微信公众号，并在文件名中添加分类标识，方便在微信后台按分类查找和管理图片。

## 📁 目录结构

```
downloads/
├── 性感美女/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── 美女写真/
│   ├── photo1.jpg
│   ├── photo2.jpg
│   └── ...
├── 日韩美女/
│   └── ...
└── 其他分类/
    └── ...
```

## 🚀 核心功能

### 1. 自动分类标识
- **上传前**: `image1.jpg`
- **上传后**: `[性感美女]image1.jpg`
- 在微信后台搜索 `[性感美女]` 即可找到该分类的所有图片

### 2. 详细上传记录
每次上传都会生成：
- **JSON日志**: 包含完整的上传信息
- **Markdown报告**: 人性化的分类报告
- **分类摘要**: 统计信息和快速查找指南

### 3. 多种上传方式
- 上传所有分类
- 选择特定分类上传
- 单个分类上传
- 预览模式（不实际上传）

## 📖 使用方法

### 方法一：使用演示脚本（推荐新手）

```bash
python category_upload_demo.py
```

这个脚本提供交互式界面，引导您完成分类上传：

1. **查看分类**: 自动扫描并显示所有可用分类
2. **选择上传方式**: 
   - 上传所有分类
   - 选择特定分类
   - 仅预览（不上传）
3. **自动生成报告**: 完成后自动生成分类报告

### 方法二：使用分类管理工具（推荐高级用户）

```bash
# 查看所有分类
python category_manager.py --action list

# 查看统计信息
python category_manager.py --action stats

# 生成上传计划
python category_manager.py --action plan

# 预览上传文件名
python category_manager.py --action preview

# 上传所有分类
python category_manager.py --action upload --all

# 上传指定分类
python category_manager.py --action upload --categories "性感美女" "美女写真"
```

### 方法三：编程方式

```python
from wechat_uploader import WeChatUploader
from category_manager import CategoryManager

# 使用上传器
uploader = WeChatUploader()

# 上传单个分类
results = uploader.upload_images_from_directory("downloads/性感美女")

# 上传所有分类
all_results = uploader.upload_all_categories()

# 生成分类报告
uploader.generate_category_report(all_results, "my_report.md")

# 使用分类管理器
manager = CategoryManager()

# 获取分类信息
categories = manager.get_available_categories()

# 上传指定分类
results = manager.upload_multiple_categories(["性感美女", "美女写真"])
```

## 📊 生成的报告示例

### JSON日志 (`upload_log_*.json`)
```json
[
  {
    "original_filename": "beauty1.jpg",
    "upload_filename": "[性感美女]beauty1.jpg",
    "media_id": "xxx123xxx",
    "url": "https://...",
    "category": "性感美女",
    "file_path": "downloads/性感美女/beauty1.jpg",
    "upload_time": "2024-01-01 10:30:00"
  }
]
```

### Markdown报告 (`category_report_*.md`)
```markdown
# 微信公众号图片分类上传报告

生成时间: 2024-01-01 10:30:00
总计上传图片: 24 张
分类数量: 8 个

## 📊 分类统计
- **性感美女**: 5 张图片
- **美女写真**: 3 张图片
- **日韩美女**: 4 张图片

## 📁 分类详情
### 性感美女 (5 张)
| 上传文件名 | Media ID | 上传时间 |
|-----------|----------|----------|
| [性感美女]beauty1.jpg | `xxx123xxx` | 2024-01-01 10:30:00 |

## 🔍 微信后台查找指南
1. **按文件名搜索**: 搜索 `[性感美女]` 查看该分类所有图片
2. **按Media ID搜索**: 使用上表中的Media ID进行精确查找
```

## 🔍 微信后台使用指南

### 1. 按分类搜索图片
在微信公众号后台素材管理中：
- 搜索 `[性感美女]` - 查看性感美女分类的所有图片
- 搜索 `[美女写真]` - 查看美女写真分类的所有图片
- 搜索 `[日韩美女]` - 查看日韩美女分类的所有图片

### 2. 按时间筛选
- 同一批次上传的图片时间相近
- 可以按上传时间范围筛选特定批次的图片

### 3. 使用Media ID
- 每张图片都有唯一的Media ID
- 可以用于精确查找特定图片
- 在文章编辑时可以直接使用Media ID引用图片

## ⚙️ 配置说明

### 环境变量配置
```bash
# .env 文件
WECHAT_APPID=your_app_id
WECHAT_SECRET=your_app_secret
```

### 分类配置
在 `config.py` 中可以自定义分类映射：
```python
CATEGORIES = {
    "xgmn": "性感美女",
    "mnxz": "美女写真", 
    "yzmn": "日韩美女",
    # 添加更多分类...
}
```

## 🎨 高级功能

### 1. 自定义分类前缀
```python
# 自定义分类标识格式
uploader.upload_permanent_image("image.jpg", "我的分类")
# 结果: [我的分类]image.jpg
```

### 2. 批量重命名
```python
# 批量处理多个分类
manager = CategoryManager()
results = manager.upload_multiple_categories([
    "性感美女", "美女写真", "日韩美女"
])
```

### 3. 上传计划预览
```python
# 生成上传计划
plan = manager.generate_upload_plan()
print(f"预计上传 {plan['total_images']} 张图片")
print(f"预计耗时 {plan['estimated_time']} 秒")
```

## 🚨 注意事项

### 1. 微信API限制
- 永久素材图片限制：100,000张
- 临时素材有效期：3天
- 上传频率：建议每张图片间隔1-2秒

### 2. 文件格式支持
- 支持格式：JPG, JPEG, PNG, GIF, WEBP, BMP
- 文件大小：建议小于10MB
- 图片尺寸：建议不超过2048x2048

### 3. 分类命名建议
- 使用中文分类名，便于识别
- 避免特殊字符：`[]<>|:*?"/\`
- 保持分类名简洁明了

### 4. 网络和认证
- 确保网络连接稳定
- 定期检查微信Token是否有效
- 监控上传日志，及时发现问题

## 🔧 故障排除

### 常见问题

1. **Token获取失败**
   ```
   解决方案：检查WECHAT_APPID和WECHAT_SECRET配置
   ```

2. **上传失败**
   ```
   解决方案：检查图片格式、大小、网络连接
   ```

3. **分类目录不存在**
   ```
   解决方案：确保downloads目录下有对应的分类文件夹
   ```

### 调试模式
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 启用详细日志
uploader = WeChatUploader()
```

## 📈 最佳实践

### 1. 上传前准备
- 整理好分类目录结构
- 检查图片质量和格式
- 预览上传计划

### 2. 分批上传
- 大量图片建议分批上传
- 监控上传进度和成功率
- 保存好上传日志

### 3. 后期管理
- 定期整理微信素材库
- 使用生成的报告管理图片
- 建立图片使用记录

## 🎉 总结

通过这个分类上传系统，您可以：

✅ **自动化分类管理** - 根据目录结构自动分类
✅ **便捷搜索查找** - 在微信后台快速找到所需图片  
✅ **详细记录追踪** - 完整的上传日志和报告
✅ **灵活上传方式** - 支持多种上传模式
✅ **可视化管理** - 清晰的分类统计和预览

这样，您在发布微信文章时就能够快速找到对应分类的图片，大大提高工作效率！