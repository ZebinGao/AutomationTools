import requests
import json
import base64
from typing import Optional, Dict, Any

class WinAppDriverClient:
    def __init__(self, winappdriver_url: str, app_path: str = None):
        """
        初始化 WinAppDriver 客户端
        
        :param winappdriver_url: WinAppDriver 服务地址
        :param app_path: 要启动的应用程序路径
        """
        self.winappdriver_url = winappdriver_url.rstrip('/')
        self.app_path = app_path
        self.session_id = None
        self.element_cache = {}  # 缓存元素 ID
        
    def start_application(self) -> Dict[str, Any]:
        """
        启动应用程序并创建会话
        
        :return: 会话响应
        """
        capabilities = {
            "platformName": "Windows",
            "deviceName": "WindowsPC",
            "app": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App",
            "ms:waitForAppLaunch": "10"  # 关键点：增加启动等待时间
        }
        
        if not self.app_path:
            raise ValueError("Application path is required to start application")
            
        # headers = {
        # "Content-Type": "application/json; charset=utf-8",
        # "Accept": "application/json"
        # }
        response = requests.post(
            f"{self.winappdriver_url}/session",
            json={"desiredCapabilities": capabilities}
            # headers=headers 
        )
        
        if response.status_code == 200:
            data = response.json()
            self.session_id = data.get('sessionId')
            return data
        else:
            raise Exception(f"Failed to start application: {response.text}")
    
    def quit(self):
        """
        关闭会话
        """
        if self.session_id:
            try:
                requests.delete(f"{self.winappdriver_url}/session/{self.session_id}")
            except:
                pass  # 忽略关闭会话时的错误
            finally:
                self.session_id = None
                self.element_cache.clear()
    
    def get_screenshot(self) -> str:
        """
        获取屏幕截图并返回 base64 编码的数据
        
        :return: Base64 编码的 PNG 截图数据
        """
        if not self.session_id:
            raise Exception("No active session")
            
        response = requests.get(f"{self.winappdriver_url}/session/{self.session_id}/screenshot")
        
        if response.status_code == 200:
            data = response.json()
            return data.get('value', '')
        else:
            raise Exception(f"Failed to get screenshot: {response.text}")
    
    def get_page_source(self) -> str:
        """
        获取当前页面的源码
        
        :return: 页面源码 XML
        """
        if not self.session_id:
            raise Exception("No active session")
            
        response = requests.get(f"{self.winappdriver_url}/session/{self.session_id}/source")
        
        if response.status_code == 200:
            data = response.json()
            return data.get('value', '')
        else:
            raise Exception(f"Failed to get page source: {response.text}")
    
    def find_element(self, strategy: str, locator: str) -> str:
        """
        查找元素
        
        :param strategy: 查找策略 (e.g., "name", "id", "xpath")
        :param locator: 查找定位器
        :return: 元素 ID
        """
        if not self.session_id:
            raise Exception("No active session")
            
        # 构造缓存键
        cache_key = f"{strategy}:{locator}"
        
        # 检查缓存
        if cache_key in self.element_cache:
            return self.element_cache[cache_key]
            
        response = requests.post(
            f"{self.winappdriver_url}/session/{self.session_id}/element",
            json={
                "using": strategy,
                "value": locator
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            element_id = data.get('value', {}).get('ELEMENT')
            if element_id:
                # 缓存元素 ID
                self.element_cache[cache_key] = element_id
                return element_id
            else:
                raise Exception("Element not found")
        else:
            raise Exception(f"Failed to find element: {response.text}")
    
    def click_element(self, element_id: str):
        """
        点击元素
        
        :param element_id: 元素 ID
        """
        if not self.session_id:
            raise Exception("No active session")
            
        response = requests.post(
            f"{self.winappdriver_url}/session/{self.session_id}/element/{element_id}/click"
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to click element: {response.text}")
    
    def send_keys(self, element_id: str, text: str):
        """
        发送文本到元素
        
        :param element_id: 元素 ID
        :param text: 要发送的文本
        """
        if not self.session_id:
            raise Exception("No active session")
            
        response = requests.post(
            f"{self.winappdriver_url}/session/{self.session_id}/element/{element_id}/value",
            json={
                "value": list(text)  # WinAppDriver 期望字符列表
            }
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to send keys: {response.text}")

    def clear_element(self, element_id: str):
        """
        清除元素内容
        
        :param element_id: 元素 ID
        """
        if not self.session_id:
            raise Exception("No active session")
            
        response = requests.post(
            f"{self.winappdriver_url}/session/{self.session_id}/element/{element_id}/clear"
        )
        
        if response.status_code != 200:
            raise Exception(f"Failed to clear element: {response.text}")
