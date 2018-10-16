#encoding:utf8
import json
import requests, re
# from fake_useragent import UserAgent
import faker
# from public.deal_name import deal_pack_name
from weiboyi.public.get_cookie import get_cookies
from weiboyi.public.get_token import get_token
import datetime

def getprice(weibo_id,weibo_type,sign,cookie):
    headers = {
        'Cookie':cookie,
    }
    data_url = "http://chuanbo.weiboyi.com/single/wbyapi/getaccountbaojia?weibo_type={}&weibo_id={}&sign={}&app_type=video".format(weibo_type,weibo_id,sign)
    response = requests.get(url=data_url,headers=headers)
    try:
        data_dict = json.loads(response.content.decode())
    except json.decoder.JSONDecodeError:
        return
    createtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建时间
    if 'original_release' in data_dict['data']['price'].keys():
        #原创视频+发布
        original_release = data_dict['data']['price']['original_release']
        #视频发布
        video_release = data_dict['data']['price']['video_release']
        #活动现场直播
        filed_events = data_dict['data']['price']['filed_events']
        item = {
            'createtime':createtime,
            'original_release':original_release,
            'video_release':video_release,
            'filed_events':filed_events,
        }
    else:
        #视频发布
        price_video_release = data_dict['data']['price']['price_video_release']
        item = {
            'createtime':createtime,
            'price_video_release':price_video_release,
        }
    return item

def getvideoprice(query_name,cookie):
    headers = {'User-Agent': faker.Faker().user_agent(),
               'Cookie': cookie}
    token = get_token(headers)
    if token is None:
        print('token未匹配到')
        return

    post_url = 'http://chuanbo.weiboyi.com/hworder/video/filterlist/source/all'
    data = {
        'web_csrf_token': token,
        'query': query_name,
        'price_list': 'top,second,other,single',
        'start': 0,
        'limit': 20
    }
    query_response = requests.post(post_url, headers=headers, data=data)
    try:
        dict_data = json.loads(query_response.content.decode())
    except json.decoder.JSONDecodeError:
        return
    datas = dict_data['data']
    result_num = datas['total']
    if result_num:
        result = datas['rows']
        for each in result:
            if 'weibo_id' in each['cells']:
                result_name = each['cells']['weibo_id']
                if result_name == query_name:
                    try:
                        url = each['cells']['single_url']
                    except KeyError:
                        print('未匹配到微信%s下的url字段' % query_name)
                    else:
                        regex = 'weibo_id=(.*?)&weibo_type=(.*?)&sign=(.*?)&'
                        weibo_id, weibo_type, sign = re.findall(regex, url)[0]
                        item = getprice(weibo_id,weibo_type,sign,cookie)
                        return item
if __name__ == '__main__':
    cookie = get_cookies('http://chuanbo.weiboyi.com/hworder/sina/index')
    name = ['1061937080','kwaiinsight']
    for i in name:
        getvideoprice(i,cookie)
