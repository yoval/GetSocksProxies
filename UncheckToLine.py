# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 03:59:04 2018

@author: fuwen
"""

import time,pymongo,requests,random,re,json

BilibiliIpUrl = 'https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr'
myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds029638.mlab.com:29638/socks_proxies')
mydb = myclient['socks_proxies']
ProxiesCol = mydb['ProxiesNotChecked']
ProxiesList = ProxiesCol.find({},{ "_id": 0, "https": 1})
ProxiesList = [Proxies for Proxies in ProxiesList]
CheckedCol = mydb["Proxies"]

for Proxies in ProxiesList :
    try :
        Response = requests.get(BilibiliIpUrl ,proxies = Proxies, timeout=10)
        d = {'https':Proxies['https']}
        y = ProxiesCol.delete_one(d)
        print('有效代理 :', y.deleted_count,"个文档已删除")
        time.sleep(2)
    except :
        d = {'https':Proxies['https']}
        y = ProxiesCol.delete_one(d)
        print('无效代理 :', y.deleted_count,"个文档已删除")
        time.sleep(2)
        continue
    IpJson = json.loads(Response.text)
    country = IpJson['data']['country']
    province = IpJson['data']['province']
    city = IpJson['data']['city']
    location = country + province + city
    Proxies['location'] = location
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    Proxies['creattime'] = t
    Proxies['update'] = t
    y = CheckedCol.insert_one(Proxies)
    print('保存ID : ',y.inserted_id)
