#!/bin/bash

# 🔧 修复 game.json 未找到错误的快速脚本

echo "🔧 开始修复 game.json 错误..."

# 1. 备份当前文件
echo "📁 备份当前文件..."
cp pages/game/game.json pages/game/game.json.$(date +%Y%m%d_%H%M%S).backup 2>/dev/null

# 2. 创建最简化的 game.json
echo "📝 创建最简化配置..."
cat > pages/game/game.json << 'EOF'
{
  "navigationBarTitleText": "太空射击游戏"
}
EOF

# 3. 验证JSON格式
echo "✅ 验证JSON格式..."
if python3 -m json.tool pages/game/game.json > /dev/null 2>&1; then
    echo "✅ JSON格式正确"
else
    echo "❌ JSON格式错误，使用备用方案..."
    echo '{"navigationBarTitleText": "太空射击游戏"}' > pages/game/game.json
fi

# 4. 检查文件权限
echo "🔐 检查文件权限..."
chmod 644 pages/game/game.json

# 5. 显示文件内容
echo "📄 当前文件内容："
cat pages/game/game.json

echo ""
echo "🎯 修复完成！请按以下步骤操作："
echo "1. 关闭微信开发者工具"
echo "2. 重新打开微信开发者工具"
echo "3. 重新导入项目目录"
echo "4. 如果问题仍然存在，请查看 docs/FIX-GAME-JSON-ERROR.md"

echo ""
echo "✨ 修复脚本执行完成！"