# 🪟 Windows 系统使用指南

## 🔧 运行修复脚本

### 方法一：使用 .bat 文件（推荐）

Windows 用户可以直接运行 `.bat` 文件：

```cmd
# 双击运行
fix-import.bat

# 或在命令提示符中运行
fix-import.bat
```

### 方法二：使用 PowerShell 脚本

如果您喜欢 PowerShell：

```powershell
# 右键点击文件夹，选择"在此处打开 PowerShell 窗口"
# 或在 PowerShell 中运行
.\fix-import.ps1

# 如果遇到执行策略问题，先运行：
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 方法三：手动执行修复步骤

如果不想运行脚本，可以手动执行以下步骤：

1. **备份配置文件**
   ```cmd
   copy project.config.json project.config.backup.json
   ```

2. **使用简化配置**
   ```cmd
   copy project.config.simple.json project.config.json
   ```

3. **清理缓存文件**
   ```cmd
   del .DS_Store
   rmdir /s /q node_modules
   del package-lock.json
   rmdir /s /q .vscode
   ```

4. **修改 AppID**
   - 用记事本打开 `project.config.json`
   - 将 `"testAppId"` 替换为您的真实小程序AppID
   - 保存文件

## 🚀 运行 .sh 脚本的方法

如果您想运行 `.sh` 脚本，有以下几种方法：

### 方法一：Git Bash（推荐）

1. **安装 Git for Windows**
   - 下载：https://git-scm.com/download/win
   - 安装时会自动包含 Git Bash

2. **运行脚本**
   ```bash
   # 右键点击文件夹，选择 "Git Bash Here"
   # 或打开 Git Bash 并导航到项目目录
   cd /path/to/wechat-miniprogram-personal
   ./fix-import.sh
   ```

### 方法二：WSL (Windows Subsystem for Linux)

1. **启用 WSL**
   ```powershell
   # 以管理员身份运行 PowerShell
   wsl --install
   ```

2. **运行脚本**
   ```bash
   # 在 WSL 中导航到项目目录
   cd /mnt/c/path/to/wechat-miniprogram-personal
   chmod +x fix-import.sh
   ./fix-import.sh
   ```

### 方法三：PowerShell

1. **安装 PowerShell Core**
   - 下载：https://github.com/PowerShell/PowerShell

2. **运行脚本**
   ```powershell
   # PowerShell 可以直接运行一些 bash 命令
   # 但建议使用 .bat 文件
   ```

### 方法四：Cygwin

1. **安装 Cygwin**
   - 下载：https://www.cygwin.com/

2. **运行脚本**
   ```bash
   # 在 Cygwin 终端中
   cd /cygdrive/c/path/to/wechat-miniprogram-personal
   ./fix-import.sh
   ```

## 📋 推荐方案

对于 Windows 用户，我们推荐以下顺序：

1. **首选**：直接双击运行 `fix-import.bat`
2. **备选**：PowerShell 运行 `fix-import.ps1`
3. **进阶**：使用 Git Bash 运行 `fix-import.sh`
4. **最后**：手动执行修复步骤

### 🎯 各方案对比

| 方案 | 难度 | 兼容性 | 推荐度 |
|------|------|--------|--------|
| .bat 文件 | ⭐ 简单 | ✅ 所有Windows | ⭐⭐⭐⭐⭐ |
| PowerShell | ⭐⭐ 简单 | ✅ Windows 7+ | ⭐⭐⭐⭐ |
| Git Bash | ⭐⭐⭐ 中等 | ⚠️ 需安装Git | ⭐⭐⭐ |
| 手动操作 | ⭐⭐ 简单 | ✅ 所有系统 | ⭐⭐ |

## 🎯 微信开发者工具导入步骤

无论使用哪种修复方法，最终都需要：

1. **打开微信开发者工具**
2. **点击"导入项目"**
3. **选择项目目录**
4. **⚠️ 重要：手动选择"小程序"类型**
5. **输入您的小程序AppID**
6. **点击确定**

## ❓ 常见问题

### Q: 双击 .bat 文件没有反应？
A: 右键点击 .bat 文件，选择"以管理员身份运行"

### Q: 提示找不到文件？
A: 确保在 `wechat-miniprogram-personal` 目录中运行脚本

### Q: 中文显示乱码？
A: .bat 文件已设置 UTF-8 编码，如果仍有问题，请使用 Git Bash

### Q: 没有安装 Git？
A: 可以直接手动执行修复步骤，或下载安装 Git for Windows

---

🪟 **Windows 用户现在可以轻松修复导入问题了！**