// 游戏状态
let gameState = {
    score: 0,
    lives: 3,
    level: 1,
    gameRunning: true,
    keys: {},
    lastShot: 0,
    shootCooldown: 200
};

// 获取画布和上下文
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// 游戏对象数组
let player;
let bullets = [];
let enemies = [];
let explosions = [];
let stars = [];
let powerUps = [];

// 玩家类
class Player {
    constructor() {
        this.x = canvas.width / 2;
        this.y = canvas.height - 80;
        this.width = 40;
        this.height = 40;
        this.speed = 5;
        this.health = 100;
    }
    
    update() {
        // 移动控制
        if (gameState.keys['ArrowLeft'] || gameState.keys['a'] || gameState.keys['A']) {
            this.x = Math.max(0, this.x - this.speed);
        }
        if (gameState.keys['ArrowRight'] || gameState.keys['d'] || gameState.keys['D']) {
            this.x = Math.min(canvas.width - this.width, this.x + this.speed);
        }
        if (gameState.keys['ArrowUp'] || gameState.keys['w'] || gameState.keys['W']) {
            this.y = Math.max(0, this.y - this.speed);
        }
        if (gameState.keys['ArrowDown'] || gameState.keys['s'] || gameState.keys['S']) {
            this.y = Math.min(canvas.height - this.height, this.y + this.speed);
        }
        
        // 射击
        if (gameState.keys[' '] && Date.now() - gameState.lastShot > gameState.shootCooldown) {
            this.shoot();
            gameState.lastShot = Date.now();
        }
    }
    
    shoot() {
        bullets.push(new Bullet(this.x + this.width/2 - 2, this.y, -8, '#00ffff', true));
    }
    
    draw() {
        // 绘制玩家飞船
        ctx.fillStyle = '#00ffff';
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        // 绘制飞船细节
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(this.x + 5, this.y + 5, this.width - 10, this.height - 10);
        
        ctx.fillStyle = '#ff0000';
        ctx.fillRect(this.x + 15, this.y + 15, 10, 10);
        
        // 引擎火焰效果
        ctx.fillStyle = '#ff6600';
        ctx.fillRect(this.x + 10, this.y + this.height, 20, 10);
        ctx.fillStyle = '#ffff00';
        ctx.fillRect(this.x + 15, this.y + this.height, 10, 8);
    }
}

// 子弹类
class Bullet {
    constructor(x, y, speed, color, isPlayerBullet = false) {
        this.x = x;
        this.y = y;
        this.width = 4;
        this.height = 10;
        this.speed = speed;
        this.color = color;
        this.isPlayerBullet = isPlayerBullet;
    }
    
    update() {
        this.y += this.speed;
    }
    
    draw() {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        // 添加发光效果
        ctx.shadowColor = this.color;
        ctx.shadowBlur = 10;
        ctx.fillRect(this.x, this.y, this.width, this.height);
        ctx.shadowBlur = 0;
    }
    
    isOffScreen() {
        return this.y < -this.height || this.y > canvas.height;
    }
}

// 敌人类
class Enemy {
    constructor(x, y, type = 'basic') {
        this.x = x;
        this.y = y;
        this.type = type;
        this.lastShot = 0;
        this.shootCooldown = 1000 + Math.random() * 2000;
        
        if (type === 'basic') {
            this.width = 30;
            this.height = 30;
            this.speed = 1 + Math.random() * 2;
            this.health = 1;
            this.color = '#ff0000';
            this.points = 10;
        } else if (type === 'fast') {
            this.width = 25;
            this.height = 25;
            this.speed = 3 + Math.random() * 2;
            this.health = 1;
            this.color = '#ff6600';
            this.points = 20;
        } else if (type === 'tank') {
            this.width = 40;
            this.height = 40;
            this.speed = 0.5 + Math.random();
            this.health = 3;
            this.color = '#800080';
            this.points = 50;
        }
    }
    
    update() {
        this.y += this.speed;
        
        // 敌人射击
        if (Date.now() - this.lastShot > this.shootCooldown) {
            this.shoot();
            this.lastShot = Date.now();
        }
    }
    
    shoot() {
        bullets.push(new Bullet(this.x + this.width/2 - 2, this.y + this.height, 4, '#ff0000', false));
    }
    
    draw() {
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        // 绘制敌人细节
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(this.x + 5, this.y + 5, this.width - 10, this.height - 10);
        
        ctx.fillStyle = '#000000';
        ctx.fillRect(this.x + 10, this.y + 10, this.width - 20, this.height - 20);
    }
    
    isOffScreen() {
        return this.y > canvas.height;
    }
}

// 爆炸效果类
class Explosion {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.particles = [];
        this.life = 30;
        
        // 创建粒子
        for (let i = 0; i < 10; i++) {
            this.particles.push({
                x: x,
                y: y,
                vx: (Math.random() - 0.5) * 10,
                vy: (Math.random() - 0.5) * 10,
                life: 30,
                color: `hsl(${Math.random() * 60 + 10}, 100%, 50%)`
            });
        }
    }
    
    update() {
        this.life--;
        this.particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.life--;
            particle.vx *= 0.98;
            particle.vy *= 0.98;
        });
        
        this.particles = this.particles.filter(particle => particle.life > 0);
    }
    
    draw() {
        this.particles.forEach(particle => {
            ctx.fillStyle = particle.color;
            ctx.globalAlpha = particle.life / 30;
            ctx.fillRect(particle.x, particle.y, 3, 3);
        });
        ctx.globalAlpha = 1;
    }
    
    isDead() {
        return this.life <= 0 && this.particles.length === 0;
    }
}

// 星星背景类
class Star {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.speed = Math.random() * 2 + 0.5;
        this.size = Math.random() * 2 + 1;
        this.opacity = Math.random() * 0.8 + 0.2;
    }
    
    update() {
        this.y += this.speed;
        if (this.y > canvas.height) {
            this.y = -this.size;
            this.x = Math.random() * canvas.width;
        }
    }
    
    draw() {
        ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
        ctx.fillRect(this.x, this.y, this.size, this.size);
    }
}

// 初始化游戏
function initGame() {
    player = new Player();
    bullets = [];
    enemies = [];
    explosions = [];
    powerUps = [];
    
    // 创建星星背景
    stars = [];
    for (let i = 0; i < 100; i++) {
        stars.push(new Star());
    }
    
    gameState.score = 0;
    gameState.lives = 3;
    gameState.level = 1;
    gameState.gameRunning = true;
    
    updateUI();
}

// 生成敌人
function spawnEnemies() {
    if (Math.random() < 0.02 + gameState.level * 0.005) {
        let enemyType = 'basic';
        let rand = Math.random();
        
        if (rand < 0.1) {
            enemyType = 'tank';
        } else if (rand < 0.3) {
            enemyType = 'fast';
        }
        
        enemies.push(new Enemy(Math.random() * (canvas.width - 40), -40, enemyType));
    }
}

// 碰撞检测
function checkCollisions() {
    // 玩家子弹与敌人碰撞
    bullets.forEach((bullet, bulletIndex) => {
        if (bullet.isPlayerBullet) {
            enemies.forEach((enemy, enemyIndex) => {
                if (bullet.x < enemy.x + enemy.width &&
                    bullet.x + bullet.width > enemy.x &&
                    bullet.y < enemy.y + enemy.height &&
                    bullet.y + bullet.height > enemy.y) {
                    
                    // 移除子弹
                    bullets.splice(bulletIndex, 1);
                    
                    // 敌人受伤
                    enemy.health--;
                    if (enemy.health <= 0) {
                        // 敌人死亡
                        explosions.push(new Explosion(enemy.x + enemy.width/2, enemy.y + enemy.height/2));
                        gameState.score += enemy.points;
                        enemies.splice(enemyIndex, 1);
                    }
                }
            });
        }
    });
    
    // 敌人子弹与玩家碰撞
    bullets.forEach((bullet, bulletIndex) => {
        if (!bullet.isPlayerBullet) {
            if (bullet.x < player.x + player.width &&
                bullet.x + bullet.width > player.x &&
                bullet.y < player.y + player.height &&
                bullet.y + bullet.height > player.y) {
                
                bullets.splice(bulletIndex, 1);
                gameState.lives--;
                explosions.push(new Explosion(player.x + player.width/2, player.y + player.height/2));
                
                if (gameState.lives <= 0) {
                    gameOver();
                }
            }
        }
    });
    
    // 敌人与玩家碰撞
    enemies.forEach((enemy, enemyIndex) => {
        if (enemy.x < player.x + player.width &&
            enemy.x + enemy.width > player.x &&
            enemy.y < player.y + player.height &&
            enemy.y + enemy.height > player.y) {
            
            explosions.push(new Explosion(enemy.x + enemy.width/2, enemy.y + enemy.height/2));
            enemies.splice(enemyIndex, 1);
            gameState.lives--;
            
            if (gameState.lives <= 0) {
                gameOver();
            }
        }
    });
}

// 更新UI
function updateUI() {
    document.getElementById('score').textContent = gameState.score;
    document.getElementById('lives').textContent = gameState.lives;
    document.getElementById('level').textContent = gameState.level;
}

// 游戏结束
function gameOver() {
    gameState.gameRunning = false;
    document.getElementById('finalScore').textContent = gameState.score;
    document.getElementById('gameOver').style.display = 'block';
}

// 重新开始游戏
function restartGame() {
    document.getElementById('gameOver').style.display = 'none';
    initGame();
}

// 显示等级提升通知
function showLevelUpNotification() {
    const notification = document.getElementById('powerUpNotification');
    notification.style.display = 'block';
    notification.style.animation = 'none';
    
    // 强制重新触发动画
    setTimeout(() => {
        notification.style.animation = 'fadeInOut 2s ease-in-out';
    }, 10);
    
    // 2秒后隐藏通知
    setTimeout(() => {
        notification.style.display = 'none';
    }, 2000);
}

// 游戏主循环
function gameLoop() {
    if (!gameState.gameRunning) {
        requestAnimationFrame(gameLoop);
        return;
    }
    
    // 清空画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 绘制星星背景
    stars.forEach(star => {
        star.update();
        star.draw();
    });
    
    // 更新和绘制玩家
    player.update();
    player.draw();
    
    // 生成敌人
    spawnEnemies();
    
    // 更新和绘制敌人
    enemies.forEach((enemy, index) => {
        enemy.update();
        enemy.draw();
        
        if (enemy.isOffScreen()) {
            enemies.splice(index, 1);
        }
    });
    
    // 更新和绘制子弹
    bullets.forEach((bullet, index) => {
        bullet.update();
        bullet.draw();
        
        if (bullet.isOffScreen()) {
            bullets.splice(index, 1);
        }
    });
    
    // 更新和绘制爆炸效果
    explosions.forEach((explosion, index) => {
        explosion.update();
        explosion.draw();
        
        if (explosion.isDead()) {
            explosions.splice(index, 1);
        }
    });
    
    // 检查碰撞
    checkCollisions();
    
    // 更新等级
    if (gameState.score > gameState.level * 500) {
        gameState.level++;
        showLevelUpNotification();
    }
    
    // 更新UI
    updateUI();
    
    requestAnimationFrame(gameLoop);
}

// 键盘事件监听
document.addEventListener('keydown', (e) => {
    gameState.keys[e.key] = true;
    e.preventDefault();
});

document.addEventListener('keyup', (e) => {
    gameState.keys[e.key] = false;
    e.preventDefault();
});

// 初始化并开始游戏
initGame();
gameLoop();