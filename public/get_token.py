import requests
from lxml import etree


def get_token(headers):
    # 获取token
    url = 'http://chuanbo.weiboyi.com/hworder/weixin/index'

    response = requests.get(url, headers=headers)
    html = etree.HTML(response.content.decode())
    token = html.xpath("//input[@name='web_csrf_token']/@value")
    if token:
        token = token[0]
    else:
        token = None
    return token


