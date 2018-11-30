# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 10:24:14 2018

@author: fuwen
"""
import pymongo,requests,json,time


BilibiliIpUrl = 'https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr'
myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds029638.mlab.com:29638/socks_proxies')
mydb = myclient['socks_proxies']
ProxiesCol = mydb['Proxies']
ProxiesList = ProxiesCol.find({},{ "_id": 0, "https": 1}).sort('update',-1).limit(30)
ProxiesList = [Proxies for Proxies in ProxiesList]

'''
for Proxies in ProxiesList :
    Proxies = {'https':Proxies['https']}
    time.sleep(2)
    try :
        Response = requests.get(BilibiliIpUrl ,proxies = Proxies, timeout=10)
        IpJson = json.loads(Response.text)
        country = IpJson['data']['country']
        province = IpJson['data']['province']
        city = IpJson['data']['city']
        location = country + province + city
        print(location)
        d = {'https':Proxies['https']}
        t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        x = ProxiesCol.update_one(d, { '$set': {'location': location,'update':t}})
        print(x.modified_count, "文档已修改")
    except Exception as e:
        d = {'https':Proxies['https']}
        y = ProxiesCol.delete_one(d)
        print('无效代理 :', y.deleted_count,"个文档已删除")
'''