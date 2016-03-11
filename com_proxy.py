#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import urllib2
from bs4 import BeautifulSoup
from util.url_request import reqByHttpProxy
from urlparse import urljoin

from util.proxy_item import ProxyItem
from util.data_storage import DataSaveToMongo

def parse_html(url_address):
    html_content = reqByHttpProxy(url_address)

    soup = BeautifulSoup(html_content)
    for table in soup.find_all('table',border=1):
        for table_content in table.find_all('tr')[5:]:
            i = 0 
            proxy_ip = ''
            proxy_port = ''
            proxy_type = ''
            proxy_locate = ''
            data_save = DataSaveToMongo()
            for content in table_content.find_all('td'):
                if i == 0:
                    print 'order num : ' + content.get_text()
                elif i == 1:
                    proxy_ip = content.get_text()
                    print 'Ip : ' + content.get_text()
                elif i == 2:
                    proxy_port = content.get_text()
                    print 'Port : ' + content.get_text()
                elif i == 3:
                    proxy_type = content.get_text()
                    print 'Proxy Type: '+ content.get_text()
                elif i == 4:
                    proxy_locate = content.get_text()
                    print 'Locate :' + content.get_text()
                i = i + 1
            proxy_url = proxy_ip + ':' + proxy_port
            
            proxy = ProxyItem(proxy_url, proxy_locate, proxy_type)
            data_save.saveToDb(proxy)
                            

def get_next_page(url_address):
    html_content = reqByHttpProxy(url_address)
    soup = BeautifulSoup(html_content)
    
    next_page = soup.find_all('table',border=1)[1]
    for url in next_page.find_all('a'):
        next_url = urljoin(url_address,url['href'])
        parse_html(next_url)

def main():
    start_time = time.time()
    start_url = 'http://www.proxy.com.ru'
    get_next_page(start_url)
    end_time = time.time()

    print 'Cost Time is : %s s'%(end_time - start_time)

if __name__ == '__main__':
    main()
