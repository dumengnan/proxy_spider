#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from util.url_request import reqByHttpProxy
from util.data_storage import DataSaveToMongo
from util.proxy_item import ProxyItem



def parse_content(html_content):
    soup = BeautifulSoup(html_content)
    content = soup.find('pre')
    update_time = soup.select('h4')[4].get_text()
    proxy_content = content.get_text()

    print 'latest update in : \n' + update_time
    
    data_save = DataSaveToMongo()
    data_save.saveOneToDb({'update_time':update_time})

    for proxy_url in proxy_content.split('\r\n'): 
        data = ProxyItem(proxy_url," ", 'HTTP')
        data_save.saveToDb(data)
        
def main():
    start_url = 'http://vpn.hn-seo.com/'
    html_content = reqByHttpProxy(start_url)

    parse_content(html_content)

if __name__ == '__main__':
    main()
