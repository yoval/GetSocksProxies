# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 22:12:16 2020

@author: Fuwenyue
"""
import requests,pymongo,time

Con=0
BilibiliIpUrl = 'https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr'
myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds049446.mlab.com:49446/proxy',retryWrites='false')
mydb = myclient['proxy']
ProxiesCol = mydb['socks']
for i in range(5):
    ProxiesList = ProxiesCol.find({},{ "_id": 0, "https": 1}).sort('update',-1)
    ProxiesList = [Proxies for Proxies in ProxiesList]
    print('数据库中有%s个代理，即将进行重复删除……'%len(ProxiesList))
    Con+=1
    print('正在进行第%s次重复查询'%Con)
    for Proxies in ProxiesList :
        if ProxiesList.count(Proxies) > 1 :
            y = ProxiesCol.delete_one(Proxies)
            ProxiesList.remove(Proxies)
            print( y.deleted_count,"个重复文档已删除")
print('已完成重复查询，即将进行代理验证……')
for Proxies in ProxiesList:
    try:
        Response = requests.get(BilibiliIpUrl ,proxies = Proxies, timeout=10)
    except:
        y = ProxiesCol.delete_one(Proxies)
        print('已删除', y.deleted_count,"个已失效代理")
        continue
    now = time.strftime('%Y{y}%m{m}%d{d} %H{H}%M{M}%S{S}').format(y='年',m='月',d='日',H='时',M='分',S='秒')
    ProxiesCol.update_one(Proxies, { '$set': { "LastUpdate": now } })
    print('代理有效，已更新代理验证日期……')
