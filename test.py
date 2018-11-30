# -*- coding: utf-8 -*-
"""
URI1 = 'mongodb://fuwenyue:pass4Top@ds059316.mlab.com:59316/my_db_1'
URI2 = 'mongodb://fuwenyue:pass4Top@ds119734.mlab.com:19734/my_db_2'
URI3 = 'mongodb://fuwenyue:pass4Top@ds119164.mlab.com:19164/my_db_3'
URI4 = 'mongodb://fuwenyue:pass4Top@ds038888.mlab.com:38888/my_db_4'
URI5 = 'mongodb://fuwenyue:pass4Top@ds044587.mlab.com:44587/my_db_5'
URI6 = 'mongodb://fuwenyue:pass4Top@ds026018.mlab.com:26018/my_db_6'
URI7 = 'mongodb://fuwenyue:pass4Top@ds029638.mlab.com:29638/socks_proxies'
"""
from bs4 import BeautifulSoup
import pymongo,requests,re

myclient  = pymongo.MongoClient("mongodb://fuwenyue:pass4Top@ds059316.mlab.com:59316/my_db_1")
mydb = myclient['my_db_1']
ProxiesCol = mydb["Proxies"]

Daili = [{}, {'https': 'Socks5://144.34.181.207:1080'},{'https': 'Socks5://104.224.132.132:1080'}]
ProxiesList = []
try:
    Response = requests.get('https://www.socks-proxy.net/',proxies = Daili[0])
except Exception as e:
    print(e)
    try:
        Response = requests.get('https://www.socks-proxy.net/',proxies = Daili[1])
    except Exception as e:
        print(e)
        try:
            Response = requests.get('https://www.socks-proxy.net/',proxies = Daili[2])
        except Exception as e:
            print(e)

Response.encoding = 'utf-8'
Html = Response.text
Soup = BeautifulSoup(Html, 'lxml')
IpTable = Soup.select('#proxylisttable > tbody > tr')
for IpRow in IpTable:
    Ip = re.findall('<td>(.*?)</td>',str(IpRow))
    proxies =  {'https': '%s://%s:%s'%(Ip[3],Ip[0],Ip[1])}
    ProxiesList.append(proxies)
    
print('共获取%s条代理，即将进行检测'%len(ProxiesList))
U_ProxiesList = []
No=0
for Proxies in ProxiesList :
    No+=1
    try :    
        Response = requests.get('https://www.58.com/',proxies = Proxies, timeout=10)
        U_ProxiesList.append(Proxies)
        print('代理有效，已保留(%d/%d)'%(No,80))
        y = ProxiesCol.insert_one(Proxies)
        print(y.inserted_id)
    except Exception :
        ProxiesList.remove(Proxies)
        print('代理无效，已删除(%d/%d)'%(No,80))
print('代理池生成完毕，共获取%s条有效代理'%len(U_ProxiesList))
return U_ProxiesList    







    
