# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 10:24:14 2018

@author: fuwen
"""
import pymongo,requests,json

while True :

    BilibiliIpUrl = 'https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr'
    myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds029638.mlab.com:29638/socks_proxies')
    mydb = myclient['socks_proxies']
    ProxiesCol = mydb['Proxies']
    ProxiesList = ProxiesCol.find({},{ "_id": 0, "https": 1})
    Count = ProxiesCol.find().count()
    print('当前共有%d条记录'%Count)
    for Proxies in ProxiesList :
        time.sleep(2)
        try :
            Response = requests.get(BilibiliIpUrl ,proxies = Proxies, timeout=10)
            IpJson = json.loads(Response.text)
            country = IpJson['data']['country']
            province = IpJson['data']['province']
            city = IpJson['data']['city']
            print('代理地区 :',country,province,city)
        except :
            ProxiesCol.delete_one(Proxies)
            Count = ProxiesCol.find().count()
            print('代理不可用，已删除 当前剩余%d条记录'%Count)
 
    time.sleep(36000)