// 太空射击小游戏主入口文件
// 基于微信小游戏API的Canvas游戏

// 游戏配置
const gameConfig = {
    canvasWidth: 375,
    canvasHeight: 667,
    backgroundColor: '#000428',
    
    // 玩家设置
    player: {
        width: 40,
        height: 40,
        speed: 5,
        fireRate: 200, // 射击间隔(ms)
        color: '#00ff00'
    },
    
    // 敌人设置
    enemy: {
        width: 30,
        height: 30,
        speed: 2,
        spawnRate: 1000, // 生成间隔(ms)
        color: '#ff0000'
    },
    
    // 子弹设置
    bullet: {
        width: 4,
        height: 10,
        speed: 8,
        color: '#ffff00'
    }
};

// 游戏状态
let gameState = {
    isRunning: false,
    isPaused: false,
    score: 0,
    highScore: 0,
    level: 1,
    lives: 3
};

// 游戏对象数组
let player = null;
let bullets = [];
let enemies = [];
let particles = [];

// 时间控制
let lastTime = 0;
let lastEnemySpawn = 0;
let lastPlayerFire = 0;

// Canvas和上下文
let canvas = null;
let ctx = null;

// 触控状态
let touchState = {
    isMoving: false,
    isShooting: false,
    moveX: 0,
    moveY: 0
};

// 游戏初始化
function initGame() {
    console.log('🚀 初始化太空射击小游戏...');
    
    // 获取Canvas
    canvas = wx.createCanvas();
    ctx = canvas.getContext('2d');
    
    // 设置Canvas尺寸
    canvas.width = gameConfig.canvasWidth;
    canvas.height = gameConfig.canvasHeight;
    
    // 初始化玩家
    player = {
        x: gameConfig.canvasWidth / 2 - gameConfig.player.width / 2,
        y: gameConfig.canvasHeight - gameConfig.player.height - 50,
        width: gameConfig.player.width,
        height: gameConfig.player.height,
        speed: gameConfig.player.speed
    };
    
    // 加载最高分
    loadHighScore();
    
    // 绑定触控事件
    bindTouchEvents();
    
    // 开始游戏循环
    gameState.isRunning = true;
    gameLoop();
    
    console.log('✅ 游戏初始化完成');
}

// 绑定触控事件
function bindTouchEvents() {
    // 触摸开始
    wx.onTouchStart((e) => {
        if (!gameState.isRunning || gameState.isPaused) return;
        
        const touch = e.touches[0];
        const x = touch.clientX;
        const y = touch.clientY;
        
        // 判断是移动还是射击
        if (y > gameConfig.canvasHeight * 0.7) {
            // 下半部分 - 移动控制
            touchState.isMoving = true;
            touchState.moveX = x;
            touchState.moveY = y;
        } else {
            // 上半部分 - 射击控制
            touchState.isShooting = true;
        }
    });
    
    // 触摸移动
    wx.onTouchMove((e) => {
        if (!gameState.isRunning || gameState.isPaused) return;
        
        const touch = e.touches[0];
        const x = touch.clientX;
        const y = touch.clientY;
        
        if (touchState.isMoving) {
            touchState.moveX = x;
            touchState.moveY = y;
        }
    });
    
    // 触摸结束
    wx.onTouchEnd(() => {
        touchState.isMoving = false;
        touchState.isShooting = false;
    });
}

// 更新玩家位置
function updatePlayer(deltaTime) {
    if (!player) return;
    
    // 触控移动
    if (touchState.isMoving) {
        const targetX = touchState.moveX - player.width / 2;
        const targetY = touchState.moveY - player.height / 2;
        
        // 平滑移动
        const dx = targetX - player.x;
        const dy = targetY - player.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance > 5) {
            player.x += (dx / distance) * player.speed;
            player.y += (dy / distance) * player.speed;
        }
    }
    
    // 边界检测
    player.x = Math.max(0, Math.min(gameConfig.canvasWidth - player.width, player.x));
    player.y = Math.max(0, Math.min(gameConfig.canvasHeight - player.height, player.y));
    
    // 自动射击
    if (touchState.isShooting && Date.now() - lastPlayerFire > gameConfig.player.fireRate) {
        createBullet(player.x + player.width / 2, player.y);
        lastPlayerFire = Date.now();
    }
}

// 创建子弹
function createBullet(x, y) {
    bullets.push({
        x: x - gameConfig.bullet.width / 2,
        y: y,
        width: gameConfig.bullet.width,
        height: gameConfig.bullet.height,
        speed: gameConfig.bullet.speed
    });
}

// 更新子弹
function updateBullets(deltaTime) {
    for (let i = bullets.length - 1; i >= 0; i--) {
        const bullet = bullets[i];
        bullet.y -= bullet.speed;
        
        // 移除超出屏幕的子弹
        if (bullet.y + bullet.height < 0) {
            bullets.splice(i, 1);
        }
    }
}

// 生成敌人
function spawnEnemy() {
    if (Date.now() - lastEnemySpawn < gameConfig.enemy.spawnRate) return;
    
    enemies.push({
        x: Math.random() * (gameConfig.canvasWidth - gameConfig.enemy.width),
        y: -gameConfig.enemy.height,
        width: gameConfig.enemy.width,
        height: gameConfig.enemy.height,
        speed: gameConfig.enemy.speed + Math.random() * 2
    });
    
    lastEnemySpawn = Date.now();
}

// 更新敌人
function updateEnemies(deltaTime) {
    for (let i = enemies.length - 1; i >= 0; i--) {
        const enemy = enemies[i];
        enemy.y += enemy.speed;
        
        // 移除超出屏幕的敌人
        if (enemy.y > gameConfig.canvasHeight) {
            enemies.splice(i, 1);
        }
    }
}

// 碰撞检测
function checkCollisions() {
    // 子弹与敌人碰撞
    for (let i = bullets.length - 1; i >= 0; i--) {
        const bullet = bullets[i];
        
        for (let j = enemies.length - 1; j >= 0; j--) {
            const enemy = enemies[j];
            
            if (isColliding(bullet, enemy)) {
                // 创建爆炸效果
                createExplosion(enemy.x + enemy.width / 2, enemy.y + enemy.height / 2);
                
                // 移除子弹和敌人
                bullets.splice(i, 1);
                enemies.splice(j, 1);
                
                // 增加分数
                gameState.score += 10;
                break;
            }
        }
    }
    
    // 玩家与敌人碰撞
    for (let i = enemies.length - 1; i >= 0; i--) {
        const enemy = enemies[i];
        
        if (isColliding(player, enemy)) {
            // 创建爆炸效果
            createExplosion(player.x + player.width / 2, player.y + player.height / 2);
            
            // 移除敌人
            enemies.splice(i, 1);
            
            // 减少生命
            gameState.lives--;
            
            if (gameState.lives <= 0) {
                gameOver();
            }
            break;
        }
    }
}

// 碰撞检测函数
function isColliding(rect1, rect2) {
    return rect1.x < rect2.x + rect2.width &&
           rect1.x + rect1.width > rect2.x &&
           rect1.y < rect2.y + rect2.height &&
           rect1.y + rect1.height > rect2.y;
}

// 创建爆炸效果
function createExplosion(x, y) {
    for (let i = 0; i < 8; i++) {
        particles.push({
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 10,
            vy: (Math.random() - 0.5) * 10,
            life: 30,
            maxLife: 30,
            color: `hsl(${Math.random() * 60 + 15}, 100%, 50%)`
        });
    }
}

// 更新粒子效果
function updateParticles(deltaTime) {
    for (let i = particles.length - 1; i >= 0; i--) {
        const particle = particles[i];
        
        particle.x += particle.vx;
        particle.y += particle.vy;
        particle.life--;
        
        if (particle.life <= 0) {
            particles.splice(i, 1);
        }
    }
}

// 渲染游戏
function render() {
    // 清空画布
    ctx.fillStyle = gameConfig.backgroundColor;
    ctx.fillRect(0, 0, gameConfig.canvasWidth, gameConfig.canvasHeight);
    
    // 绘制星空背景
    drawStarfield();
    
    // 绘制玩家
    if (player) {
        ctx.fillStyle = gameConfig.player.color;
        ctx.fillRect(player.x, player.y, player.width, player.height);
    }
    
    // 绘制子弹
    ctx.fillStyle = gameConfig.bullet.color;
    bullets.forEach(bullet => {
        ctx.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);
    });
    
    // 绘制敌人
    ctx.fillStyle = gameConfig.enemy.color;
    enemies.forEach(enemy => {
        ctx.fillRect(enemy.x, enemy.y, enemy.width, enemy.height);
    });
    
    // 绘制粒子效果
    particles.forEach(particle => {
        const alpha = particle.life / particle.maxLife;
        ctx.fillStyle = particle.color.replace(')', `, ${alpha})`).replace('hsl', 'hsla');
        ctx.fillRect(particle.x - 2, particle.y - 2, 4, 4);
    });
    
    // 绘制UI
    drawUI();
}

// 绘制星空背景
function drawStarfield() {
    ctx.fillStyle = '#ffffff';
    for (let i = 0; i < 50; i++) {
        const x = (i * 37) % gameConfig.canvasWidth;
        const y = (i * 73 + Date.now() * 0.1) % gameConfig.canvasHeight;
        const size = Math.sin(i) * 2 + 1;
        ctx.fillRect(x, y, size, size);
    }
}

// 绘制UI
function drawUI() {
    ctx.fillStyle = '#ffffff';
    ctx.font = '20px Arial';
    
    // 分数
    ctx.fillText(`分数: ${gameState.score}`, 10, 30);
    
    // 最高分
    ctx.fillText(`最高分: ${gameState.highScore}`, 10, 60);
    
    // 生命值
    ctx.fillText(`生命: ${gameState.lives}`, 10, 90);
    
    // 等级
    ctx.fillText(`等级: ${gameState.level}`, 10, 120);
}

// 游戏循环
function gameLoop() {
    if (!gameState.isRunning) return;
    
    const currentTime = Date.now();
    const deltaTime = currentTime - lastTime;
    lastTime = currentTime;
    
    // 更新游戏逻辑
    updatePlayer(deltaTime);
    updateBullets(deltaTime);
    updateEnemies(deltaTime);
    updateParticles(deltaTime);
    
    // 生成敌人
    spawnEnemy();
    
    // 碰撞检测
    checkCollisions();
    
    // 渲染
    render();
    
    // 继续循环
    requestAnimationFrame(gameLoop);
}

// 游戏结束
function gameOver() {
    gameState.isRunning = false;
    
    // 更新最高分
    if (gameState.score > gameState.highScore) {
        gameState.highScore = gameState.score;
        saveHighScore();
    }
    
    // 显示游戏结束界面
    showGameOverScreen();
}

// 显示游戏结束界面
function showGameOverScreen() {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
    ctx.fillRect(0, 0, gameConfig.canvasWidth, gameConfig.canvasHeight);
    
    ctx.fillStyle = '#ffffff';
    ctx.font = '30px Arial';
    ctx.textAlign = 'center';
    
    ctx.fillText('游戏结束', gameConfig.canvasWidth / 2, gameConfig.canvasHeight / 2 - 50);
    ctx.fillText(`最终分数: ${gameState.score}`, gameConfig.canvasWidth / 2, gameConfig.canvasHeight / 2);
    ctx.fillText(`最高分: ${gameState.highScore}`, gameConfig.canvasWidth / 2, gameConfig.canvasHeight / 2 + 50);
    ctx.fillText('点击屏幕重新开始', gameConfig.canvasWidth / 2, gameConfig.canvasHeight / 2 + 100);
    
    ctx.textAlign = 'left';
    
    // 绑定重新开始事件
    wx.onTouchStart(restartGame);
}

// 重新开始游戏
function restartGame() {
    // 重置游戏状态
    gameState.score = 0;
    gameState.lives = 3;
    gameState.level = 1;
    
    // 清空游戏对象
    bullets = [];
    enemies = [];
    particles = [];
    
    // 重置玩家位置
    player.x = gameConfig.canvasWidth / 2 - gameConfig.player.width / 2;
    player.y = gameConfig.canvasHeight - gameConfig.player.height - 50;
    
    // 重新开始游戏
    gameState.isRunning = true;
    lastTime = Date.now();
    gameLoop();
}

// 保存最高分
function saveHighScore() {
    wx.setStorageSync('highScore', gameState.highScore);
}

// 加载最高分
function loadHighScore() {
    try {
        gameState.highScore = wx.getStorageSync('highScore') || 0;
    } catch (e) {
        gameState.highScore = 0;
    }
}

// 小游戏启动
wx.onShow(() => {
    console.log('🎮 太空射击小游戏启动');
    initGame();
});

// 小游戏隐藏
wx.onHide(() => {
    console.log('⏸️ 太空射击小游戏暂停');
    gameState.isPaused = true;
});

// 导出游戏对象（用于调试）
if (typeof module !== 'undefined') {
    module.exports = {
        gameConfig,
        gameState,
        initGame,
        restartGame
    };
}