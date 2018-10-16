import time
import requests
from weiboyi.public.ydm import get_captcha
# from ydm import get_captcha
from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as ec


def enter_captcha(driver):
    """
    输入验证码
    :param driver: 
    :return: 包含Cookie的driver
    """
    captcha_url = driver.find_element_by_xpath("//img[@id='captcha']").get_attribute('src')

    response = requests.get(captcha_url)
    with open('captcha.png', 'wb') as f:
        f.write(response.content)
    times = 20
    while True:
        if times <= 0:
            break
        pic_code = get_captcha()
        if pic_code:
            print(pic_code)
            driver.find_element_by_id('piccode').send_keys(pic_code)
            driver.find_element_by_class_name('btn_wrap').click()
            time.sleep(1)
            return driver
        else:
            print('正在识别验证码...请稍后')
            times -= 1


def get_cookies(url):
    """
    采用selenium模拟登陆 获取登陆cookie
    :return: Cookie 
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(r'F:\python\python_wangxingyue\chromedriver_win32\chromedriver.exe',chrome_options=chrome_options)
    # driver = webdriver.Chrome(r'G:\Program Files\feiq\Recv Files\chromedriver.exe',chrome_options=chrome_options)
    # driver = webdriver.Chrome('G:/Program Files/feiq/Recv Files/chromedriver', chrome_options=chrome_options)
    # driver = webdriver.Chrome('/home/bigdata/lin/yuanrong2.1/chromedriver')
    driver.get(url)
    time.sleep(1)
    driver.find_element_by_id('username').send_keys('violin6')
    time.sleep(0.5)
    driver.find_element_by_id('password').send_keys('abc123123')
    # 输入验证码
    driver = enter_captcha(driver)
    # 构建Cookie
    cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
    cookie_str = ';'.join(item for item in cookie)
    return cookie_str

# if __name__ == '__main__':
#     url = 'http://chuanbo.weiboyi.com/hworder/sina/index'
#     cookie = get_cookies(url)
#     print(cookie)
