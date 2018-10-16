#encoding:utf8
from weiboyi.public.save_data import decide
from weiboyi.public.connect_db import connect_db
from weiboyi.public.save_data import save_data

def wxbasedata(data,item):
    result = decide(data[0])
    if result is "ok":
        updatewxsql1 = "update CrawlWeiboWeixinInfo set TotalReadNum=%s, AvgReadNum=%s, MaxReadNum=%s," \
                       "TopAvgReadNum=%s, TopAvgLikeNum=%s, LastUpdateTime='%s', CreateTime='%s', UpdateTime='%s', StatusValue=%s where ID=%s" \
                       % (item['total_read_num'], item['avg_read_num'], item['max_read_num'],
                          item['top_avg_read_num'], item['top_avg_like_num'], item['last_update_time'],
                          item['create_time'], item['update_time'], item['status'], data[0])
    else:
        updatewxsql1 = "insert into CrawlWeiboWeixinInfo(ID,TotalReadNum,AvgReadNum,MaxReadNum,TopAvgReadNum," \
                       "TopAvgLikeNum,LastUpdateTime,CreateTime,UpdateTime,StatusValue) " \
                       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                       %(data[0], item['total_read_num'], item['avg_read_num'], item['max_read_num'],item['top_avg_read_num'], item['top_avg_like_num'],
                          item['last_update_time'],item['create_time'], item['update_time'], item['status'])
    updatewxsql2 = "update PlatformIPAccount set avgReadCount = %s,avgLikeCount = %s WHERE accountID = '%s'" \
                   %(item['top_avg_read_num'], item['top_avg_like_num'], data[2])
    save_data(updatewxsql1)
    save_data(updatewxsql2)

def toutiaoprice(data,item):
    decide_sql = "select id,source,platformPriceNameID from PlatformIPAccountPrice where iPAcctountID = '%s' and source = 14 and platformPriceNameID = 1"%(data)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(decide_sql)
    conn.commit()
    decide = cursor.fetchall()
    if decide:
        if item['multi_top_original_writing'] != 0:
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=1 where id='%s'"%(item['multi_top_original_writing'],decide[0][0])
            #更新数据头条价格等于多图文第一条原创加发布价格，原创=1
        elif item['multi_top_original_writing'] == 0 and item['multi_top'] != 0:
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=0 where id='%s'"%(item['multi_top'],decide[0][0])
            #更新数据头条价格等于多图文第一条发布价格，原创=0
        elif item['multi_top_original_writing'] == 0 and item['multi_top'] == 0 and item['single_original_writing'] != 0:
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=1 where id='%s'"%(item['single_original_writing'],decide[0][0])
            #更新数据头条价格等于单图文原创加发布价格， 原创=1
        elif item['multi_top_original_writing'] == 0 and item['multi_top'] == 0 and item['single_original_writing'] == 0 and item['single'] != 0:
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=0 where id='%s'"%(item['single'],decide[0][0])
            #更新数据头条价格等于单图文发布价格， 原创=0
        else:
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=0 where id='%s'"%(0,decide[0][0])
            #更新数据头条价格等于0， 原创=0
        save_data(updateprice_sql)
    else:
        if item['multi_top_original_writing'] != 0:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',1,1,14,'%s',1)"%(data,item['multi_top_original_writing'],item['last_update_time'])
            #插入数据头条价格等于多图文第一条原创加发布价格，原创=1
        elif item['multi_top_original_writing'] == 0 and item['multi_top'] != 0:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',1,1,14,'%s',0)"%(data,item['multi_top'],item['last_update_time'])
            #插入数据头条价格等于多图文第一条发布价格，原创=0
        elif item['multi_top_original_writing'] == 0 and item['multi_top'] == 0 and item['single_original_writing'] != 0:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',1,1,14,'%s',1)"%(data,item['single_original_writing'],item['last_update_time'])
            #插入数据头条价格等于单图文原创加发布价格， 原创=1
        elif item['multi_top_original_writing'] == 0 and item['multi_top'] == 0 and item['single_original_writing'] == 0 and item['single'] != 0:
            insertprice_sql =  "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',1,1,14,'%s',0)"%(data,item['single'],item['last_update_time'])
            #插入数据头条价格等于单图文发布价格， 原创=0
        else:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',1,1,14,'%s',0)"%(data,0,item['last_update_time'])
            #插入数据头条价格等于0， 原创=0
        save_data(insertprice_sql)

def secondprice(data, item):
    decide_sql = "select id,source,platformPriceNameID from PlatformIPAccountPrice where iPAcctountID = '%s' and source = 14 and platformPriceNameID = 8"%(data)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(decide_sql)
    conn.commit()
    decide = cursor.fetchall()
    if decide:
        if item['multi_second_original_writing'] != 0:
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=1 where id='%s'"%(item['multi_second_original_writing'],decide[0][0])
            #更新数据次条价格等于多图文第1条原创加发布价格，原创=1
        elif item['multi_second_original_writing'] == 0 and item['multi_second'] != 0:
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=0 where id='%s'"%(item['multi_second'],decide[0][0])
            #更新数据次条价格等于多图文第一条发布价格，原创=0
        else:
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=0 where id='%s'"%(0,decide[0][0])
            #更新数据次条价格等于0， 原创=0
        save_data(updateprice_sql)
    else:
        if item['multi_second_original_writing'] != 0:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',8,1,14,'%s',1)"%(data,item['multi_second_original_writing'],item['last_update_time'])
        elif item['multi_second_original_writing'] == 0 and item['multi_second'] != 0:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',8,1,14,'%s',0)"%(data,item['multi_second'],item['last_update_time'])
        else:
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',8,1,14,'%s',0)"%(data,0,item['last_update_time'])
            # print(insertprice_sql)
            #插入数据头条价格等于0， 原创=0
        save_data(insertprice_sql)

def contentprice(data,item):
    decide_sql = "select id,source,platformPriceNameID from PlatformIPAccountPrice where iPAcctountID = '%s' and source = 14 and platformPriceNameID = 2"%(data)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(decide_sql)
    conn.commit()
    decide = cursor.fetchall()
    if decide:
        if item['multi_top_original_writing'] != 0 and item['multi_top'] != 0:
            #多图文第一条原创+发布，多图文第一条发布都存在时，原创内容价格=（多图文第一条原创+发布）-（多图文第一条发布）
            originalprice = item['multi_top_original_writing'] - item['multi_top']
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=1 where id='%s'"%(originalprice,decide[0][0])
        elif item['multi_top_original_writing'] == 0 and item['multi_top'] == 0 and item['single_original_writing'] != 0 and item['single'] != 0:
            #多图文第一条原创+发布，多图文第一条发布都不存在时，且单图文原创+发布，单图文发布都存在时，原创内容价格 = （单图文原创+发布）-（单图文发布）
            originalprice = item['single_original_writing'] - item['single']
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=1 where id='%s'"%(originalprice,decide[0][0])
        elif item['multi_top_original_writing'] == 0 and item['multi_top'] == 0 and item['single_original_writing'] == 0 and item['single'] == 0 and item['multi_second_original_writing'] != 0 and item['multi_second'] != 0:
            #多图文第一条原创+发布，多图文第一条发布都不存在时，且单图文原创+发布，单图文发布都不存在时.多图文第二条原创+发布，多图文第二条发布都存在时，原创内容价格 = （多图文第二条原创+发布）-（多图文第二条发布）
            originalprice = item['multi_second_original_writing'] - item['multi_second']
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=1 where id='%s'"%(originalprice,decide[0][0])
        else:
            #剩下的其他情况，原创内容皆为0
            originalprice = 0
            updateprice_sql = "update PlatformIPAccountPrice set price='%s',isOriginal=1 where id='%s'"%(originalprice,decide[0][0])
        save_data(updateprice_sql)
    else:
        # global insertprice_sql
        if item['multi_top_original_writing'] != 0 and item['multi_top'] != 0:
            sign = 1
            originalprice = item['multi_top_original_writing'] - item['multi_top']
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',2,1,14,'%s',1)"%(data,originalprice,item['last_update_time'])
            save_data(insertprice_sql)
        elif item['multi_top_original_writing'] == 0 and item['multi_top'] == 0 and item['single_original_writing'] != 0 and item['single'] != 0:
            sign = 1
            originalprice = item['single_original_writing'] - item['single']
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',2,1,14,'%s',1)"%(data,originalprice,item['last_update_time'])
        elif item['multi_top_original_writing'] == 0 and item['multi_top'] == 0 and item['single_original_writing'] == 0 and item['single'] == 0 and item['multi_second_original_writing'] != 0 and item['multi_second'] != 0:
            sign = 1
            originalprice = item['multi_second_original_writing'] - item['multi_second']
            insertprice_sql = "insert into PlatformIPAccountPrice(iPAcctountID,price,platformPriceNameID,statusIndex,source,createdTime,isOriginal) VALUES ('%s','%s',2,1,14,'%s',1)"%(data,originalprice,item['last_update_time'])
        else:
            sign = 0
        #剩下其他情况皆为原创内容为0，且不做任何操作
        # print(insertprice_sql)
        if sign == 1:
            save_data(insertprice_sql)







