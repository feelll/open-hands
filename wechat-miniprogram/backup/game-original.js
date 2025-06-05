// pages/game/game.js
Page({
  data: {
    score: 0,
    lives: 3,
    level: 1,
    highScore: 0,
    gameOver: false,
    paused: false
  },

  onLoad() {
    // 获取历史最高分
    const highScore = wx.getStorageSync('highScore') || 0;
    this.setData({ highScore });
    
    // 初始化游戏
    this.initGame();
  },

  onReady() {
    // 页面渲染完成后初始化Canvas
    this.initCanvas();
  },

  onUnload() {
    // 页面卸载时清理资源
    this.cleanup();
  },

  initCanvas() {
    const query = wx.createSelectorQuery();
    query.select('#gameCanvas')
      .fields({ node: true, size: true })
      .exec((res) => {
        try {
          const canvas = res[0].node;
          const ctx = canvas.getContext('2d');
          
          // 设置画布尺寸
          const dpr = wx.getSystemInfoSync().pixelRatio;
          canvas.width = res[0].width * dpr;
          canvas.height = res[0].height * dpr;
          ctx.scale(dpr, dpr);
          
          this.canvas = canvas;
          this.ctx = ctx;
          this.canvasWidth = res[0].width;
          this.canvasHeight = res[0].height;
          
          // 检查 requestAnimationFrame 是否可用
          if (!this.canvas.requestAnimationFrame) {
            console.warn('Canvas requestAnimationFrame not available, using setTimeout fallback');
            this.canvas.requestAnimationFrame = (callback) => {
              return setTimeout(callback, 1000 / 60); // 60 FPS
            };
          }
          
          // 开始游戏
          this.startGame();
        } catch (error) {
          console.error('Canvas initialization failed:', error);
          wx.showToast({
            title: '游戏初始化失败',
            icon: 'none'
          });
        }
      });
  },

  initGame() {
    // 游戏状态初始化
    this.gameState = {
      score: 0,
      lives: 3,
      level: 1,
      gameRunning: true,
      paused: false,
      lastShot: 0,
      shootCooldown: 200,
      keys: {}
    };

    // 游戏对象数组
    this.player = null;
    this.bullets = [];
    this.enemies = [];
    this.explosions = [];
    this.stars = [];
    
    // 移动状态
    this.moveState = {
      up: false,
      down: false,
      left: false,
      right: false
    };

    this.setData({
      score: 0,
      lives: 3,
      level: 1,
      gameOver: false,
      paused: false
    });
  },

  startGame() {
    if (!this.ctx) return;
    
    // 创建玩家
    this.player = new Player(this.canvasWidth / 2, this.canvasHeight - 80);
    
    // 创建星星背景
    this.stars = [];
    for (let i = 0; i < 50; i++) {
      this.stars.push(new Star(this.canvasWidth, this.canvasHeight));
    }
    
    // 开始游戏循环
    this.gameLoop();
  },

  gameLoop() {
    if (!this.gameState.gameRunning || this.data.paused) {
      if (this.gameState.gameRunning) {
        this.canvas.requestAnimationFrame(() => this.gameLoop());
      }
      return;
    }

    // 清空画布
    this.ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight);

    // 绘制星星背景
    this.stars.forEach(star => {
      star.update();
      star.draw(this.ctx);
    });

    // 更新和绘制玩家
    if (this.player) {
      this.player.update(this.moveState, this.canvasWidth, this.canvasHeight);
      this.player.draw(this.ctx);
    }

    // 生成敌人
    this.spawnEnemies();

    // 更新和绘制敌人
    this.enemies.forEach((enemy, index) => {
      enemy.update();
      enemy.draw(this.ctx);

      if (enemy.isOffScreen(this.canvasHeight)) {
        this.enemies.splice(index, 1);
      }
    });

    // 更新和绘制子弹
    this.bullets.forEach((bullet, index) => {
      bullet.update();
      bullet.draw(this.ctx);

      if (bullet.isOffScreen(this.canvasHeight)) {
        this.bullets.splice(index, 1);
      }
    });

    // 更新和绘制爆炸效果
    this.explosions.forEach((explosion, index) => {
      explosion.update();
      explosion.draw(this.ctx);

      if (explosion.isDead()) {
        this.explosions.splice(index, 1);
      }
    });

    // 检查碰撞
    this.checkCollisions();

    // 更新等级
    if (this.gameState.score > this.gameState.level * 500) {
      this.gameState.level++;
      this.setData({ level: this.gameState.level });
    }

    // 更新UI
    this.setData({
      score: this.gameState.score,
      lives: this.gameState.lives
    });

    this.canvas.requestAnimationFrame(() => this.gameLoop());
  },

  spawnEnemies() {
    if (Math.random() < 0.02 + this.gameState.level * 0.005) {
      let enemyType = 'basic';
      let rand = Math.random();
      
      if (rand < 0.1) {
        enemyType = 'tank';
      } else if (rand < 0.3) {
        enemyType = 'fast';
      }
      
      this.enemies.push(new Enemy(Math.random() * (this.canvasWidth - 40), -40, enemyType));
    }
  },

  checkCollisions() {
    // 玩家子弹与敌人碰撞
    this.bullets.forEach((bullet, bulletIndex) => {
      if (bullet.isPlayerBullet) {
        this.enemies.forEach((enemy, enemyIndex) => {
          if (this.isColliding(bullet, enemy)) {
            this.bullets.splice(bulletIndex, 1);
            enemy.health--;
            
            if (enemy.health <= 0) {
              this.explosions.push(new Explosion(enemy.x + enemy.width/2, enemy.y + enemy.height/2));
              this.gameState.score += enemy.points;
              this.enemies.splice(enemyIndex, 1);
            }
          }
        });
      }
    });

    // 敌人子弹与玩家碰撞
    this.bullets.forEach((bullet, bulletIndex) => {
      if (!bullet.isPlayerBullet && this.player) {
        if (this.isColliding(bullet, this.player)) {
          this.bullets.splice(bulletIndex, 1);
          this.gameState.lives--;
          this.explosions.push(new Explosion(this.player.x + this.player.width/2, this.player.y + this.player.height/2));
          
          if (this.gameState.lives <= 0) {
            this.gameOver();
          }
        }
      }
    });

    // 敌人与玩家碰撞
    this.enemies.forEach((enemy, enemyIndex) => {
      if (this.player && this.isColliding(enemy, this.player)) {
        this.explosions.push(new Explosion(enemy.x + enemy.width/2, enemy.y + enemy.height/2));
        this.enemies.splice(enemyIndex, 1);
        this.gameState.lives--;
        
        if (this.gameState.lives <= 0) {
          this.gameOver();
        }
      }
    });
  },

  isColliding(obj1, obj2) {
    return obj1.x < obj2.x + obj2.width &&
           obj1.x + obj1.width > obj2.x &&
           obj1.y < obj2.y + obj2.height &&
           obj1.y + obj1.height > obj2.y;
  },

  gameOver() {
    this.gameState.gameRunning = false;
    
    // 更新最高分
    if (this.gameState.score > this.data.highScore) {
      wx.setStorageSync('highScore', this.gameState.score);
      this.setData({ highScore: this.gameState.score });
    }
    
    this.setData({ gameOver: true });
  },

  // 触控事件处理
  onMoveStart(e) {
    const direction = e.currentTarget.dataset.direction;
    this.moveState[direction] = true;
  },

  onMoveEnd(e) {
    const direction = e.currentTarget.dataset.direction;
    this.moveState[direction] = false;
  },

  onShoot() {
    if (this.player && Date.now() - this.gameState.lastShot > this.gameState.shootCooldown) {
      this.bullets.push(new Bullet(
        this.player.x + this.player.width/2 - 2, 
        this.player.y, 
        -8, 
        '#00ffff', 
        true
      ));
      this.gameState.lastShot = Date.now();
    }
  },

  // 触摸屏幕移动
  onTouchStart(e) {
    this.touchStartX = e.touches[0].x;
    this.touchStartY = e.touches[0].y;
  },

  onTouchMove(e) {
    if (!this.player) return;
    
    const deltaX = e.touches[0].x - this.touchStartX;
    const deltaY = e.touches[0].y - this.touchStartY;
    
    this.player.x = Math.max(0, Math.min(this.canvasWidth - this.player.width, this.player.x + deltaX * 0.5));
    this.player.y = Math.max(0, Math.min(this.canvasHeight - this.player.height, this.player.y + deltaY * 0.5));
    
    this.touchStartX = e.touches[0].x;
    this.touchStartY = e.touches[0].y;
  },

  onTouchEnd() {
    // 触摸结束时自动射击
    this.onShoot();
  },

  togglePause() {
    const paused = !this.data.paused;
    this.setData({ paused });
    
    if (!paused && this.gameState.gameRunning) {
      this.gameLoop();
    }
  },

  restartGame() {
    this.initGame();
    this.startGame();
  },

  shareGame() {
    wx.showShareMenu({
      withShareTicket: true
    });
  },

  cleanup() {
    this.gameState.gameRunning = false;
  }
});

// 游戏类定义
class Player {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.width = 40;
    this.height = 40;
    this.speed = 3;
  }

  update(moveState, canvasWidth, canvasHeight) {
    if (moveState.left) {
      this.x = Math.max(0, this.x - this.speed);
    }
    if (moveState.right) {
      this.x = Math.min(canvasWidth - this.width, this.x + this.speed);
    }
    if (moveState.up) {
      this.y = Math.max(0, this.y - this.speed);
    }
    if (moveState.down) {
      this.y = Math.min(canvasHeight - this.height, this.y + this.speed);
    }
  }

  draw(ctx) {
    ctx.fillStyle = '#00ffff';
    ctx.fillRect(this.x, this.y, this.width, this.height);
    
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(this.x + 5, this.y + 5, this.width - 10, this.height - 10);
    
    ctx.fillStyle = '#ff0000';
    ctx.fillRect(this.x + 15, this.y + 15, 10, 10);
  }
}

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

  draw(ctx) {
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x, this.y, this.width, this.height);
  }

  isOffScreen(canvasHeight) {
    return this.y < -this.height || this.y > canvasHeight;
  }
}

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
  }

  draw(ctx) {
    ctx.fillStyle = this.color;
    ctx.fillRect(this.x, this.y, this.width, this.height);
    
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(this.x + 5, this.y + 5, this.width - 10, this.height - 10);
  }

  isOffScreen(canvasHeight) {
    return this.y > canvasHeight;
  }
}

class Explosion {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.particles = [];
    this.life = 30;
    
    for (let i = 0; i < 8; i++) {
      this.particles.push({
        x: x,
        y: y,
        vx: (Math.random() - 0.5) * 8,
        vy: (Math.random() - 0.5) * 8,
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

  draw(ctx) {
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

class Star {
  constructor(canvasWidth, canvasHeight) {
    this.x = Math.random() * canvasWidth;
    this.y = Math.random() * canvasHeight;
    this.speed = Math.random() * 2 + 0.5;
    this.size = Math.random() * 2 + 1;
    this.opacity = Math.random() * 0.8 + 0.2;
    this.canvasWidth = canvasWidth;
    this.canvasHeight = canvasHeight;
  }

  update() {
    this.y += this.speed;
    if (this.y > this.canvasHeight) {
      this.y = -this.size;
      this.x = Math.random() * this.canvasWidth;
    }
  }

  draw(ctx) {
    ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
    ctx.fillRect(this.x, this.y, this.size, this.size);
  }
}