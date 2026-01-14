from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1. 初始化驱动 (确保路径正确)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # 2. 访问百度
    driver.get("https://www.baidu.com/s?wd=")

    # 3. 定位百度的搜索输入框
    # 百度输入框的 ID 长期以来一直是 'kw' (取自 "Key Word")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "kw"))
    )

    # 4. 模拟输入并回车
    search_box.click()
    time.sleep(1)
    search_box.send_keys("Python 自动化爬虫")
    
    # 直接发送回车键
    search_box.send_keys(Keys.ENTER) 
    

    # 5. 等待搜索结果加载并打印第一条结果的标题
    # 搜索结果通常在 id 为 'content_left' 的容器中
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content_left"))
    )
    
    # 获取搜索结果中的标题 (通常是 h3 标签)
    first_result = driver.find_element(By.CSS_SELECTOR, "h3")
    print(f"第一条搜索结果是: {first_result.text}")

    # 停留几秒方便观察
    time.sleep(5)

finally:
    driver.quit()