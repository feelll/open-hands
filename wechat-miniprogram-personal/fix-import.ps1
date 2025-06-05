# PowerShell 脚本：修复微信小程序导入问题

Write-Host "🔧 修复微信小程序导入问题..." -ForegroundColor Green

# 备份原配置文件
if (Test-Path "project.config.json") {
    Write-Host "📁 备份原配置文件..." -ForegroundColor Yellow
    Copy-Item "project.config.json" "project.config.backup.json"
}

# 使用简化配置文件
if (Test-Path "project.config.simple.json") {
    Write-Host "🔄 使用简化配置文件..." -ForegroundColor Yellow
    Copy-Item "project.config.simple.json" "project.config.json"
}

# 清理可能的缓存文件
Write-Host "🧹 清理缓存文件..." -ForegroundColor Yellow

$filesToRemove = @(".DS_Store", "package-lock.json")
$foldersToRemove = @("node_modules", ".vscode")

foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "  删除文件: $file" -ForegroundColor Gray
    }
}

foreach ($folder in $foldersToRemove) {
    if (Test-Path $folder) {
        Remove-Item $folder -Recurse -Force
        Write-Host "  删除文件夹: $folder" -ForegroundColor Gray
    }
}

Write-Host "✅ 修复完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📋 接下来的步骤：" -ForegroundColor Cyan
Write-Host "1. 在 project.config.json 中将 'testAppId' 替换为您的真实小程序AppID"
Write-Host "2. 在微信开发者工具中重新导入项目"
Write-Host "3. ⚠️  导入时手动选择项目类型为'小程序'"
Write-Host ""
Write-Host "🎯 如果仍有问题，请查看 IMPORT-TROUBLESHOOTING.md 获取更多解决方案" -ForegroundColor Magenta

Read-Host "按任意键继续..."