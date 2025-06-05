// 游戏配置文件
const GAME_CONFIG = {
    // 画布设置
    canvas: {
        width: 800,
        height: 600
    },
    
    // 玩家设置
    player: {
        speed: 5,
        shootCooldown: 200,
        startLives: 3,
        startHealth: 100
    },
    
    // 敌人设置
    enemies: {
        spawnRate: 0.02,
        types: {
            basic: {
                speed: [1, 3],
                health: 1,
                points: 10,
                color: '#ff0000'
            },
            fast: {
                speed: [3, 5],
                health: 1,
                points: 20,
                color: '#ff6600'
            },
            tank: {
                speed: [0.5, 1.5],
                health: 3,
                points: 50,
                color: '#800080'
            }
        }
    },
    
    // 等级设置
    levels: {
        scorePerLevel: 500,
        difficultyIncrease: 0.005
    },
    
    // 视觉效果
    effects: {
        starCount: 100,
        explosionParticles: 10,
        explosionLife: 30
    },
    
    // 颜色主题
    colors: {
        player: '#00ffff',
        playerBullet: '#00ffff',
        enemyBullet: '#ff0000',
        ui: '#00ffff',
        background: ['#000428', '#004e92']
    }
};

// 导出配置（如果在模块环境中）
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GAME_CONFIG;
}