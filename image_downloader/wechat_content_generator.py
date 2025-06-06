#!/usr/bin/env python3
"""
微信公众号内容自动化准备系统
自动生成文章内容、处理图片、格式化文本，为发布做好准备
"""
import os
import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests
from PIL import Image, ImageDraw, ImageFont
import logging

class WeChatContentGenerator:
    """微信公众号内容自动化生成器"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.content_templates = self._load_content_templates()
        self.image_styles = self._load_image_styles()
        
    def _setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def _load_content_templates(self) -> Dict[str, Any]:
        """加载内容模板"""
        return {
            "美女图片": {
                "title_templates": [
                    "今日精选：{count}张高清美女壁纸分享",
                    "每日美图推荐：{theme}系列壁纸合集",
                    "高颜值壁纸来袭：{count}张{theme}美图",
                    "壁纸控必收：{theme}风格美女图片精选",
                    "今日份美好：{count}张治愈系美女壁纸"
                ],
                "intro_templates": [
                    "又到了每日壁纸分享时间！今天为大家带来{count}张精美的{theme}壁纸，每一张都经过精心挑选，高清无水印，适合做手机和电脑壁纸。",
                    "Hello大家好！今天的壁纸分享来啦～这次为大家准备了{theme}系列的美图，共{count}张，画质超清，颜值超高！",
                    "壁纸控们看过来！今日精选{count}张{theme}美女壁纸，每一张都是高清大图，保存即可使用，快来挑选你喜欢的吧！"
                ],
                "outro_templates": [
                    "以上就是今天的壁纸分享，喜欢的话记得点赞收藏哦！明天还会有更多精美壁纸等着大家～",
                    "今天的分享就到这里啦！如果你喜欢这些壁纸，别忘了给小编点个赞👍 明天见！",
                    "壁纸已经准备好了，快去设置成你的专属壁纸吧！记得关注我们，每天都有新的美图分享哦～"
                ]
            },
            "风景图片": {
                "title_templates": [
                    "治愈系风景壁纸：{count}张{theme}美景分享",
                    "大自然的馈赠：{theme}风光摄影作品集",
                    "今日风景推荐：{count}张{theme}高清壁纸"
                ],
                "intro_templates": [
                    "大自然总是能给我们带来无限的治愈力量。今天分享{count}张{theme}风景壁纸，让美景陪伴你的每一天。",
                    "忙碌的生活中，让我们停下来欣赏一下大自然的美好。{count}张{theme}风景图片，带你领略不一样的美景。"
                ]
            }
        }
    
    def _load_image_styles(self) -> Dict[str, Any]:
        """加载图片样式配置"""
        return {
            "thumbnail": {
                "size": (400, 300),
                "quality": 85,
                "format": "JPEG"
            },
            "cover": {
                "size": (900, 500),
                "quality": 90,
                "format": "JPEG"
            },
            "watermark": {
                "text": "壁纸分享",
                "position": "bottom_right",
                "opacity": 0.7,
                "font_size": 24
            }
        }
    
    def generate_article_content(self, 
                               category: str,
                               image_count: int,
                               theme: str = "精选",
                               custom_intro: str = None) -> Dict[str, Any]:
        """生成文章内容"""
        self.logger.info(f"开始生成文章内容：{category} - {theme} - {image_count}张")
        
        templates = self.content_templates.get(category, self.content_templates["美女图片"])
        
        # 生成标题
        title_template = random.choice(templates["title_templates"])
        title = title_template.format(count=image_count, theme=theme)
        
        # 生成开头
        if custom_intro:
            intro = custom_intro
        else:
            intro_template = random.choice(templates["intro_templates"])
            intro = intro_template.format(count=image_count, theme=theme)
        
        # 生成结尾
        outro_template = random.choice(templates.get("outro_templates", ["感谢大家的支持！"]))
        outro = outro_template.format(count=image_count, theme=theme)
        
        # 生成发布时间建议
        publish_time = self._suggest_publish_time()
        
        content = {
            "title": title,
            "intro": intro,
            "outro": outro,
            "category": category,
            "theme": theme,
            "image_count": image_count,
            "publish_time": publish_time,
            "tags": self._generate_tags(category, theme),
            "generated_at": datetime.now().isoformat()
        }
        
        self.logger.info(f"文章内容生成完成：{title}")
        return content
    
    def _suggest_publish_time(self) -> str:
        """建议发布时间"""
        now = datetime.now()
        
        # 建议的发布时间段
        good_hours = [8, 12, 18, 20, 21]  # 早上8点、中午12点、晚上6-9点
        
        # 找到下一个合适的时间
        for hour in good_hours:
            suggested_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if suggested_time > now:
                return suggested_time.strftime("%Y-%m-%d %H:%M")
        
        # 如果今天没有合适时间，建议明天早上8点
        tomorrow = now + timedelta(days=1)
        suggested_time = tomorrow.replace(hour=8, minute=0, second=0, microsecond=0)
        return suggested_time.strftime("%Y-%m-%d %H:%M")
    
    def _generate_tags(self, category: str, theme: str) -> List[str]:
        """生成标签"""
        base_tags = ["壁纸", "高清", "分享"]
        
        if "美女" in category:
            base_tags.extend(["美女", "写真", "颜值"])
        elif "风景" in category:
            base_tags.extend(["风景", "自然", "治愈"])
        
        if theme != "精选":
            base_tags.append(theme)
        
        return base_tags
    
    def prepare_images_for_upload(self, 
                                image_dir: str,
                                output_dir: str = "wechat_ready",
                                add_watermark: bool = True,
                                create_thumbnails: bool = True) -> List[Dict[str, Any]]:
        """准备图片用于上传"""
        self.logger.info(f"开始准备图片：{image_dir}")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        processed_images = []
        image_files = [f for f in os.listdir(image_dir) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        for i, image_file in enumerate(image_files, 1):
            try:
                image_path = os.path.join(image_dir, image_file)
                image_info = self._process_single_image(
                    image_path, output_dir, i, 
                    add_watermark, create_thumbnails
                )
                processed_images.append(image_info)
                
            except Exception as e:
                self.logger.error(f"处理图片失败 {image_file}: {e}")
        
        self.logger.info(f"图片准备完成，共处理 {len(processed_images)} 张")
        return processed_images
    
    def _process_single_image(self, 
                            image_path: str,
                            output_dir: str,
                            index: int,
                            add_watermark: bool,
                            create_thumbnails: bool) -> Dict[str, Any]:
        """处理单张图片"""
        image = Image.open(image_path)
        base_name = f"image_{index:03d}"
        
        image_info = {
            "index": index,
            "original_path": image_path,
            "original_size": image.size,
            "processed_files": {}
        }
        
        # 创建主图（添加水印）
        main_image = image.copy()
        if add_watermark:
            main_image = self._add_watermark(main_image)
        
        main_path = os.path.join(output_dir, f"{base_name}_main.jpg")
        main_image.save(main_path, "JPEG", quality=90)
        image_info["processed_files"]["main"] = main_path
        
        # 创建缩略图
        if create_thumbnails:
            thumbnail = image.copy()
            thumbnail.thumbnail(self.image_styles["thumbnail"]["size"], Image.Resampling.LANCZOS)
            
            thumb_path = os.path.join(output_dir, f"{base_name}_thumb.jpg")
            thumbnail.save(thumb_path, "JPEG", quality=85)
            image_info["processed_files"]["thumbnail"] = thumb_path
        
        # 创建封面图（如果是第一张）
        if index == 1:
            cover = image.copy()
            cover_size = self.image_styles["cover"]["size"]
            
            # 计算裁剪区域（居中裁剪）
            img_width, img_height = cover.size
            target_width, target_height = cover_size
            
            # 计算缩放比例
            scale = max(target_width / img_width, target_height / img_height)
            new_width = int(img_width * scale)
            new_height = int(img_height * scale)
            
            # 缩放图片
            cover = cover.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 居中裁剪
            left = (new_width - target_width) // 2
            top = (new_height - target_height) // 2
            cover = cover.crop((left, top, left + target_width, top + target_height))
            
            cover_path = os.path.join(output_dir, f"{base_name}_cover.jpg")
            cover.save(cover_path, "JPEG", quality=90)
            image_info["processed_files"]["cover"] = cover_path
        
        return image_info
    
    def _add_watermark(self, image: Image.Image) -> Image.Image:
        """添加水印"""
        try:
            # 创建水印图层
            watermark_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark_layer)
            
            # 水印文字
            watermark_text = self.image_styles["watermark"]["text"]
            font_size = self.image_styles["watermark"]["font_size"]
            
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # 计算文字尺寸
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # 计算位置（右下角）
            margin = 20
            x = image.width - text_width - margin
            y = image.height - text_height - margin
            
            # 绘制半透明背景
            bg_padding = 10
            draw.rectangle([
                x - bg_padding, y - bg_padding,
                x + text_width + bg_padding, y + text_height + bg_padding
            ], fill=(255, 255, 255, 128))
            
            # 绘制文字
            draw.text((x, y), watermark_text, fill=(0, 0, 0, 180), font=font)
            
            # 合成水印
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            watermarked = Image.alpha_composite(image, watermark_layer)
            return watermarked.convert('RGB')
            
        except Exception as e:
            self.logger.warning(f"添加水印失败: {e}")
            return image
    
    def generate_wechat_article_draft(self, 
                                    content: Dict[str, Any],
                                    images: List[Dict[str, Any]],
                                    output_file: str = None) -> str:
        """生成微信文章草稿"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"wechat_article_draft_{timestamp}.md"
        
        # 生成Markdown格式的文章草稿
        draft_content = self._create_markdown_draft(content, images)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(draft_content)
        
        self.logger.info(f"文章草稿已生成：{output_file}")
        return output_file
    
    def _create_markdown_draft(self, content: Dict[str, Any], images: List[Dict[str, Any]]) -> str:
        """创建Markdown格式的草稿"""
        lines = []
        
        # 标题
        lines.append(f"# {content['title']}\n")
        
        # 元信息
        lines.append("## 📋 文章信息\n")
        lines.append(f"- **分类**: {content['category']}")
        lines.append(f"- **主题**: {content['theme']}")
        lines.append(f"- **图片数量**: {content['image_count']}张")
        lines.append(f"- **建议发布时间**: {content['publish_time']}")
        lines.append(f"- **标签**: {', '.join(content['tags'])}")
        lines.append(f"- **生成时间**: {content['generated_at']}\n")
        
        # 开头
        lines.append("## 📝 文章开头\n")
        lines.append(f"{content['intro']}\n")
        
        # 图片展示区域
        lines.append("## 🖼️ 图片展示\n")
        lines.append("*以下为图片插入位置，发布时请替换为实际图片*\n")
        
        for i, img_info in enumerate(images, 1):
            lines.append(f"### 图片 {i}")
            if "main" in img_info["processed_files"]:
                lines.append(f"- **主图路径**: `{img_info['processed_files']['main']}`")
            if "thumbnail" in img_info["processed_files"]:
                lines.append(f"- **缩略图路径**: `{img_info['processed_files']['thumbnail']}`")
            if "cover" in img_info["processed_files"]:
                lines.append(f"- **封面图路径**: `{img_info['processed_files']['cover']}`")
            lines.append(f"- **原始尺寸**: {img_info['original_size'][0]} × {img_info['original_size'][1]}")
            lines.append("")
        
        # 结尾
        lines.append("## 📝 文章结尾\n")
        lines.append(f"{content['outro']}\n")
        
        # 发布提醒
        lines.append("## 📢 发布提醒\n")
        lines.append("1. 将上述图片上传到微信公众平台素材库")
        lines.append("2. 在文章编辑器中插入对应图片")
        lines.append("3. 调整图片排版和文字格式")
        lines.append("4. 设置封面图（使用第一张图片的cover版本）")
        lines.append("5. 添加标签和摘要")
        lines.append(f"6. 定时发布：{content['publish_time']}")
        
        return "\n".join(lines)
    
    def create_publishing_checklist(self, content: Dict[str, Any], images: List[Dict[str, Any]]) -> str:
        """创建发布检查清单"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        checklist_file = f"publishing_checklist_{timestamp}.md"
        
        checklist = [
            "# 📋 微信公众号发布检查清单\n",
            f"**文章标题**: {content['title']}",
            f"**计划发布时间**: {content['publish_time']}\n",
            
            "## ✅ 发布前检查\n",
            "- [ ] 所有图片已上传到素材库",
            "- [ ] 图片质量检查完成",
            "- [ ] 文章标题吸引人且不超过64字符",
            "- [ ] 文章摘要已填写",
            "- [ ] 封面图已设置",
            "- [ ] 标签已添加",
            "- [ ] 文章内容格式检查",
            "- [ ] 错别字检查",
            "- [ ] 图片排版美观",
            "- [ ] 文章结构清晰\n",
            
            "## 📊 素材清单\n",
            f"**图片总数**: {len(images)}张\n"
        ]
        
        for i, img_info in enumerate(images, 1):
            checklist.append(f"### 图片 {i}")
            for file_type, file_path in img_info["processed_files"].items():
                checklist.append(f"- [ ] {file_type}: `{file_path}`")
            checklist.append("")
        
        checklist.extend([
            "## 🚀 发布后操作\n",
            "- [ ] 检查文章显示效果",
            "- [ ] 分享到朋友圈",
            "- [ ] 分享到微信群",
            "- [ ] 数据监控（阅读量、点赞数等）",
            "- [ ] 回复读者评论\n",
            
            f"## 📈 预期数据\n",
            f"- **目标阅读量**: 根据历史数据设定",
            f"- **预期互动**: 点赞、评论、分享",
            f"- **发布时间**: {content['publish_time']} (黄金时段)"
        ])
        
        with open(checklist_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(checklist))
        
        self.logger.info(f"发布检查清单已生成：{checklist_file}")
        return checklist_file

def main():
    """主函数 - 演示完整的内容准备流程"""
    print("🚀 微信公众号内容自动化准备系统")
    print("=" * 60)
    
    generator = WeChatContentGenerator()
    
    # 示例：为下载的美女图片生成内容
    image_dir = "downloads/美女照片"  # 假设这是下载的图片目录
    
    if not os.path.exists(image_dir):
        print(f"⚠️ 图片目录不存在: {image_dir}")
        print("请先使用图片爬虫下载一些图片，或者修改image_dir路径")
        return
    
    # 统计图片数量
    image_files = [f for f in os.listdir(image_dir) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    image_count = len(image_files)
    
    if image_count == 0:
        print(f"⚠️ 目录中没有找到图片文件: {image_dir}")
        return
    
    print(f"📊 找到 {image_count} 张图片")
    
    # 1. 生成文章内容
    print("\n📝 生成文章内容...")
    content = generator.generate_article_content(
        category="美女图片",
        image_count=image_count,
        theme="清新"
    )
    
    print(f"✅ 文章标题: {content['title']}")
    print(f"✅ 建议发布时间: {content['publish_time']}")
    
    # 2. 准备图片
    print("\n🖼️ 准备图片...")
    processed_images = generator.prepare_images_for_upload(
        image_dir=image_dir,
        output_dir="wechat_ready",
        add_watermark=True,
        create_thumbnails=True
    )
    
    print(f"✅ 图片处理完成，共 {len(processed_images)} 张")
    
    # 3. 生成文章草稿
    print("\n📄 生成文章草稿...")
    draft_file = generator.generate_wechat_article_draft(content, processed_images)
    print(f"✅ 草稿文件: {draft_file}")
    
    # 4. 生成发布检查清单
    print("\n📋 生成发布检查清单...")
    checklist_file = generator.create_publishing_checklist(content, processed_images)
    print(f"✅ 检查清单: {checklist_file}")
    
    print("\n" + "=" * 60)
    print("🎉 内容准备完成！")
    print("\n📁 生成的文件:")
    print(f"   • {draft_file} - 文章草稿")
    print(f"   • {checklist_file} - 发布检查清单")
    print(f"   • wechat_ready/ - 处理后的图片")
    print("\n📋 下一步操作:")
    print("   1. 查看生成的文章草稿")
    print("   2. 将图片上传到微信公众平台素材库")
    print("   3. 在公众平台编辑器中组装文章")
    print("   4. 按照检查清单完成发布前检查")
    print("   5. 定时发布文章")

if __name__ == "__main__":
    main()