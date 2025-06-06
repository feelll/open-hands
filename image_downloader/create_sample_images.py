"""
创建示例图片用于演示
"""
import os
from PIL import Image, ImageDraw, ImageFont
from config import CATEGORIES, DOWNLOAD_DIR

def create_sample_image(text, size=(800, 600), color='lightblue'):
    """创建示例图片"""
    img = Image.new('RGB', size, color=color)
    draw = ImageDraw.Draw(img)
    
    # 尝试使用默认字体
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    # 计算文本位置
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # 绘制文本
    draw.text((x, y), text, fill='black', font=font)
    
    return img

def create_sample_images():
    """为每个分类创建示例图片"""
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink', 'lightgray', 'lightcyan', 'lavender']
    
    for i, (category_code, category_name) in enumerate(CATEGORIES.items()):
        category_dir = os.path.join(DOWNLOAD_DIR, category_name)
        os.makedirs(category_dir, exist_ok=True)
        
        color = colors[i % len(colors)]
        
        # 为每个分类创建3张示例图片
        for j in range(3):
            text = f"{category_name}\n示例图片 {j+1}"
            img = create_sample_image(text, color=color)
            
            filename = f"sample_{category_code}_{j+1:02d}.jpg"
            filepath = os.path.join(category_dir, filename)
            
            img.save(filepath, 'JPEG', quality=85)
            print(f"创建示例图片: {filepath}")

if __name__ == "__main__":
    print("正在创建示例图片...")
    create_sample_images()
    print("示例图片创建完成！")