import base64
from io import BytesIO
from PIL import Image
import re

def compress_image(base64_image_data: str, quality: int = 80) -> str:
    """
    压缩 base64 编码的图像数据
    
    :param base64_image_data: Base64 编码的图像数据
    :param quality: JPEG 压缩质量 (0-100)
    :return: 压缩后的 Base64 图像数据
    """
    # 移除数据 URI 前缀（如果存在）
    if base64_image_data.startswith('data:image'):
        # 提取 base64 数据部分
        base64_image_data = re.sub('^data:image/.+;base64,', '', base64_image_data)
    
    # 解码 base64 数据
    image_data = base64.b64decode(base64_image_data)
    
    # 打开图像
    image = Image.open(BytesIO(image_data))
    
    # 转换为 RGB（如果需要）
    if image.mode in ('RGBA', 'LA', 'P'):
        # 创建白色背景
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
        image = background
    
    # 压缩图像
    output_buffer = BytesIO()
    image.save(output_buffer, format='JPEG', quality=quality, optimize=True)
    compressed_image_data = output_buffer.getvalue()
    
    # 返回 base64 编码的压缩图像
    return base64.b64encode(compressed_image_data).decode('utf-8')

def resize_image(base64_image_data: str, max_width: int = 800, max_height: int = 600) -> str:
    """
    调整图像大小以适应指定的最大尺寸
    
    :param base64_image_data: Base64 编码的图像数据
    :param max_width: 最大宽度
    :param max_height: 最大高度
    :return: 调整大小后的 Base64 图像数据
    """
    # 移除数据 URI 前缀（如果存在）
    if base64_image_data.startswith('data:image'):
        base64_image_data = re.sub('^data:image/.+;base64,', '', base64_image_data)
    
    # 解码 base64 数据
    image_data = base64.b64decode(base64_image_data)
    
    # 打开图像
    image = Image.open(BytesIO(image_data))
    
    # 计算新尺寸保持宽高比
    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    
    # 转换为 RGB（如果需要）
    if image.mode in ('RGBA', 'LA', 'P'):
        # 创建白色背景
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
        image = background
    
    # 保存调整大小的图像
    output_buffer = BytesIO()
    image.save(output_buffer, format='JPEG', quality=80, optimize=True)
    resized_image_data = output_buffer.getvalue()
    
    # 返回 base64 编码的调整大小的图像
    return base64.b64encode(resized_image_data).decode('utf-8')
