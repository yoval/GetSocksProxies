# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 15:02:28 2018
curl --socks4 131.196.143.123:50489 http://ifcfg.co
@author: fuwen
"""

from bs4 import BeautifulSoup
import pymongo,requests,re,random,time,json

BilibiliIpUrl = 'https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr'
MyProxiesList = [{}, {'https': 'Socks5://144.34.181.207:1080'},{'https': 'Socks5://104.224.132.132:1080'}]

while True :
    myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds029638.mlab.com:29638/socks_proxies')
    mydb = myclient['socks_proxies']
    ProxiesCol = mydb['Proxies']
    while True :
        print('正在尝试连接……')
        try :
            Response = requests.get('https://www.socks-proxy.net/',proxies = MyProxiesList[random.randint(0,2)],timeout = 15)
            print('连接成功！')
            break
        except Exception :
            print('连接失败，即将重新尝试连接。')
    
    Soup = BeautifulSoup(Response.text, 'lxml')       
    IpTable = Soup.select('#proxylisttable > tbody > tr')
    IpList = [re.findall('<td>(.*?)</td>',str(IpRow)) for IpRow in IpTable]                      
    ProxiesList = [{'https':'%s://%s:%s'%(Ip[3],Ip[0],Ip[1])} for Ip in IpList]
    
    for Proxies in ProxiesList :
        try :
            Response = requests.get(BilibiliIpUrl ,proxies = Proxies, timeout=10)
            IpJson = json.loads(Response.text)
            country = IpJson['data']['country']
            province = IpJson['data']['province']
            city = IpJson['data']['city']
            Proxies['location'] = country + province + city
            x = ProxiesCol.insert_one(Proxies)
            print('ProxiesSaved')
    
        except Exception :
            print('ProxiesError')
    time.sleep(3600)