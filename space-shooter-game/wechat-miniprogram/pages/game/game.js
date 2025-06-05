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
    this.setData({
      message: '页面渲染完成，可以开始测试'
    });
  },

  startTest() {
    console.log('开始测试按钮被点击');
    this.setData({
      message: '测试成功！game.js 文件正常工作'
    });
    
    wx.showToast({
      title: '测试成功！',
      icon: 'success'
    });
  }
});