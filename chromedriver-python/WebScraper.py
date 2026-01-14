from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

web_Url = "https://www.baidu.com"

options = webdriver.ChromeOptions()
#如果你想指定chrome浏览器的位置，可以取消下面一行的注释并指定路径
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# 如果你非要用原来的路径，请确保关闭所有已打开的 Chrome
#clean_cookies_path = r'D:\GitHub\WebScraper-python-selenium\login-cookies'
# 添加启动参数
#options.add_argument(f'--user-data-dir={clean_cookies_path}')

#自动下载并启动chromerdriver
service = Service(ChromeDriverManager().install())
#options.add_experimental_option("excludeSwitches", "127.0.0.1:5050")
browser = webdriver.Chrome(service=service, options=options)
browser.get(web_Url)

a = 1