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

while True:
    ProxiesList = ProxiesCol.find({},{ "_id": 0, "https": 1}).sort('update',-1)
    ProxiesList = [Proxies for Proxies in ProxiesList]
    PROXIESLIST = []
    SAMELIST = []
    for Proxies in ProxiesList :
        if Proxies not in PROXIESLIST :
            PROXIESLIST.append(Proxies)
    for Proxies in PROXIESLIST :
        if ProxiesList.count(Proxies) > 1 :
            SAMELIST.append(Proxies)
    for Proxies in SAMELIST :
        y = ProxiesCol.delete_one(Proxies)
        print( y.deleted_count,"个重复文档已删除")
    time.sleep(2)
    print( "————————————")
    if SAMELIST==[]:
        break
        
ProxiesList = ProxiesCol.find().sort('update',1)

for Proxies in ProxiesList :
    LastUpdate = Proxies['update']
    Proxies = {'https':Proxies['https']}
    print('上次更新时间 : ',LastUpdate)
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
        print(x.modified_count, "文档已更新")
    except Exception as e:
        d = {'https':Proxies['https']}
        y = ProxiesCol.delete_one(d)
        print('无效代理 :', y.deleted_count,"个文档已删除")
    print('------')