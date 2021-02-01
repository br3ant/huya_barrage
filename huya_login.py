import os
import pickle
import platform
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import config


class HuyaDriver:
    def __init__(self, room_id):
        options = webdriver.ChromeOptions()
        prefs = {
            "profile.default_content_setting_values.plugins": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
            "PluginsAllowedForUrls": "https://www.huya.com"
        }
        options.add_experimental_option("prefs", prefs)
        # options.add_argument('--ignore-certificate-errors')
        if platform.system() == 'Windows':
            executable_path = './win/chromedriver.exe'
        elif platform.system() == 'Darwin':
            executable_path = './mac/chromedriver'
        elif platform.system() == 'Linux':
            executable_path = './linux/geckodriver'
        else:
            executable_path = ''
        self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=options)

        # 隐式等待是全局性的，只要用了driver.findxx没有第一时间找到元素，就会等待5s，当然一般都被用wait覆盖掉了
        self.driver.implicitly_wait(5)
        # 显示等待是定向性的，最大等待时间10s,每次检测元素有没有生成的时间间隔300ms，过了最大等待时间抛出异常
        self.wait = WebDriverWait(self.driver, timeout=10, poll_frequency=300)

        self.url = f'https://www.huya.com/{room_id}'

        if os.path.exists(config.get('cookie_path')):
            print("当前目录下存在虎牙登录的cookie文件，将为您自动登录")
            self.login_with_cookie()
        else:
            print("当前目录下不存在虎牙登录的cookie文件")
            self.login_with_qr()

        # self.close_video()

    def close_video(self):
        print('关闭video')
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="pub_msg_input"]')))
        except:
            print("对不起，暂停按钮")
            return

    def login_with_qr(self):
        self.driver.get(self.url)

        self.driver.maximize_window()
        print(self.driver.title)
        # 这个是最垃圾的等待，都定死啦
        time.sleep(1)

        # login_button = self.wait.until(
        #     EC.element_to_be_clickable(
        #         (By.XPATH, '//*[@id="nav-login"]')))
        # driver.find_element_by_link_text("登录").click()
        # 点击登录按钮
        # login_button.click()

        # 这个时候我们用二维码登录，设置最多等待3分钟，如果登录那个区域是可见的，就登录成功
        WebDriverWait(self.driver, 180).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="login-username"]')))

        print("登录成功")
        # 保存cookie到cookies.pkl文件
        session = requests.Session()
        # 获取cookie
        cookies = self.driver.get_cookies()
        # 把cookie写入文件
        if not os.path.exists("cookie"):
            os.mkdir("cookie")
        pickle.dump(cookies, open(config.get('cookie_path'), "wb"))

    def login_with_cookie(self):

        # driver.get("https://www.douyu.com")
        self.driver.get(self.url)
        self.driver.maximize_window()
        # 把cookie文件加载出来
        with open(config.get('cookie_path'), "rb") as cookiefile:
            cookies = pickle.load(cookiefile)
        for cookie in cookies:
            print(cookie)
            self.driver.add_cookie(cookie)
        time.sleep(3)
        self.driver.refresh()
        # 如果登录成功那个区域不可见的，说明cookie没有登录成功，重新用二维码登录
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="login-username"]')))
        except:
            print("对不起，使用cookie登录失败，请重新扫描二维码登录")
            self.login_with_qr()

        print("登录成功")
        print(self.driver.title)

    def send_barrage(self, message):
        # print('开始输入弹幕')
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="pub_msg_input"]')))
        except:
            print("对不起，没有找到输入框")
            return

        # 清空输入框信息
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="pub_msg_input"]'))).clear()

        time.sleep(3)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="pub_msg_input"]'))).send_keys(message)
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="msg_send_bt"]'))).click()
        print(f'发送成功 message = {message}')

    def colse(self):
        self.driver.close()


if __name__ == "__main__":
    driver = HuyaDriver('10132155')
    driver.send_barrage('hahah')
