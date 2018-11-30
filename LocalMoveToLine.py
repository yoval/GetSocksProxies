# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 13:10:11 2018

@author: fuwen
"""
import pymongo,requests,json,time


BilibiliIpUrl = 'https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr'
LocalClient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
LocalDB = LocalClient["WuBaTongcheng"]# 连接数据库
LocalCol = LocalDB["Proxies"]# 连接数据表
LineClient = pymongo.MongoClient("mongodb://fuwenyue:pass4Top@ds029638.mlab.com:29638/socks_proxies")
LineDB = LineClient["socks_proxies"]
LineCol = LineDB["Proxies"]
ItemList = LocalCol.find({},{ "_id": 0})
ProxiesList = LocalCol.find({},{ "_id": 0, "https": 1})

for Proxies in ProxiesList :
    try :
        Response = requests.get(BilibiliIpUrl ,proxies = Proxies, timeout=10)
        IpJson = json.loads(Response.text)
        country = IpJson['data']['country']
        print(country)
        province = IpJson['data']['province']
        city = IpJson['data']['city']
        location = country + province + city
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        Proxies['location'] = location
        Proxies['creattime'] = t        
        x = LineCol.insert_one(Proxies)
        print('成功添加至线上。ID ：',x.inserted_id)
        d = {'https':Proxies['https']}
        y = LocalCol.delete_one(d)
        print('本地数据库', y.deleted_count, '个文档已删除')
    except :
        d = {'https':Proxies['https']}
        y = LocalCol.delete_one(d)
        print('error，本地数据库', y.deleted_count, '个文档已删除')

