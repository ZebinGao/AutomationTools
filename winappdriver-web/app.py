from flask import Flask, request, jsonify, render_template, session
import requests
import os
import uuid
from config import Config
from utils.winappdriver import WinAppDriverClient
from utils.image_utils import compress_image

app = Flask(__name__)
app.config.from_object(Config)

# 存储会话的 WinAppDriver 客户端
driver_sessions = {}

@app.route('/')
def index():
    """主页 - 显示控制界面"""
    return render_template('index.html')

@app.route('/api/session', methods=['POST'])
def create_session():
    """创建新的 WinAppDriver 会话"""
    data = request.get_json()
    app_path = data.get('appPath')
    
    if not app_path:
        return jsonify({'error': 'Missing appPath parameter'}), 400
    
    try:
        # 创建新的会话ID
        session_id = str(uuid.uuid4())
        
        # 初始化 WinAppDriver 客户端
        driver_client = WinAppDriverClient(
            winappdriver_url=app.config['WINAPPDRIVER_URL'],
            app_path=app_path
        )
        
        # 启动应用
        response = driver_client.start_application()
        
        # 存储会话
        driver_sessions[session_id] = driver_client
        
        return jsonify({
            'sessionId': session_id,
            'status': 'success',
            'message': 'Session created successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """删除 WinAppDriver 会话"""
    if session_id in driver_sessions:
        try:
            driver_sessions[session_id].quit()
            del driver_sessions[session_id]
            return jsonify({'status': 'success', 'message': 'Session deleted'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Session not found'}), 404

@app.route('/api/session/<session_id>/screenshot')
def get_screenshot(session_id):
    """获取屏幕截图"""
    if session_id not in driver_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    try:
        # 获取截图
        screenshot_data = driver_sessions[session_id].get_screenshot()
        
        # 压缩图片
        compressed_data = compress_image(screenshot_data, quality=app.config['SCREENSHOT_QUALITY'])
        
        return jsonify({
            'status': 'success',
            'screenshot': compressed_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/<session_id>/source')
def get_source(session_id):
    """获取UI元素源码"""
    if session_id not in driver_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    try:
        source = driver_sessions[session_id].get_page_source()
        return jsonify({
            'status': 'success',
            'source': source
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/<session_id>/element', methods=['POST'])
def find_element(session_id):
    """查找元素"""
    if session_id not in driver_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    data = request.get_json()
    strategy = data.get('strategy')
    locator = data.get('locator')
    
    if not strategy or not locator:
        return jsonify({'error': 'Missing strategy or locator parameters'}), 400
    
    try:
        element = driver_sessions[session_id].find_element(strategy, locator)
        return jsonify({
            'status': 'success',
            'elementId': element
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/<session_id>/element/<element_id>/click', methods=['POST'])
def click_element(session_id, element_id):
    """点击元素"""
    if session_id not in driver_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    try:
        driver_sessions[session_id].click_element(element_id)
        return jsonify({'status': 'success', 'message': 'Element clicked'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/session/<session_id>/element/<element_id>/text', methods=['POST'])
def send_text(session_id, element_id):
    """发送文本到元素"""
    if session_id not in driver_sessions:
        return jsonify({'error': 'Session not found'}), 404
    
    data = request.get_json()
    text = data.get('text')
    
    if text is None:
        return jsonify({'error': 'Missing text parameter'}), 400
    
    try:
        driver_sessions[session_id].send_keys(element_id, text)
        return jsonify({'status': 'success', 'message': 'Text sent'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
