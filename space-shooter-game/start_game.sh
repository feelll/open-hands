#!/bin/bash

echo "🚀 启动太空射击游戏服务器..."
echo "================================"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 切换到游戏目录
cd "$(dirname "$0")"

echo "📁 当前目录: $(pwd)"
echo "🌐 启动HTTP服务器在端口 12000..."

# 启动服务器
python3 server.py

echo "🎮 游戏服务器已停止"