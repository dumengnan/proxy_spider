#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2 
import pymongo
from threadwork import ThreadPool

proxy_flag = 1
alive_count = 0

class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        global proxy_flag
        proxy_flag = 0
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg,headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_302


# 通过使用代理ip打开一个url,通过返回码判断代理是否可用
def Test_ProxyStatu(proxy_ip, collection):
    try:
        proxy = urllib2.ProxyHandler({'http':proxy_ip['proxy_url']})

        cookieprocessor = urllib2.HTTPCookieProcessor()

        opener = urllib2.build_opener(MyHTTPRedirectHandler,cookieprocessor)
        opener.add_handler(proxy)

        urllib2.install_opener(opener)

        response = urllib2.urlopen('http://www.woaidu.org/sitemap_1.html',timeout=3)
        
        if response.getcode() == 200 and proxy_flag == 1: 
	    global alive_count
	    alive_count = alive_count+1  
            print proxy_ip
        else:
            collection.remove({'proxy_url':proxy_ip['proxy_url']})
    
    except Exception,e:
        collection.remove({'proxy_url':proxy_ip['proxy_url']})
        print 'except reason ' + str(e.args)

def main():
    SingleMONGODB_SERVER="localhost"
    SingleMONGODB_PORT=27017
    MONGODB_DB="proxyip_data"
    MONGODB_COLLECTION="proxyip_collection"

    try:
        connection =  pymongo.MongoClient(
            SingleMONGODB_SERVER,
            SingleMONGODB_PORT
        )

        db = connection[MONGODB_DB]
        collection = db[MONGODB_COLLECTION]

        pool = ThreadPool(10)
        for proxy in collection.find({"proxy_type":"HTTP"}):
            proxy_dict = {}
            global proxy_flag
            proxy_flag = 1
            proxy_dict['proxy_url'] = proxy['proxy_url'] 
	    # 按顺序检测所有的代理ip是否可用，如果不可用，将其从数据库中移除
            pool.add_task(Test_ProxyStatu,proxy_dict, collection)

        pool.wait_completion()
    except Exception,e:
        print 'exception error ' + e.message

if __name__ == '__main__':
    main()
    print 'alive proxy have ' + str(alive_count)
    #print 'return code is ' + str(Test_ProxyStatu({
     #   'proxy_url':"http://111.47.13.2:80",'user_pass':None}))
