# 微信小程序游戏故障排除指南

## 🔧 常见错误及解决方案

### 1. ReferenceError: Trace is not defined

**错误描述**:
```
ReferenceError: Trace is not defined
at http://127.0.0.1:40590/__pageframe__/__dev__/WARemoteDebugForLib3.js
```

**解决方案**:
1. 更新基础库版本到 3.0.2 或更高
2. 在 `project.config.json` 中修改：
   ```json
   {
     "libVersion": "3.0.2"
   }
   ```
3. 重新编译项目

### 2. TypeError: requestAnimationFrame is not a function

**错误描述**:
```
TypeError: requestAnimationFrame is not a function
at Br.gameLoop (game.js? [sm]:179)
```

**解决方案**:
已在代码中使用 `setTimeout` 替代 `requestAnimationFrame`：
```javascript
// 使用 setTimeout 替代 requestAnimationFrame
this.gameLoopId = setTimeout(() => this.gameLoop(), 1000 / 30);
```

### 3. Canvas 初始化失败

**错误描述**:
- Canvas 无法正常显示
- 游戏画面空白

**解决方案**:
1. 确保 Canvas 类型设置正确：
   ```xml
   <canvas type="2d" id="gameCanvas" class="game-canvas"></canvas>
   ```

2. 检查 Canvas 尺寸设置：
   ```javascript
   const dpr = systemInfo.pixelRatio || 2;
   canvas.width = res[0].width * dpr;
   canvas.height = res[0].height * dpr;
   ctx.scale(dpr, dpr);
   ```

### 4. 触控操作不响应

**错误描述**:
- 触摸屏幕无法移动飞船
- 按钮点击无反应

**解决方案**:
1. 检查事件绑定：
   ```xml
   bindtouchstart="onTouchStart"
   bindtouchmove="onTouchMove"
   bindtouchend="onTouchEnd"
   ```

2. 确保事件处理函数正确：
   ```javascript
   onTouchStart(e) {
     this.touchStartX = e.touches[0].x;
     this.touchStartY = e.touches[0].y;
   }
   ```

### 5. 游戏性能问题

**症状**:
- 游戏卡顿
- 帧率过低
- 内存占用过高

**解决方案**:
1. 降低游戏帧率：
   ```javascript
   setTimeout(() => this.gameLoop(), 1000 / 30); // 30 FPS
   ```

2. 减少游戏对象数量：
   ```javascript
   // 减少星星数量
   for (let i = 0; i < 30; i++) { // 原来是 50
     this.stars.push(new Star(this.canvasWidth, this.canvasHeight));
   }
   
   // 减少粒子数量
   for (let i = 0; i < 5; i++) { // 原来是 8
     this.particles.push({...});
   }
   ```

3. 优化渲染循环：
   ```javascript
   // 减少UI更新频率
   if (Date.now() % 5 === 0) {
     this.setData({
       score: this.gameState.score,
       lives: this.gameState.lives
     });
   }
   ```

### 6. 本地存储问题

**错误描述**:
- 最高分无法保存
- 数据丢失

**解决方案**:
1. 使用正确的存储API：
   ```javascript
   // 保存数据
   wx.setStorageSync('highScore', this.gameState.score);
   
   // 读取数据
   const highScore = wx.getStorageSync('highScore') || 0;
   ```

2. 添加错误处理：
   ```javascript
   try {
     wx.setStorageSync('highScore', this.gameState.score);
   } catch (error) {
     console.error('Storage failed:', error);
   }
   ```

### 7. 分享功能问题

**错误描述**:
- 分享按钮无效果
- 分享内容不正确

**解决方案**:
1. 启用分享功能：
   ```javascript
   shareGame() {
     wx.showShareMenu({
       withShareTicket: true
     });
   }
   ```

2. 自定义分享内容（在页面中添加）：
   ```javascript
   onShareAppMessage() {
     return {
       title: '太空射击游戏 - 挑战你的反应速度！',
       path: '/pages/game/game',
       imageUrl: '/images/share-image.png' // 可选
     };
   }
   ```

## 🛠️ 调试技巧

### 1. 开启调试模式
在微信开发者工具中：
- 点击"调试器"
- 查看 Console 输出
- 监控 Network 请求
- 检查 Storage 数据

### 2. 性能监控
```javascript
// 添加性能监控
console.time('gameLoop');
this.gameLoop();
console.timeEnd('gameLoop');

// 监控内存使用
console.log('Objects count:', {
  bullets: this.bullets.length,
  enemies: this.enemies.length,
  explosions: this.explosions.length
});
```

### 3. 错误捕获
```javascript
// 全局错误处理
App({
  onError(error) {
    console.error('App Error:', error);
    wx.showToast({
      title: '游戏出现错误',
      icon: 'none'
    });
  }
});

// 页面错误处理
Page({
  onError(error) {
    console.error('Page Error:', error);
  }
});
```

## 📱 设备兼容性

### 支持的设备
- iOS 9.0+ 
- Android 5.0+
- 微信版本 7.0+

### 已知问题
1. **低端设备**: 可能出现性能问题，建议进一步降低帧率
2. **小屏设备**: UI 可能需要调整，使用 rpx 单位确保适配
3. **旧版微信**: 某些 API 可能不支持，需要做兼容性检查

## 🔍 测试清单

发布前请确保以下功能正常：

- [ ] 游戏正常启动和初始化
- [ ] 触控移动和按键控制正常
- [ ] 射击功能正常
- [ ] 敌人生成和碰撞检测正常
- [ ] 分数和等级系统正常
- [ ] 游戏结束和重新开始正常
- [ ] 最高分保存和读取正常
- [ ] 分享功能正常
- [ ] 暂停和继续功能正常
- [ ] 在不同设备上测试性能
- [ ] 长时间游戏无内存泄漏

## 📞 获取帮助

如果以上解决方案无法解决问题，可以：

1. 查看微信小程序官方文档
2. 在微信开发者社区提问
3. 检查基础库更新日志
4. 联系微信小程序技术支持

记住：大部分问题都与基础库版本和 Canvas API 兼容性有关，确保使用最新的基础库版本通常能解决大部分问题。