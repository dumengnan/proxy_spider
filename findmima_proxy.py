#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from util.url_request import reqDirect

def parse_content(html_content):
    soup = BeautifulSoup(html_content)
    content = soup.find('pre')
    update_time = soup.select('h4')[4].get_text()
    proxy_content = content.get_text()

    print 'latest update in : \n' + update_time
    print 'the http proxy :\n' + proxy_content

def main():
    start_url = 'http://vpn.hn-seo.com/'
    html_content = reqDirect(start_url)

    parse_content(html_content)

if __name__ == '__main__':
    main()
