# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 00:50:30 2020

@author: Fuwenyue
"""
import requests,time,pymongo
from bs4 import BeautifulSoup

LocalProxy = {'https': 'https://127.0.0.1:1080'}
ProxyUrl = 'https://free-proxy-list.net/'
BilibiliIpUrl = 'http://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr'

def InsertMongoDB(ProxyData):
    myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds049446.mlab.com:49446/proxy',retryWrites='false')
    mydb = myclient['proxy']
    ProxiesCol = mydb['http']
    x = ProxiesCol.insert_one(ProxyData)
    print('数据库ID为：',x.inserted_id)

def GetProxyData():
    while True:
        print('Connecting...')
        Resp = requests.get(ProxyUrl,proxies = LocalProxy)
        print('链接成功！')
        break
    Soup = BeautifulSoup(Resp.text, 'lxml')
    IpTables = Soup.select('#proxylisttable > tbody > tr')
    print('此次共有%s个代理'%len(IpTables))
    for IpTable in IpTables:
        global ProxyData
        ProxyData = {'Proxy':{'IPadress':IpTable.contents[0].string,
                              'Prot':IpTable.contents[1].string},
                     'Location':IpTable.contents[3].string,
                     'Anonymity' : IpTable.contents[4].string,
                     'Google' : IpTable.contents[5].string,
                     'Https' : IpTable.contents[6].string,
                     'AddTime':'',
                     'Lastchecktime':''
                     }
        Proxy = {'http': 'http://' + ProxyData['Proxy']['IPadress']+':'+ ProxyData['Proxy']['Prot']}
        try:
            print('尝试用此代理链接Bilibili……')
            Response = requests.get(BilibiliIpUrl ,proxies = Proxy, timeout=10)
            print('代理有效！解析返回信息！')
        except:
            print('代理无效！跳过……')
            continue
        try:
            IpJson = Response.json()
            print('解析成功！')
        except:
            print('解析失败！跳过')
            continue
        country = IpJson['data']['country']
        province = IpJson['data']['province']
        city = IpJson['data']['city']
        ProxyData['Location'] = country + province + city
        now = time.strftime('%Y{y}%m{m}%d{d} %H{H}%M{M}%S{S}').format(y='年',m='月',d='日',H='时',M='分',S='秒')
        ProxyData['AddTime'] = now
        ProxyData['Lastchecktime'] = now
        InsertMongoDB(ProxyData)

if __name__=='__main__' :
    while True :
        GetProxyData()
        time.sleep(60)


