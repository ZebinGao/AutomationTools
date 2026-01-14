from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. 初始化驱动 (确保路径正确)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # 2. 访问自己的网页
    driver.get("https://zebin-yue.top/about/")

    # 3. 使用层级定位
    top = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#top > a"))
    )

    # 4. 模拟输入并回车
    top.click()
    time.sleep(1)
    top.send_keys("Python 自动化爬虫")
    
    # 直接发送回车键
    top.send_keys(Keys.ENTER) 

    # 很多搜索引擎（如百度、谷歌）为了提升用户体验，会在页面加载完成后，通过 JavaScript 自动将光标定位（focus）在搜索框中。
    
    # 获取搜索结果中的标题 (通常是 h3 标签)
    first_result = driver.find_element(By.CSS_SELECTOR, "h3")
    print(f"第一条搜索结果是: {first_result.text}")

    # 停留几秒方便观察
    time.sleep(5)

finally:
    driver.quit()