// pages/game/game.js - 测试版本
Page({
  data: {
    message: '游戏加载中...'
  },

  onLoad() {
    console.log('游戏页面加载成功');
    this.setData({
      message: '游戏页面加载成功！'
    });
  },

  onReady() {
    console.log('游戏页面渲染完成');
  }
});