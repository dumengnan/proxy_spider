#!/usr/bin/python
# -*- coding:utf-8 -*-

import socket 
import socks

from select_useragent import selectUserAgent

def reqByProxy(url_address):
    SOCKS5_PROXY_HOST = '127.0.0.1'
    SOCKS5_PROXY_PORT = 1080

    default_socket = socket.socket

    socks.set_default_proxy(socks.SOCKS5, SOCKS5_PROXY_HOST, SOCKS5_PROXY_PORT)
    socket.socket = socks.socksocket

    import urllib2
    req = urllib2.Request(url_address)
    user_agent = selectUserAgent()
    req.add_header('User-Agent',user_agent)
    
    return urllib2.urlopen(req, timeout=10).read()

def reqDirect(url_address):
    import urllib2
    req = urllib2.Request(url_address)
    user_agent = selectUserAgent()
    req.add_header('User-Agent',user_agent)
    html_content = urllib2.urlopen(req, timeout=10).read()

    return html_content

def reqByHttpProxy(url_address):
    import urllib2
    proxy = urllib2.ProxyHandler({'http':'127.0.0.1:8118'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    
    req = urllib2.Request(url_address)
    user_agent = selectUserAgent()
    req.add_header('User-Agent', user_agent)

    html_content = urllib2.urlopen(req,timeout=10).read()

    return html_content
