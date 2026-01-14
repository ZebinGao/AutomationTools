# WebScraper-python-selenium
爬取自己的文章和图片，绝对合法

## 安装环境

python -m venv venv
.\venv\Scripts\activate

## 安装配置
pip install -r .\requirements.txt

## 配置端口，因为使用了VPN
git config --global http.proxy 'http://127.0.0.1:7880'
git config --global https.proxy 'http://127.0.0.1:7880'

## 新建cookies文件夹
参考如下的指令
clean_cookies_path = r'D:\GitHub\WebScraper-python-selenium\login-cookies'


## 多个python环境冲突

升级selenium
`python -m pip install --upgrade selenium`

安装driver
`python -m pip install webdriver-manager`