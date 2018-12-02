# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 02:00:53 2018

@author: fuwen
"""
import time,pymongo,requests,random,re,json
from bs4 import BeautifulSoup



BilibiliIpUrl = 'https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr'

while True:
    myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds029638.mlab.com:29638/socks_proxies')
    mydb = myclient['socks_proxies']
    ProxiesHub = mydb['ProxiesHub']
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
    ProxiesList = [{'https':'%s://%s:%s'%(Ip[3],Ip[0],Ip[1])} for Ip in IpList]
    y = ProxiesCol.insert_many(ProxiesList) 
    ProxiesHub.insert_many(ProxiesList)       
    print('保存ID: ',y.inserted_ids)        
    time.sleep(3600)