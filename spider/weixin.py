import json
import requests, re
# from fake_useragent import UserAgent
import faker
# from public.deal_name import deal_pack_name
from weiboyi.public.get_cookie import get_cookies
from weiboyi.public.get_token import get_token
from weiboyi.public.logger import logger


def get_base_data(weibo_type, weibo_id, sign, cookie):
    headers = {
        'Cookie':cookie,
    }
    # 获取总阅读数、平均阅读数、最大阅读数、头条平均阅读数、头条平均点赞数
    data_url = 'http://chuanbo.weiboyi.com/single/wbyapi/getbaseshuju?weibo_type={}&weibo_id={}&sign={}&app_type='
    data_response = requests.get(data_url.format(weibo_type, weibo_id, sign))
    # 获取头条原创+发布价格，次条原创+发布价格，单图文原创+发布价格
    num_url = 'http://chuanbo.weiboyi.com/single/wbyapi/getaccountbaojia?weibo_type={}&weibo_id={}&sign={}&app_type='
    # print(num_url.format(weibo_type, weibo_id, sign))
    num_response = requests.get(num_url.format(weibo_type, weibo_id, sign), headers=headers)
    try:
        num_dict = json.loads(num_response.content.decode())
        data_dict = json.loads(data_response.content.decode())
    # except Exception as e:
    except json.decoder.JSONDecodeError:
        return
    if 'multi_top' in num_dict['data']['price'].keys():
    #头条发布价
        multi_top = num_dict['data']['price']['multi_top']
        #头条原创+发布价格
        multi_top_original_writing = num_dict['data']['price']['multi_top_original_writing']
        #次条发布价格
        multi_second = num_dict['data']['price']['multi_second']
        #次条发布+原创价格
        multi_second_original_writing = num_dict['data']['price']['multi_second_original_writing']
        #单图文发布价格
        single = num_dict['data']['price']['single']
        #单图文原创+发布价格
        single_original_writing = num_dict['data']['price']['single_original_writing']
    else:
        multi_top = num_dict['data']['price']['multi_graphic_top_price']
        multi_top_original_writing = 0
        multi_second = num_dict['data']['price']['multi_graphic_second_price']
        multi_second_original_writing = 0
        single = num_dict['data']['price']['single_graphic_price']
        single_original_writing = 0
    # 头条平均阅读数
    top_avg_read_num = data_dict['data']['msgitem_top_avg_read_num_28d']
    if top_avg_read_num == '10W+':
        top_avg_read_num = 100001
    if top_avg_read_num == -1:
        top_avg_read_num = 0

    # 头条平均点赞数
    top_avg_like_num = data_dict['data']['msgitem_top_avg_like_num_28d']
    if top_avg_like_num == -1:
        top_avg_like_num = 0
    total_num = data_dict['data']['msgitem_top_avg_read_num_28d']
    if total_num is not 0:
        total_num = total_num * 30
    else:
        total_num = 0
    avg_read_num = data_dict['data']['msgitem_top_avg_read_num_28d']
    max_read_num = data_dict['data']['msgitem_top_max_read_num_28d']
    item = {
        'total_read_num': total_num,
        'avg_read_num': avg_read_num,
        'max_read_num': max_read_num,
        'top_avg_read_num': top_avg_read_num,
        'top_avg_like_num': top_avg_like_num,
        'multi_top':multi_top,
        'multi_top_original_writing':multi_top_original_writing,
        'multi_second':multi_second,
        'multi_second_original_writing':multi_second_original_writing,
        'single':single,
        'single_original_writing':single_original_writing,
    }
    return item


def get_habit_data(weibo_type, weibo_id, sign):
    # 获取更新时间
    habit_url = 'http://chuanbo.weiboyi.com/single/wbyapi/getaccounthabit?weibo_type={}&weibo_id={}&sign={}&app_type='
    habit_response = requests.get(habit_url.format(weibo_type, weibo_id, sign))
    habit_dict = json.loads(habit_response.content.decode())
    # 更新时间
    last_update_time = habit_dict['data']['latest_update_time']
    return last_update_time


def get_data(query_name, cookie):
    headers = {'User-Agent': faker.Faker().user_agent(),
               'Cookie': cookie}
    token = get_token(headers)
    if token is None:
        logger.error('token未匹配到')
        return

    post_url = 'http://chuanbo.weiboyi.com/hworder/weixin/filterlist/source/all'
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
                        url = each['cells']['url']
                    except KeyError:
                        print('未匹配到微信%s下的url字段' % query_name)
                    else:
                        regex = 'weibo_id=(.*)&weibo_type=(.*)&sign=(.*)'
                        weibo_id, weibo_type, sign = re.findall(regex, url)[0]
                        item = get_base_data(weibo_type, weibo_id, sign, cookie)
                        if item == None:
                            return item
                        last_update_time = get_habit_data(weibo_type, weibo_id, sign)
                        item['last_update_time'] = last_update_time
                        return item
                    break
    else:
        print('微信下:%s未获取到数据' % query_name)
        return None

