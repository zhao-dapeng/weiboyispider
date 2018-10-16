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


if __name__ == '__main__':
    # cookie = '_gscu_867320846=26975698xi8dnn44; loginHistoryRecorded=0; TRACK_DETECTED=1.0.1; ' \
    #          'TRACK_BROWSER_ID=3ba3dbb5a3f12da2e8f9a831d912617e; Hm_lvt_28390dde54d52b2842a44c05fcdb31f7=1527060999; ' \
    #          'TOUR_GUEST_RANK_DETAIL=1; Hm_lvt_29d7c655e7d1db886d67d7b9b3846aca=1528081253; ' \
    #          'Hm_lpvt_29d7c655e7d1db886d67d7b9b3846aca=1528081253; _gscbrs_867320846=1; ' \
    #          'Hm_lvt_b96f95878b55be2cf49fb3c099aea393=1528081254; ' \
    #          'Hm_lpvt_b96f95878b55be2cf49fb3c099aea393=1528081254; PHPSESSID=kge4r2kubo3c0k7sstb5vssv97; ' \
    #          'aLastLoginTime=1528081216; _gscs_867320846=280812534f03gt43|pv:2; ' \
    #          'Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1528081314; ' \
    #          'Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1528081314; ' \
    #          '_pk_ref.2.c366=%5B%22%22%2C%22%22%2C1528081315%2C%22http%3A%2F%2Fwww.weiboyi.com%2F%22%5D; ' \
    #          '_pk_id.2.c366=c079ad01fd4fe5f6.1528081315.1.1528081315.1528081315.; _pk_ses.2.c366=*; ' \
    #          'TRACK_USER_ID=454771; TRACK_IDENTIFY_AT=2018-06-04T03%3A01%3A54.772Z; ' \
    #          'TRACK_SESSION_ID=755639ebc96646931492a61cbad44150 '
    cookie = get_cookies('http://chuanbo.weiboyi.com/hworder/sina/index')
    # cookie = 'rememberusername=;aLastLoginTime=1528708797;TY_SESSION_ID=b913761b-d6c9-4228-9311-a24eb420353f;PHPSESSID=dnhdb6jd2cj1hpe2u4k6b3p710;_pk_ses.2.c366=*;_gscu_867320846=28708884elu3b212;_gscbrs_867320846=1;Hm_lvt_5ff3a7941ce54a1ba102742f48f181ab=1528708899;username=;loginHistoryRecorded=0;Hm_lpvt_5ff3a7941ce54a1ba102742f48f181ab=1528708899;_pk_id.2.c366=bfa76453cf38eaa4.1528708885.1.1528708899.1528708885.;_gscs_867320846=28708884xz0e2u12|pv:2;TRACK_USER_ID=454771;TRACK_IDENTIFY_AT=2018-06-11T09%3A21%3A38.834Z;TRACK_SESSION_ID=09e29d18d563e34505fe1463b2df6e45;TRACK_DETECTED=1.0.1;TRACK_BROWSER_ID=012b10a580d91c423d51ae04172d2735;sajssdk_2015_cross_new_user=1;sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22454771%22%2C%22%24device_id%22%3A%22163ee26a0bb818-0000eba871abe8-737356c-1049088-163ee26a0bc3d8%22%2C%22props%22%3A%7B%7D%2C%22first_id%22%3A%22163ee26a0bb818-0000eba871abe8-737356c-1049088-163ee26a0bc3d8%22%7D'
    name = ['lengtoo','rmrbwx']
    for i in range(len(name)):
        item = get_data(name[i], cookie)
        print(item)