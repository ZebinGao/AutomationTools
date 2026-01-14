import os

class Config:
    # Flask 配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-testing'
    
    # WinAppDriver 配置
    WINAPPDRIVER_URL = os.environ.get('WINAPPDRIVER_URL') or 'http://127.0.0.1:4723'
    
    # 截图配置
    SCREENSHOT_QUALITY = int(os.environ.get('SCREENSHOT_QUALITY') or '80')  # JPEG 质量 0-100
    
    # 会话超时配置（秒）
    SESSION_TIMEOUT = int(os.environ.get('SESSION_TIMEOUT') or '3600')
