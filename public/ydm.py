import requests
import json


def get_captcha():

    captcha_username = '*****'  # 打码网站用户名
    captcha_password = '********'   # 打码网站密码
    captcha_appid = 1
    captcha_appkey = '22cc5376925e9387a23cf797cb9ba745'
    captcha_codetype = '1004'
    captcha_url = 'http://api.yundama.com/api.php?method=upload'
    # captcha_result_url = 'http://api.yundama.com/api.php?cid={}&method=result'
    filename = 'captcha.png'
    timeout = 60

    data = {'method': 'upload', 'username': captcha_username, 'password': captcha_password, 'appid': captcha_appid, 'appkey': captcha_appkey, 'codetype': captcha_codetype, 'timeout': timeout}
    f = open(filename, 'rb')
    file = {'file': f}
    response = requests.post(captcha_url, data, files=file).text
    f.close()
    response_dict = json.loads(response)
    result = response_dict['text']
    print(result)
    return result

if __name__ == '__main__':
    res = get_captcha()
    print(res)