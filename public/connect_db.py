import pymysql


def connect_db():
    """
    连接mysql数据库
    :return: 数据库连接以及游标
    """
    conn = pymysql.connect(host='********',
                           user='**************',
                           password='****************',
                           # 线上库
                           database='***********',
                           charset="utf8mb4")
    return conn
