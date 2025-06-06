"""
主程序入口
"""
import os
import argparse
import logging
from image_scraper import ImageScraper
from wechat_uploader import WeChatUploader
from config import *

def setup_logging():
    """设置全局日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='图片下载和微信公众号上传工具')
    parser.add_argument('--download', action='store_true', help='下载图片')
    parser.add_argument('--upload', action='store_true', help='上传到微信公众号')
    parser.add_argument('--category', type=str, help='指定分类代码 (如: xgmn)')
    parser.add_argument('--all', action='store_true', help='处理所有分类')
    parser.add_argument('--check-config', action='store_true', help='检查配置')
    
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # 检查配置
    if args.check_config:
        check_configuration()
        return
        
    # 如果没有指定任何操作，默认执行下载和上传
    if not args.download and not args.upload:
        args.download = True
        args.upload = True
        
    # 创建下载目录
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # 下载图片
    if args.download:
        logger.info("开始下载图片...")
        scraper = ImageScraper()
        
        if args.category:
            if args.category in CATEGORIES:
                category_name = CATEGORIES[args.category]
                scraper.scrape_category(args.category, category_name)
            else:
                logger.error(f"未知的分类代码: {args.category}")
                logger.info(f"可用的分类代码: {list(CATEGORIES.keys())}")
                return
        else:
            scraper.scrape_all_categories()
            
    # 上传到微信公众号
    if args.upload:
        logger.info("开始上传到微信公众号...")
        uploader = WeChatUploader()
        
        # 检查微信配置
        if not WECHAT_APPID or not WECHAT_SECRET:
            logger.error("微信公众号配置不完整，请检查 .env 文件")
            logger.info("请参考 .env.example 文件配置微信公众号信息")
            return
            
        # 获取素材统计
        material_count = uploader.get_material_count()
        if material_count:
            logger.info(f"当前素材库统计: 图片 {material_count.get('image_count', 0)} 张")
            
        # 上传图片
        if args.category:
            if args.category in CATEGORIES:
                category_name = CATEGORIES[args.category]
                category_dir = os.path.join(DOWNLOAD_DIR, category_name)
                uploaded = uploader.upload_images_from_directory(category_dir)
                uploader.save_upload_log(uploaded, f"upload_log_{args.category}.json")
            else:
                logger.error(f"未知的分类代码: {args.category}")
                return
        else:
            uploaded = uploader.upload_all_categories()
            uploader.save_upload_log(uploaded, "upload_log_all.json")
            
        logger.info(f"上传完成，共上传 {len(uploaded)} 张图片")

def check_configuration():
    """检查配置"""
    logger = logging.getLogger(__name__)
    
    logger.info("=== 配置检查 ===")
    logger.info(f"基础URL: {BASE_URL}")
    logger.info(f"下载目录: {DOWNLOAD_DIR}")
    logger.info(f"最大工作线程: {MAX_WORKERS}")
    logger.info(f"请求间隔: {DELAY_BETWEEN_REQUESTS}秒")
    logger.info(f"每分类最大图片数: {MAX_IMAGES_PER_CATEGORY}")
    
    logger.info("\n=== 分类配置 ===")
    for code, name in CATEGORIES.items():
        logger.info(f"{code}: {name}")
        
    logger.info("\n=== 微信公众号配置 ===")
    if WECHAT_APPID:
        logger.info(f"AppID: {WECHAT_APPID[:8]}...")
    else:
        logger.warning("AppID: 未配置")
        
    if WECHAT_SECRET:
        logger.info(f"Secret: {WECHAT_SECRET[:8]}...")
    else:
        logger.warning("Secret: 未配置")
        
    # 测试微信API连接
    if WECHAT_APPID and WECHAT_SECRET:
        uploader = WeChatUploader()
        token = uploader.get_access_token()
        if token:
            logger.info("✓ 微信API连接正常")
            material_count = uploader.get_material_count()
            if material_count:
                logger.info(f"素材库统计: {material_count}")
        else:
            logger.error("✗ 微信API连接失败")
    else:
        logger.warning("跳过微信API测试（配置不完整）")

if __name__ == "__main__":
    main()