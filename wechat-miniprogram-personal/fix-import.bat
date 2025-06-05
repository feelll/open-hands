@echo off
chcp 65001 >nul
echo 🔧 修复微信小程序导入问题...

REM 备份原配置文件
if exist "project.config.json" (
    echo 📁 备份原配置文件...
    copy "project.config.json" "project.config.backup.json" >nul
)

REM 使用简化配置文件
if exist "project.config.simple.json" (
    echo 🔄 使用简化配置文件...
    copy "project.config.simple.json" "project.config.json" >nul
)

REM 清理可能的缓存文件
echo 🧹 清理缓存文件...
if exist ".DS_Store" del ".DS_Store" >nul 2>&1
if exist "node_modules" rmdir /s /q "node_modules" >nul 2>&1
if exist "package-lock.json" del "package-lock.json" >nul 2>&1
if exist ".vscode" rmdir /s /q ".vscode" >nul 2>&1

echo ✅ 修复完成！
echo.
echo 📋 接下来的步骤：
echo 1. 在 project.config.json 中将 'testAppId' 替换为您的真实小程序AppID
echo 2. 在微信开发者工具中重新导入项目
echo 3. ⚠️  导入时手动选择项目类型为'小程序'
echo.
echo 🎯 如果仍有问题，请查看 IMPORT-TROUBLESHOOTING.md 获取更多解决方案
pause