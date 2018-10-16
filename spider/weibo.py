import json
import requests, re
# from fake_useragent import UserAgent
import faker
from weiboyi.public.deal_name import deal_pack_name
from weiboyi.public.get_token import get_token
from weiboyi.public.get_cookie import get_cookies
from weiboyi.public.logger import logger


def get_base_data(each):
    # 直发转发数
    tweet_avg_send_count = each['cells']['tweet_average_send_num']
    if '万' in str(tweet_avg_send_count):
        tweet_avg_send_count = int(float(str(tweet_avg_send_count).replace('万', '')) * 10000)
    # 直发评论数
    tweet_avg_posts_count = each['cells']['tweet_average_posts_num']
    if '万' in str(tweet_avg_posts_count):
        tweet_avg_posts_count = int(float(str(tweet_avg_posts_count).replace('万', '')) * 10000)
    # 直发点赞数
    tweet_avg_like_count = each['cells']['tweet_average_like_num']
    if '万' in str(tweet_avg_like_count):
        tweet_avg_like_count = int(float(str(tweet_avg_like_count).replace('万', '')) * 10000)
    # 转发数
    retweet_avg_send_count = each['cells']['retweet_average_send_num']
    if '万' in str(retweet_avg_send_count):
        retweet_avg_send_count = int(float(str(retweet_avg_send_count).replace('万', '')) * 10000)
    # 转发评论数
    retweet_avg_posts_count = each['cells']['retweet_average_posts_num']
    if '万' in str(retweet_avg_posts_count):
        retweet_avg_posts_count = int(float(str(retweet_avg_posts_count).replace('万', '')) * 10000)
    # 转发点赞数
    retweet_avg_like_count = each['cells']['retweet_average_like_num']
    if '万' in str(retweet_avg_like_count):
        retweet_avg_like_count = int(float(str(retweet_avg_like_count).replace('万', '')) * 10000)
    if each['cells']['net_deal_price'] is None:
        #直发报价
        tweet_price = each['cells']['external_reference_price']['tweet']['quote']
        #转发报价
        retweet_price = each['cells']['external_reference_price']['retweet']['quote']
        #软广转发
        soft_retweet_price = 0
        #软广直发
        soft_tweet_price = 0
    else:
        #直发报价
        tweet_price = each['cells']['net_deal_price']['tweet_price']
        #转发报价
        retweet_price = each['cells']['net_deal_price']['retweet_price']
        #软广转发
        soft_retweet_price = each['cells']['net_deal_price']['soft_retweet_price']
        #软广直发
        soft_tweet_price = each['cells']['net_deal_price']['soft_tweet_price']
    item = {
        'tweet_avg_send_count': tweet_avg_send_count,
        'tweet_avg_posts_count': tweet_avg_posts_count,
        'tweet_avg_like_count': tweet_avg_like_count,
        'retweet_avg_send_count': retweet_avg_send_count,
        'retweet_avg_posts_count': retweet_avg_posts_count,
        'retweet_avg_like_count': retweet_avg_like_count,
        'tweet_price':tweet_price,
        'retweet_price':retweet_price,
        'soft_retweet_price':soft_retweet_price,
        'soft_tweet_price':soft_tweet_price,
    }
    return item


def get_habit_data(weibo_type, weibo_id, sign):
    # 获取更新时间
    habit_url = 'http://chuanbo.weiboyi.com/single/wbyapi/getaccounthabit?weibo_type={}&weibo_id={}&sign={}&app_type='
    habit_response = requests.get(habit_url.format(weibo_type, weibo_id, sign))
    try:
        habit_dict = json.loads(habit_response.content.decode())
    except json.decoder.JSONDecodeError:
        print("json解析出错")
        return

    # 更新时间
    last_update_time = habit_dict['data']['latest_update_time']
    # print(last_update_time)
    return last_update_time


def get_data(query_name, cookie):
    headers = {'User-Agent': faker.Faker().user_agent(),
               'Cookie': cookie}
    token = get_token(headers)
    if token is None:
        logger.error('token未匹配到')
        return

    post_url = 'http://chuanbo.weiboyi.com/hworder/sina/filterlist/source/all'
    data = {
        'web_csrf_token': token,
        'query': query_name,
        'price_list': 'tweet,retweet',
        'start': 0,
        'limit': 20
    }
    query_response = requests.post(post_url, headers=headers, data=data)
    dict_data = json.loads(query_response.content.decode())
    datas = dict_data['data']
    result_num = datas['total']
    if result_num:
        result = datas['rows']
        for each in result:
            result_name = each['cells']['weibo_name']
            result_name = deal_pack_name(result_name)
            if result_name == query_name:
                item = get_base_data(each)
                try:
                    url = each['cells']['single_url']
                except KeyError:
                    logger.error('未匹配到微博%s下的single_url字段' % query_name)
                else:
                    regex = 'weibo_id=(.*)&weibo_type=(.*)&sign=(.*)'
                    weibo_id, weibo_type, sign = re.findall(regex, url)[0]
                    last_update_time = get_habit_data(weibo_type, weibo_id, sign)
                    item['last_update_time'] = last_update_time
                    return item
            break
    else:
        print('微博下:%s未获取到数据' % query_name)
        return None

if __name__ == '__main__':
    cookie = get_cookies('http://chuanbo.weiboyi.com/hworder/sina/index')
    name = '杨幂'
    item = get_data(name, cookie)
    print('bbbbbbbbbbb',item)