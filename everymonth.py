#encoding:utf8
import datetime, time
import requests
import gevent
from gevent import pool, monkey, queue, Timeout

from weiboyi.public.get_cookie import get_cookies
from weiboyi.public.connect_db import connect_db
from weiboyi.public.logger import logger
from weiboyi.spider import weixin
from weiboyi.spider import weibo
from weiboyi.spider.shortvideo import getvideoprice
from weiboyi.spider.shortvideo_dosql import shortvideosql
from weiboyi.spider.weibo_dosql import straight_price, forward_price, wbbasedata
from weiboyi.spider.weixin_dosql import toutiaoprice, secondprice, contentprice, wxbasedata

monkey.patch_all()
p = pool.Pool(5)
q = queue.Queue()

def get_insertid():
    """获取需要插入数据的id"""
    # 获取昨天入库的数据
    conn = connect_db()
    cursor = conn.cursor()
    # 设置client、connection、results编码方式为utf8mb4
    cursor.execute("SET NAMES utf8mb4")
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection = utf8mb4")
    sql = "select id, platformID, accountID, `name`, indexUrl  from PlatformIPAccount " \
          " where  platformID in (1,2,3,10,12,13)"
    cursor.execute(sql)
    weixindatas = cursor.fetchall()
    conn.close()
    return weixindatas

def dealitem(item):
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if item is None:
        return
    for k in item:
        if item[k] == None:
            item[k] = 0
        if item['last_update_time'] == 0:
            item['last_update_time'] = nowtime
    item['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 创建时间
    item['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 更新时间
    item['status'] = 0
    return item

def insertdata(data,cookie):
    if data[1] == 12:
        #微信
        item = weixin.get_data(data[2], cookie)
        item = dealitem(item)
        if item:
            #微信基础数据
            wxbasedata(data,item)
            #头条价格
            toutiaoprice(data[0],item)
            #次条价格
            secondprice(data[0],item)
            #原创内容价格
            contentprice(data[0],item)
    elif data[1] == 13:
        # 微博
        item = weibo.get_data(data[3], cookie)
        item = dealitem(item)
        if item:
            #微博基础数据
            wbbasedata(data,item)
            #直发价格
            straight_price(data[0], item)
            #转发价格
            forward_price(data[0], item)
    else:
        #获取短视频价格
        item = getvideoprice(data[2],cookie)
        if item:
            shortvideosql(data,item)

def mainfun():
    res = []
    datas = get_insertid()
    cookie = get_cookies('http://chuanbo.weiboyi.com/hworder/sina/index')
    for data in datas:
        print(data)
        try:
            res.append(p.spawn(insertdata, data, cookie))
        except ValueError:
            continue
    gevent.joinall(res)
    print('本月更新完成')

if __name__ == '__main__':
    mainfun()