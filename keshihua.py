# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 16:06:15 2020

@author: Fuwenyue
"""
from pyecharts.globals import ThemeType
import pyecharts.options as opts
from pyecharts.charts import Bar
import pymongo

myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds049446.mlab.com:49446/proxy',retryWrites='false')
mydb = myclient['proxy']
ProxiesCol = mydb['socks']
ProxiesList = ProxiesCol.find({},{ "_id": 0, "Location": 1}).sort('update',-1)
ProxiesList = [i for i in ProxiesList]
LocationList = [Proxies['Location'] for Proxies in ProxiesList]
LocationList = [Location[0:2] for Location in LocationList]
dic = {}
xaxis = list(set(LocationList))

for x in xaxis:
    y = LocationList.count(x)
    dic[x] = y

l = list(tuple(dic.items()))
sorted_l = sorted(l,key=lambda t:t[1],reverse=True)
xaxis = [x[0] for x in sorted_l][:10]
yaxis = [x[1] for x in sorted_l][:10]

bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
    .add_xaxis(xaxis)
    .add_yaxis("Socks", yaxis)
    .set_global_opts(title_opts=opts.TitleOpts(title="SOCKS地域分布"))#设置标题
    )


#bar.render_notebook()
