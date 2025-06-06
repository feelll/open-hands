"""
Web演示界面
"""
import os
import json
from flask import Flask, render_template_string, jsonify, request
from config import CATEGORIES, DOWNLOAD_DIR

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>图片下载和微信公众号上传工具</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }
        .content {
            padding: 30px;
        }
        .section {
            margin-bottom: 40px;
        }
        .section h2 {
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }
        .stat-label {
            color: #666;
            font-size: 0.9em;
        }
        .categories-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .category-card {
            background: #f8f9fa;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .category-card:hover {
            transform: translateY(-5px);
        }
        .category-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            font-weight: bold;
        }
        .category-content {
            padding: 15px;
        }
        .image-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 10px;
            margin-top: 10px;
        }
        .image-item {
            aspect-ratio: 1;
            background: #ddd;
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }
        .image-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .image-placeholder {
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            font-size: 0.8em;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }
        .feature-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .feature-icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
        .feature-title {
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        .feature-desc {
            color: #666;
            font-size: 0.9em;
        }
        .upload-log {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
        }
        .log-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .log-item:last-child {
            border-bottom: none;
        }
        .log-filename {
            font-weight: bold;
            color: #333;
        }
        .log-status {
            background: #28a745;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
        }
        .footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 40px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖼️ 图片下载和微信公众号上传工具</h1>
            <p>自动化图片采集与管理解决方案</p>
        </div>
        
        <div class="content">
            <!-- 统计信息 -->
            <div class="section">
                <h2>📊 项目统计</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{{ stats.total_categories }}</div>
                        <div class="stat-label">支持分类</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ stats.total_images }}</div>
                        <div class="stat-label">已下载图片</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ stats.uploaded_images }}</div>
                        <div class="stat-label">已上传图片</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{{ stats.success_rate }}%</div>
                        <div class="stat-label">成功率</div>
                    </div>
                </div>
            </div>

            <!-- 功能特性 -->
            <div class="section">
                <h2>✨ 核心功能</h2>
                <div class="features">
                    <div class="feature-card">
                        <div class="feature-icon">🕷️</div>
                        <div class="feature-title">智能爬虫</div>
                        <div class="feature-desc">自动解析网站结构，智能提取图片链接，支持多种反爬虫策略</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📁</div>
                        <div class="feature-title">分类管理</div>
                        <div class="feature-desc">按网站分类自动整理图片，支持8个主要美女图片分类</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">☁️</div>
                        <div class="feature-title">微信上传</div>
                        <div class="feature-desc">自动上传到微信公众号素材库，支持批量处理和进度跟踪</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📝</div>
                        <div class="feature-title">日志记录</div>
                        <div class="feature-desc">详细的操作日志，包括下载状态、上传结果和错误信息</div>
                    </div>
                </div>
            </div>

            <!-- 图片分类 -->
            <div class="section">
                <h2>🎨 图片分类</h2>
                <div class="categories-grid">
                    {% for category_code, category_info in categories.items() %}
                    <div class="category-card">
                        <div class="category-header">
                            {{ category_info.name }} ({{ category_code }})
                        </div>
                        <div class="category-content">
                            <p><strong>图片数量:</strong> {{ category_info.count }} 张</p>
                            <div class="image-grid">
                                {% set max_images = 6 if category_info.count > 6 else category_info.count %}
                                {% for i in range(max_images) %}
                                <div class="image-item">
                                    <div class="image-placeholder">IMG</div>
                                </div>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>

            <!-- 上传日志 -->
            {% if upload_logs %}
            <div class="section">
                <h2>📤 最近上传记录</h2>
                <div class="upload-log">
                    {% for log in upload_logs[:10] %}
                    <div class="log-item">
                        <div>
                            <div class="log-filename">{{ log.filename }}</div>
                            <div style="font-size: 0.8em; color: #666;">{{ log.upload_time }}</div>
                        </div>
                        <div class="log-status">{{ log.status }}</div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            <!-- 使用说明 -->
            <div class="section">
                <h2>📖 使用说明</h2>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px;">
                    <h3>基本使用</h3>
                    <pre style="background: #333; color: #fff; padding: 15px; border-radius: 4px; overflow-x: auto;">
# 检查配置
python main.py --check-config

# 下载所有分类
python main.py --download

# 下载指定分类
python main.py --download --category xgmn

# 上传到微信公众号
python main.py --upload

# 完整流程
python main.py</pre>

                    <h3>配置微信公众号</h3>
                    <ol>
                        <li>复制 <code>.env.example</code> 为 <code>.env</code></li>
                        <li>在 <code>.env</code> 中填入微信公众号的 AppID 和 Secret</li>
                        <li>运行程序即可自动上传图片到素材库</li>
                    </ol>
                </div>
            </div>
        </div>

        <div class="footer">
            <p>&copy; 2025 图片下载和微信公众号上传工具 | 仅供学习和研究使用</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # 统计信息
    stats = get_project_stats()
    
    # 分类信息
    categories = get_categories_info()
    
    # 上传日志
    upload_logs = get_upload_logs()
    
    return render_template_string(HTML_TEMPLATE, 
                                stats=stats, 
                                categories=categories,
                                upload_logs=upload_logs)

def get_project_stats():
    """获取项目统计信息"""
    total_categories = len(CATEGORIES)
    total_images = 0
    uploaded_images = 0
    
    # 统计下载的图片数量
    if os.path.exists(DOWNLOAD_DIR):
        for category_name in CATEGORIES.values():
            category_dir = os.path.join(DOWNLOAD_DIR, category_name)
            if os.path.exists(category_dir):
                images = [f for f in os.listdir(category_dir) 
                         if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
                total_images += len(images)
    
    # 统计上传的图片数量
    upload_log_files = ['demo_upload_log.json', 'upload_log.json', 'upload_log_all.json']
    for log_file in upload_log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    uploaded_images += len([log for log in logs if log.get('status') == 'success'])
                break
            except:
                pass
    
    success_rate = int((uploaded_images / total_images * 100) if total_images > 0 else 0)
    
    return {
        'total_categories': total_categories,
        'total_images': total_images,
        'uploaded_images': uploaded_images,
        'success_rate': success_rate
    }

def get_categories_info():
    """获取分类信息"""
    categories = {}
    
    for code, name in CATEGORIES.items():
        category_dir = os.path.join(DOWNLOAD_DIR, name)
        count = 0
        
        if os.path.exists(category_dir):
            images = [f for f in os.listdir(category_dir) 
                     if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp'))]
            count = len(images)
        
        categories[code] = {
            'name': name,
            'count': count
        }
    
    return categories

def get_upload_logs():
    """获取上传日志"""
    upload_log_files = ['demo_upload_log.json', 'upload_log.json', 'upload_log_all.json']
    
    for log_file in upload_log_files:
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
                    return sorted(logs, key=lambda x: x.get('upload_time', ''), reverse=True)
            except:
                pass
    
    return []

if __name__ == '__main__':
    print("启动Web演示界面...")
    print("访问地址: http://localhost:12001")
    app.run(host='0.0.0.0', port=12001, debug=False)