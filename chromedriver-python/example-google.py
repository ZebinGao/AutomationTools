from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 1. 初始化驱动（确保你的 chromedriver 版本与 Chrome 一致）
service = Service(ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service)

try:
    # 2. 打开 Google (根据截图显示是德语界面)
    driver.get("https://www.google.com")

    # 3. 处理 Cookie 弹窗 (Google 经常会弹出一个全屏的隐私同意确认框)
    # 如果有弹窗，我们需要点击“全部接受”按钮，否则无法操作搜索框
    try:
        # 寻找包含 "Alle akzeptieren" 或 "Accept all" 字样的按钮
        accept_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Alle akzeptieren') or contains(., 'Accept all')]"))
        )
        accept_button.click()
    except:
        print("未发现 Cookie 确认弹窗，继续执行")

    # 4. 定位搜索框
    # Google 搜索框通常是一个 textarea 或 input，name 属性固定为 'q'
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )

    # 5. 模拟选中、输入并回车
    search_box.clear()               # 清空现有内容
    time.sleep(2)
    search_box.send_keys("Python Selenium Tutorial") # 输入搜索词
    time.sleep(3)
    search_box.send_keys(Keys.ENTER) # 模拟按下回车键

    # 6. 等待结果加载
    time.sleep(5)

finally:
    # 运行完毕后关闭浏览器
    time.sleep(5)
    driver.quit()