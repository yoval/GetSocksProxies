# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 02:00:53 2018

@author: fuwen
"""
import time,pymongo,requests,random,re,json
from bs4 import BeautifulSoup


while True:
    myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds029638.mlab.com:29638/socks_proxies')
    mydb = myclient['socks_proxies']
    ProxiesHub = mydb['ProxiesHub']
    SavedProxiesList = ProxiesHub.find({},{ "_id": 0, "https": 1}).sort('update',-1)
    SavedProxiesList = [Proxies for Proxies in SavedProxiesList]
    while True :
        print('正在尝试连接……')
        try :
            Response = requests.get('https://www.socks-proxy.net/', timeout = 10)
            print('连接成功！')
            break
        except Exception :
            print('连接失败，即将重新尝试连接。')
            time.sleep(2)
    Soup = BeautifulSoup(Response.text, 'lxml')       
    IpTable = Soup.select('#proxylisttable > tbody > tr')
    IpList = [re.findall('<td>(.*?)</td>',str(IpRow)) for IpRow in IpTable]                   
    ProxiesList = [{'https':'%s://%s:%s'%(Ip[3],Ip[0],Ip[1]),'Country':Ip[2]} for Ip in IpList]
    for Proxies in ProxiesList :
        PROXIES = {'https':Proxies['https']}
        if PROXIES not in SavedProxiesList :
            x = ProxiesHub.insert_one(Proxies)
            print('保存ID :',x.inserted_id)
        else :
            print('代理已存在，跳过')
#    break
    time.sleep(300)
    
    