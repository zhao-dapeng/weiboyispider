#encoding:utf8
import pymysql
from weiboyi.public.connect_db import connect_db
from weiboyi.public.logger import logger

def save_data(sql):
    conn = connect_db()
    cursor = conn.cursor()
    # 设置client、connection、results编码方式为utf8mb4
    cursor.execute("SET NAMES utf8mb4")
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection = utf8mb4")
    try:
        cursor.execute(sql)
        print(sql)
    except pymysql.IntegrityError:
        print('数据已存在',sql)
    except Exception as e:
        logger.error('执行SQL发生异常 原因是：%s' % e)
        logger.error('SQL为：%s' % sql)
    else:
        conn.commit()
    finally:
        conn.close()

def decide(num):
    conn = connect_db()
    cursor = conn.cursor()
    # 设置client、connection、results编码方式为utf8mb4
    cursor.execute("SET NAMES utf8mb4")
    cursor.execute("SET CHARACTER SET utf8mb4")
    cursor.execute("SET character_set_connection = utf8mb4")
    findsql = "SELECT * from CrawlWeiboWeixinInfo where ID=%s" % (num)
    cursor.execute(findsql)
    conn.commit()
    res = cursor.fetchall()
    if res:
        return 'ok'
    else:
        return 'error'
