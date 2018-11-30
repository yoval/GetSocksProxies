# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 16:10:14 2018

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
    time.sleep(2)
    try :
        Response = requests.get(BilibiliIpUrl ,proxies = Proxies, timeout=10)
        IpJson = json.loads(Response.text)
        country = IpJson['data']['country']
        province = IpJson['data']['province']
        city = IpJson['data']['city']
        print('有效代理 :',country)
    except :
        d = {'https':Proxies['https']}
        y = LineCol.delete_one(d)
        print('无效代理 :', y.deleted_count,"个文档已删除")
