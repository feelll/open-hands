#!/usr/bin/env python3
"""
微信公众号内容生成配置文件
"""

# 内容生成配置
CONTENT_CONFIG = {
    # 文章模板配置
    "templates": {
        "美女图片": {
            "keywords": ["美女", "壁纸", "高清", "写真", "颜值"],
            "themes": ["清新", "甜美", "性感", "可爱", "优雅", "时尚", "古风", "日系"],
            "title_formats": [
                "今日精选：{count}张{theme}美女壁纸",
                "高颜值来袭：{theme}系列美图分享",
                "壁纸控必收：{count}张{theme}写真",
                "每日美图：{theme}风格壁纸合集",
                "治愈系美女：{count}张{theme}高清图"
            ]
        },
        "风景图片": {
            "keywords": ["风景", "自然", "治愈", "摄影", "美景"],
            "themes": ["山水", "海景", "森林", "城市", "夕阳", "雪景", "花海", "星空"],
            "title_formats": [
                "大自然的馈赠：{count}张{theme}美景",
                "治愈系风景：{theme}摄影作品集",
                "今日风光：{count}张{theme}高清壁纸"
            ]
        },
        "动漫图片": {
            "keywords": ["动漫", "二次元", "插画", "卡通", "萌"],
            "themes": ["可爱", "萌系", "治愈", "唯美", "热血", "校园", "奇幻", "科幻"],
            "title_formats": [
                "二次元福利：{count}张{theme}动漫壁纸",
                "动漫控必收：{theme}系列插画",
                "今日二次元：{count}张{theme}美图"
            ]
        }
    },
    
    # 发布时间配置
    "publish_schedule": {
        "peak_hours": [8, 12, 18, 20, 21],  # 黄金发布时间
        "avoid_hours": [1, 2, 3, 4, 5, 6],  # 避免发布时间
        "weekend_adjustment": True,  # 周末时间调整
        "holiday_adjustment": True   # 节假日时间调整
    },
    
    # 图片处理配置
    "image_processing": {
        "formats": {
            "main": {
                "max_size": (1080, 1920),  # 主图最大尺寸
                "quality": 90,
                "format": "JPEG"
            },
            "thumbnail": {
                "size": (400, 300),
                "quality": 85,
                "format": "JPEG"
            },
            "cover": {
                "size": (900, 500),  # 封面图尺寸
                "quality": 95,
                "format": "JPEG"
            }
        },
        "watermark": {
            "enabled": True,
            "text": "壁纸分享",
            "font_size": 24,
            "opacity": 0.7,
            "position": "bottom_right",
            "margin": 20
        },
        "auto_enhance": {
            "brightness": 1.05,  # 亮度调整
            "contrast": 1.1,     # 对比度调整
            "saturation": 1.05   # 饱和度调整
        }
    },
    
    # 内容质量控制
    "quality_control": {
        "min_image_count": 5,      # 最少图片数量
        "max_image_count": 20,     # 最多图片数量
        "min_image_size": (800, 600),  # 最小图片尺寸
        "title_max_length": 64,    # 标题最大长度
        "intro_min_length": 50,    # 开头最小长度
        "intro_max_length": 200    # 开头最大长度
    },
    
    # SEO优化配置
    "seo": {
        "keywords_density": 0.02,  # 关键词密度
        "meta_description_length": 120,  # 描述长度
        "tags_count": 5,           # 标签数量
        "internal_links": True     # 内部链接
    }
}

# 内容风格配置
STYLE_CONFIG = {
    "writing_styles": {
        "casual": {
            "tone": "轻松随意",
            "emoji_usage": "适中",
            "sentence_length": "中等",
            "vocabulary": "日常用语"
        },
        "professional": {
            "tone": "专业正式",
            "emoji_usage": "少量",
            "sentence_length": "较长",
            "vocabulary": "专业术语"
        },
        "friendly": {
            "tone": "亲切友好",
            "emoji_usage": "较多",
            "sentence_length": "较短",
            "vocabulary": "亲民用语"
        }
    },
    
    "emoji_sets": {
        "basic": ["😊", "👍", "❤️", "🔥", "✨", "🎉", "📸", "🌟"],
        "image_related": ["🖼️", "📷", "🎨", "🌈", "💫", "✨", "🔆", "🎭"],
        "emotion": ["😍", "🥰", "😘", "💕", "💖", "💝", "🌹", "💐"]
    }
}

# 自动化配置
AUTOMATION_CONFIG = {
    "batch_processing": {
        "enabled": True,
        "max_concurrent": 5,       # 最大并发处理数
        "retry_attempts": 3,       # 重试次数
        "timeout": 30              # 超时时间（秒）
    },
    
    "content_variation": {
        "title_variations": 3,     # 标题变体数量
        "intro_variations": 2,     # 开头变体数量
        "auto_select_best": True   # 自动选择最佳版本
    },
    
    "scheduling": {
        "auto_schedule": True,     # 自动安排发布时间
        "buffer_time": 30,         # 缓冲时间（分钟）
        "avoid_conflicts": True    # 避免时间冲突
    }
}

# 平台特定配置
PLATFORM_CONFIG = {
    "wechat": {
        "title_max_length": 64,
        "content_max_length": 20000,
        "image_max_count": 20,
        "image_max_size": 10 * 1024 * 1024,  # 10MB
        "supported_formats": ["jpg", "jpeg", "png", "gif"],
        "cover_ratio": "16:9"
    },
    
    "weibo": {
        "title_max_length": 140,
        "content_max_length": 2000,
        "image_max_count": 9,
        "hashtag_required": True
    }
}

# 数据分析配置
ANALYTICS_CONFIG = {
    "tracking": {
        "engagement_metrics": True,
        "click_through_rate": True,
        "share_rate": True,
        "comment_sentiment": True
    },
    
    "optimization": {
        "a_b_testing": True,
        "performance_learning": True,
        "auto_adjustment": True
    }
}