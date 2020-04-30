# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 02:55:32 2020

@author: Fuwenyue
"""
import pymongo
myclient  = pymongo.MongoClient('mongodb://fuwenyue:pass4Top@ds049446.mlab.com:49446/proxy',retryWrites='false')
mydb = myclient['proxy']
ProxiesCol = mydb['http']

