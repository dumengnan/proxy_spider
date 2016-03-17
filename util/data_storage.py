#!/usr/bin/python
# -*- coding:utf-8 -*-

from proxy_item import ProxyItem
import pymongo

class DataSaveToMongo:

    def __init__(self):
        connection = pymongo.MongoClient(
                "localhost",
                27017
                )
        db = connection['proxyip_data']
        self.collection = db['proxyip_collection']

    def saveToDb(self,item):
        self.collection.insert(item.__dict__)

    def saveOneToDb(self, dict_data):
        self.collection.insert(dict_data)

if __name__ == '__main__':
    proxy_url = 'test'
    proxy_locate = 'Japen'
    proxy_type = 'http'
    proxy_ip = ProxyItem(proxy_url,proxy_locate,proxy_type)
    data_save = DataSaveToMongo()
    data_save.saveToDb(proxy_ip)
