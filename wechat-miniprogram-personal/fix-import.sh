#!/bin/bash

# 微信小程序导入问题修复脚本

echo "🔧 修复微信小程序导入问题..."

# 备份原配置文件
if [ -f "project.config.json" ]; then
    echo "📁 备份原配置文件..."
    cp project.config.json project.config.backup.json
fi

# 使用简化配置文件
if [ -f "project.config.simple.json" ]; then
    echo "🔄 使用简化配置文件..."
    cp project.config.simple.json project.config.json
fi

# 清理可能的缓存文件
echo "🧹 清理缓存文件..."
rm -f .DS_Store
rm -rf node_modules/
rm -f package-lock.json
rm -rf .vscode/

echo "✅ 修复完成！"
echo ""
echo "📋 接下来的步骤："
echo "1. 在 project.config.json 中将 'testAppId' 替换为您的真实小程序AppID"
echo "2. 在微信开发者工具中重新导入项目"
echo "3. ⚠️  导入时手动选择项目类型为'小程序'"
echo ""
echo "🎯 如果仍有问题，请查看 IMPORT-TROUBLESHOOTING.md 获取更多解决方案"