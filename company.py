# -*- encoding: utf-8 -*-
'''
    @文件    :company.py
    @说明    :获取网站链接以及基本数据
    @时间    :2020/09/03 11:41:00
    @作者    :jdh
    @版本    :1.0
'''
import re
import requests
import pymysql
from lxml import etree


def load_cookie(cookie_path):
    with open(cookie_path, 'r') as f:
        cookie = f.read()
    return cookie

HEADERS = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'cookie':load_cookie('./cookies.txt'),
}

class Spider(object):
    def __init__(self):
        self.base_search_url = 'https://www.qcc.com/search?key={}'
        
        self.HOST = 'locahost'
        self.USER = 'root'
        self.PASSWD = 'Fuck_you'
        self.DATABASE = 'company'
        self.qcc_base_url = 'https://www.qcc.com'

    def load_company(self, company_path):
        with open(company_path, 'r', encoding='utf-8') as f:
            companies = f.readlines()
        return companies
    
    def search_with_qichacha(self, keyword):
        search_url = self.base_search_url.format(keyword)
        resp = requests.get(search_url, headers=HEADERS)
        return resp.text
    
    def process_company(self, text, company_name):
        html = etree.HTML(text)
        
        origin_first_part = html.xpath('//*[@id="search-result"]/tr[1]/td[3]')[0].xpath('string(.)')
        first_part = re.sub('\n', 'AJDH', origin_first_part.replace(' ',''))

        try:
            reg_qcc_link = r'/firm/[A-Z0-9]{7}\.shtml'
            qcc_link = self.qcc_base_url + re.search(reg_qcc_link, text).group(0)
        except AttributeError as e:
            print(e)
            qcc_link = 'https://lovejdh.cn'

        try:
            reg_phone = r"电话：AJDH([\d-]{12,13})AJDH"
            phone = re.findall(reg_phone, first_part)[0] # 正则匹配电话
        except IndexError as e:
            print(e)
            self.debug_save(first_part, company_name)
            phone = '0000000000000'
        
        try:
            reg_email = r'(?:[0-9a-zA-Z_]+.)+@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}' #正则匹配出邮箱
            email = re.findall(reg_email, first_part)[0].replace('AJDH','')
        except IndexError:
            self.debug_save(first_part, company_name)
            email = '000@000.com'
        
        try:
            website = re.search('官网：AJDH([http://|www].*?)AJDH', first_part).group(0)
            website = re.sub('AJDH|官网：', '', website)
        except AttributeError:
            self.debug_save(first_part, company_name)
            website = 'http://lovejdh.cn'
        
        try:
            location = re.search('地址：(.*?)AJDH', first_part).group(0)
            location = re.sub('AJDH|地址：', '', location)
        except AttributeError:
            self.debug_save(first_part, company_name)
            location = '火星'
        
        data = company_name+' '+phone+' '+email+' '+website+' '+location+' '+qcc_link
        return data
    
    def connetc_mysql(self):
        """
            链接数据库
        """
        self.db = pymysql.connect(self.HOST, 
                                self.USER, 
                                self.PASSWD, 
                                self.DATABASE, 
                                charset='utf8')
        self.curson = self.db.cursor()
    
    def insert(self, item, is_basic=True):
        """
            插入
        """
        basic_insert_sql = "INSER INTO 'company' ('name', 'phone', 'email', 'wensite', 'location') VALUES (%s, %s, %s, %s, %s)"
        full_insert_sql = "INSER INTO company "
        sql = basic_insert_sql
        if not is_basic: sql = full_insert_sql
        sql = basic_insert_sql
        self.curson.execute(sql, item)
        self.db.commit()
    
    def save(self, line):
        line = line.replace('\n', '')
        with open('result.txt', 'a', encoding='utf-8') as f:
            f.write(line+'\n')
    
    def debug_save(self, text, name):
        name = name.replace('\n', '')
        path = 'debug/{}.txt'.format(name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    def run(self):
        companies = self.load_company('company.txt')
        for company in companies:
            search_result = self.search_with_qichacha(company)
            data = self.process_company(search_result, company)
            self.save(data)
            print('company {} seccessful'.format(company))
        

if __name__ == "__main__":
    spider = Spider()
    spider.run()