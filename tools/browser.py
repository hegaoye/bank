from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bankconfig import BROWSER_PATH


class Browser:
    """
    浏览器对象
    """

    def __init__(self):
        chrome_options = Options()
        # 浏览器不提供可视化页面
        # chrome_options.add_argument('--headless')
        # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--disable-gpu')
        # 以最高权限运行
        chrome_options.add_argument('--no-sandbox')
        # 启动就最大化
        chrome_options.add_argument('--start-maximized')
        # 以下用于有界面时配置项
        # 隐藏滚动条, 应对一些特殊页面
        # chrome_options.add_argument('--hide-scrollbars')
        # 不加载图片, 提升速度
        chrome_options.add_argument('blink-settings=imagesEnabled=false')

        self.browser = webdriver.Chrome(executable_path=BROWSER_PATH, chrome_options=chrome_options)
        self.browser.maximize_window()

    def get_brower(self):
        return self.browser
