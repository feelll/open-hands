#!/usr/bin/env python3
import http.server
import socketserver
import os
import sys

# 设置端口
PORT = 12000

# 切换到游戏目录
os.chdir('/workspace/space-shooter-game')

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 添加CORS头部以允许跨域访问
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

# 创建服务器
with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
    print(f"太空射击游戏服务器启动在端口 {PORT}")
    print(f"访问游戏: https://work-1-kysoqxhmfuonxamu.prod-runtime.all-hands.dev")
    print("按 Ctrl+C 停止服务器")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        sys.exit(0)