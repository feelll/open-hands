from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from web_scraper import WebScraper
from data_analyzer import DataAnalyzer
import traceback

app = Flask(__name__)
CORS(app)

# 创建必要的目录
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)
os.makedirs('reports', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_website():
    try:
        data = request.get_json()
        url = data.get('url')
        use_selenium = data.get('use_selenium', False)
        
        if not url:
            return jsonify({'error': '请提供有效的URL'}), 400
        
        # 初始化组件
        scraper = WebScraper()
        analyzer = DataAnalyzer()
        
        # 抓取网页内容
        html_content = scraper.get_page_content(url, use_selenium)
        if not html_content:
            return jsonify({'error': '无法获取网页内容'}), 400
        
        # 提取数据
        extracted_data = scraper.extract_text_content(html_content)
        search_terms = scraper.extract_search_terms(extracted_data.get('text_content', ''))
        preferences = scraper.analyze_user_preferences(extracted_data)
        categories = scraper.categorize_content(extracted_data)
        
        # 生成分析报告
        report = analyzer.generate_comprehensive_report(
            url, extracted_data, search_terms, preferences, categories
        )
        
        # 保存报告
        report_filename = f"report_{hash(url) % 10000}.json"
        report_path = os.path.join('reports', report_filename)
        
        # 转换numpy类型为Python原生类型
        def convert_numpy_types(obj):
            if hasattr(obj, 'item'):
                return obj.item()
            elif isinstance(obj, dict):
                return {k: convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(v) for v in obj]
            else:
                return obj
        
        report_serializable = convert_numpy_types(report)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_serializable, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True,
            'report': report_serializable,
            'report_id': report_filename.replace('.json', '')
        })
        
    except Exception as e:
        print(f"分析过程中出错: {e}")
        print(traceback.format_exc())
        return jsonify({'error': f'分析失败: {str(e)}'}), 500

@app.route('/report/<report_id>')
def view_report(report_id):
    try:
        report_path = os.path.join('reports', f'{report_id}.json')
        if not os.path.exists(report_path):
            return "报告不存在", 404
        
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        return render_template('report.html', report=report)
    except Exception as e:
        return f"加载报告失败: {e}", 500

@app.route('/api/reports')
def list_reports():
    try:
        reports = []
        for filename in os.listdir('reports'):
            if filename.endswith('.json'):
                report_id = filename.replace('.json', '')
                report_path = os.path.join('reports', filename)
                with open(report_path, 'r', encoding='utf-8') as f:
                    report_data = json.load(f)
                
                reports.append({
                    'id': report_id,
                    'url': report_data.get('url', ''),
                    'title': report_data.get('basic_info', {}).get('title', ''),
                    'timestamp': report_data.get('timestamp', '')
                })
        
        # 按时间排序
        reports.sort(key=lambda x: x['timestamp'], reverse=True)
        return jsonify(reports)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=12000, debug=True)