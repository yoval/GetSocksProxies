# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 13:18:58 2020

@author: Fuwenyue
"""
import requests,re,pymongo,json,time
from bs4 import BeautifulSoup

LocalProxy = {'https': 'https://127.0.0.1:1080'}
BilibiliIpUrl = 'https://api.live.bilibili.com/ip_service/v1/ip_service/get_ip_addr'
ProxyUrl = 'https://www.socks-proxy.net/'
Count=1
while True:
    print('第%s次'%str(Count))
    myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds049446.mlab.com:49446/proxy',retryWrites='false')
    mydb = myclient['proxy']
    ProxiesCol = mydb['socks']
    try:
        print('正在链接网站……')
        Resp = requests.get(ProxyUrl,proxies = LocalProxy)
        print('网站链接成功！')
    except:
        print('链接至网站失败！')
        continue
    Soup = BeautifulSoup(Resp.text, 'lxml')
    print('正在解析网页……')
    IpTable = Soup.select('#proxylisttable > tbody > tr')
    IpList = [re.findall('<td>(.*?)</td>',str(IpRow)) for IpRow in IpTable] 
    ProxiesList = [{'https':'%s://%s:%s'%(Ip[3],Ip[0],Ip[1])} for Ip in IpList]
    print('网页解析成功，共%d个代理！'%len(IpList))
    print('即将尝试用这些代理链接Bilibili……')
    n=0
    for Proxies in ProxiesList :
        try:
            n+=1
            Response = requests.get(BilibiliIpUrl ,proxies = Proxies, timeout=10)
            print('Bilibili链接成功！')
            IpJson = json.loads(Response.text)
            country = IpJson['data']['country']
            province = IpJson['data']['province']
            city = IpJson['data']['city']
            print('代理所在地区:%s'%country)
            Proxies['Location'] = country + province + city
            now = time.strftime('%Y{y}%m{m}%d{d} %H{H}%M{M}%S{S}').format(y='年',m='月',d='日',H='时',M='分',S='秒')
            Proxies['AddTime'] = now
            Proxies['LastUpdate'] = now
            print('将代理导入数据库……')
            ProxiesCol.insert_one(Proxies)
            print('导入成功！')
        except :
            print('第%d个代理链接Bilibili链接失败！'%n)
    Count+=1
    time.sleep(5)



