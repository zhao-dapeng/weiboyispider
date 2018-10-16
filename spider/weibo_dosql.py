import pymysql
from weiboyi.public.save_data import decide
from weiboyi.public.connect_db import connect_db
from weiboyi.public.save_data import save_data


def wbbasedata(data,item):
    resultwb = decide(data[0])
    if resultwb is "ok":
        updatewbsql1 = "update CrawlWeiboWeixinInfo set RetweetAvgLikeNum=%s, RetweetAvgPostsNum=%s, RetweetAvgSendNum=%s, " \
                       "TweetAvgLikeNum=%s, TweetAvgPostsNum=%s, TweetAvgSendNum=%s, LastUpdateTime='%s', CreateTime='%s', UpdateTime='%s', " \
                       "StatusValue=%s where ID=%s" \
                       % (item['retweet_avg_like_count'], item['retweet_avg_posts_count'],
                          item['retweet_avg_send_count'], item['tweet_avg_like_count'], item['tweet_avg_posts_count'],
                          item['tweet_avg_send_count'], item['last_update_time'],
                          item['create_time'], item['update_time'], item['status'], data[0])
    else:
        updatewbsql1 = "insert into CrawlWeiboWeixinInfo(ID,RetweetAvgLikeNum,RetweetAvgPostsNum,RetweetAvgSendNum,TweetAvgLikeNum," \
                       "TweetAvgPostsNum,TweetAvgSendNum,LastUpdateTime,CreateTime,UpdateTime,StatusValue) " \
                       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                       %( data[0],item['retweet_avg_like_count'], item['retweet_avg_posts_count'],item['retweet_avg_send_count'], item['tweet_avg_like_count'],
                          item['tweet_avg_posts_count'],item['tweet_avg_send_count'], item['last_update_time'],item['create_time'],
                          item['update_time'], item['status'])
    updatewbsql2 = "update PlatformIPAccount set avgForwardCount = %s,avgCommontCount = %s where accountID = '%s'" \
                   %(item['tweet_avg_send_count'],item['tweet_avg_posts_count'],data[2])
    save_data(updatewbsql1)
    save_data(updatewbsql2)

# item = {'tweet_avg_send_count': 90000, 'tweet_avg_posts_count': 40000, 'tweet_avg_like_count': 190000, 'retweet_avg_send_count': 180000, 'retweet_avg_posts_count': 110000, 'retweet_avg_like_count': 170000, 'tweet_price': 694100, 'retweet_price': 0, 'soft_retweet_price': 0, 'soft_tweet_price': 0, 'last_update_time': '2018-07-24'}
def straight_price(data,item):
    decide_sql = "select id,source,platformPriceNameID from PlatformIPAccountPrice where iPAcctountID = '%s' and source = 14 and platformPriceNameID = 6"%(data)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(decide_sql)
    conn.commit()
    decide = cursor.fetchall()
    if decide:
        if item['soft_tweet_price'] != 0:
            updataprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=0 where id='%s'"%(item['tweet_price'],decide[0][0])
        elif item['soft_tweet_price'] == 0 and item['tweet_price'] != 0:
            updataprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=0 where id='%s'"%(item['soft_tweet_price'],decide[0][0])
        else:
            updataprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=0 where id='%s'"%(0,decide[0][0])
        save_data(updataprice_sql)
    else:
        if item['soft_tweet_price'] != 0:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',6,1,14,'%s',0)"%(data,item['tweet_price'],item['last_update_time'])
        # print(insertprice_sql)
        elif item['soft_tweet_price'] == 0 and item['tweet_price'] != 0:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',6,1,14,'%s',0)"%(data,item['soft_tweet_price'],item['last_update_time'])
        else:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',6,1,14,'%s',0)"%(data,0,item['last_update_time'])
        save_data(insertprice_sql)

def forward_price(data,item):
    decide_sql = "select id,source,platformPriceNameID from PlatformIPAccountPrice where iPAcctountID = '%s' and source = 14 and platformPriceNameID = 7"%(data)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(decide_sql)
    conn.commit()
    decide = cursor.fetchall()
    if decide:
        if item['soft_retweet_price'] != 0:
            updataprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=0 where id='%s'"%(item['retweet_price'],decide[0][0])
        elif item['soft_retweet_price'] == 0 and item['retweet_price'] != 0:
            updataprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=0 where id='%s'"%(item['soft_retweet_price'],decide[0][0])
        else:
            updataprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=0 where id='%s'"%(0,decide[0][0])
        save_data(updataprice_sql)
    else:
        if item['soft_retweet_price'] != 0:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',7,1,14,'%s',0)"%(data,item['retweet_price'],item['last_update_time'])
        # print(insertprice_sql)
        elif item['soft_retweet_price'] == 0 and item['retweet_price'] != 0:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',7,1,14,'%s',0)"%(data,item['soft_retweet_price'],item['last_update_time'])
        else:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',7,1,14,'%s',0)"%(data,0,item['last_update_time'])
        save_data(insertprice_sql)
