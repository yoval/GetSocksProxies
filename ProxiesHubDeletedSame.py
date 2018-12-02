# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 02:00:53 2018

@author: fuwen
"""
import time,pymongo,requests,random,re,json
from bs4 import BeautifulSoup


myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds029638.mlab.com:29638/socks_proxies')
mydb = myclient['socks_proxies']
ProxiesCol = mydb['ProxiesHub']

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
    

HKProxies = ProxiesCol.find({'Country':'HK'})
HKProxies = [Proxies for Proxies in HKProxies]