#encoding:utf8
from weiboyi.public.save_data import save_data
from weiboyi.public.connect_db import connect_db

def shortvideosql(data,item):
    conn = connect_db()
    cursor = conn.cursor()
    existsql = "select iPAcctountID from PlatformIPAccountPrice where iPAcctountID = '%s' and source = 14"%(data[0])
    cursor.execute(existsql)
    conn.commit()
    decide = cursor.fetchall()
    if decide:
        if 'original_release' in item.keys():
            #更新原创视频+发布的价格
            updateoriginal = "update PlatformIPAccountPrice set price = '%s',isOriginal = '%s' where iPAcctountID = '%s' and platformPriceNameID = 3"\
                             %(item['original_release'],1,decide[0][0])
            save_data(updateoriginal)
            #更新活动现场直播
            updateevents = "update PlatformIPAccountPrice set price = '%s', isOriginal = '%s' where iPAcctountID = '%s' and platformPriceNameID = 5"\
                           %(item['filed_events'],0,decide[0][0])
            save_data(updateevents)
            #更新原创视频价格
            if item['original_release'] != 0 and item['video_release'] != 0:
                originalvideo = item['original_release'] - item['video_release']
                updatevideo = "update PlatformIPAccountPrice set price = '%s', isOriginal = '%s' where iPAcctountID = '%s' and platformPriceNameID = 4"\
                              %(originalvideo,1,decide[0][0])
            else:
                updatevideo = "update PlatformIPAccountPrice set price = '%s', isOriginal = '%s' where iPAcctountID = '%s' and platformPriceNameID = 4" \
                              %(0,0,decide[0][0])
            save_data(updatevideo)
        else:
            #更新原创视频+发布的价格
            updateoriginal = "update PlatformIPAccountPrice set price = '%s',isOriginal = '%s' where iPAcctountID = '%s' and platformPriceNameID = 3" \
                             %(item['price_video_release'],0,decide[0][0])
            save_data(updateoriginal)
            #更新活动现场直播
            updateevents = "update PlatformIPAccountPrice set price = '%s', isOriginal = '%s' where iPAcctountID = '%s' and platformPriceNameID = 5" \
                           %(0,0,decide[0][0])
            save_data(updateevents)
            #更新原创视频价格
            updatevideo = "update PlatformIPAccountPrice set price = '%s', isOriginal = '%s' where iPAcctountID = '%s' and platformPriceNameID = 4" \
                          %(0,0,decide[0][0])
            save_data(updatevideo)
    else:
        #有三种报价的字典结构
        if 'original_release' in item.keys():
            #插入原创视频+发布
            insertoriginal = "insert into PlatformIPAccountPrice(iPAcctountID, price, platformPriceNameID,statusIndex,source,createdTime,isOriginal) " \
                             "VALUES('%s','%s','%s','%s','%s','%s','%s')"%(data[0],item['original_release'],3,1,14,item['createtime'],1)
            save_data(insertoriginal)
            #插入活动现场直播
            insertevents = "insert into PlatformIPAccountPrice(iPAcctountID, price, platformPriceNameID,statusIndex,source,createdTime,isOriginal) " \
                            "VALUES('%s','%s','%s','%s','%s','%s','%s')"%(data[0],item['filed_events'],5,1,14,item['createtime'],0)
            save_data(insertevents)
            #当原创视频+发布价格和视频发布价格都不为空时，插入原创视频价格。
            if item['original_release'] != 0 and item['video_release'] != 0:
                originalvideo = item['original_release'] - item['video_release']
                insertvideo = "insert into PlatformIPAccountPrice(iPAcctountID, price, platformPriceNameID,statusIndex,source,createdTime,isOriginal) " \
                              "VALUES('%s','%s','%s','%s','%s','%s','%s')"%(data[0],originalvideo,4,1,14,item['createtime'],1)
            else:
                insertvideo = "insert into PlatformIPAccountPrice(iPAcctountID, price, platformPriceNameID,statusIndex,source,createdTime,isOriginal) " \
                              "VALUES('%s','%s','%s','%s','%s','%s','%s')"%(data[0],0,4,1,14,item['createtime'],0)
            save_data(insertvideo)
        #只有一种报价的结构
        else:
            #插入视频发布
            insertoriginal = "insert into PlatformIPAccountPrice(iPAcctountID, price, platformPriceNameID,statusIndex,source,createdTime,isOriginal) " \
                             "VALUES('%s','%s','%s','%s','%s','%s','%s')"%(data[0],item['price_video_release'],3,1,14,item['createtime'],0)
            save_data(insertoriginal)
            #插入活动现场直播
            insertevents = "insert into PlatformIPAccountPrice(iPAcctountID, price, platformPriceNameID,statusIndex,source,createdTime,isOriginal) " \
                           "VALUES('%s','%s','%s','%s','%s','%s','%s')"%(data[0],0,5,1,14,item['createtime'],0)
            save_data(insertevents)
            #这种情况原创视频价格必定为0
            insertvideo = "insert into PlatformIPAccountPrice(iPAcctountID, price, platformPriceNameID,statusIndex,source,createdTime,isOriginal) " \
                              "VALUES('%s','%s','%s','%s','%s','%s','%s')"%(data[0],0,4,1,14,item['createtime'],0)
            save_data(insertvideo)



