# -*- encoding: utf-8 -*-
'''
    @文件    :company_website.py
    @说明    :对网站进行遍历获取人员
    @时间    :2020/09/03 15:57:27
    @作者    :jdh
    @版本    :1.0
'''
# 标准库
import re
import requests

# 第三方库

# 自定义模块

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
}
keywords = ['expert', 'zj']

class WebSpider(object):
    def __init__(self):
        urls = {}
        pass

    def connect(self, web):
        if not web.startswith('http'):
            web = 'http://'+ web
        resp = requests.get(web, headers=HEADERS)
        return resp.text
    
    def process(self, text):
        re.findall('/(.*?)\.[jsp|php|html|jhtml]', text)
        pass
    

if  __name__ == "__main__":
    web_site_list = ['www.smedi.com',
                    'http://www.cjwsjy.com.cn/',
                    'http://www.bjucd.com',
                    'http://www.lpec.com.cn',
                    'http://www.crdc.com',
                    'http://www.cnwg.com.cn/',]
    
    webspider = WebSpider()
    webspider.connect(web_site_list[0])