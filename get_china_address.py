# -*- coding: utf-8 -*-
import pymongo

__author__ = 'ly'


import requests

from lxml import etree

start_url = 'http://ldzl.people.com.cn/dfzlk/front/personProvince1.htm'
conn = pymongo.MongoClient('127.0.0.1', 27017, connect=False)
test = conn.china_district

def parse_district(url):
    url = 'http://ldzl.people.com.cn' + url
    resp = requests.get(url=url)
    content = resp.text
    tree = etree.HTML(content)
    provice = tree.xpath("//h3[@class='red']/text()")[0]
    all_district = tree.xpath("//ul[@class='clearfix list_a']/li/i[1]/text()")
    for district in all_district:
        if district.endswith('市'):
            dis = district.split('市')[0]
        else:dis = district
        data = {
            'provice': provice,
            'city': district,
            'dis': dis,
        }
        test.all_china_city.insert_one(data)
    
def main():
    response = requests.get(url=start_url)
    # content = response._content.decode("utf-8")
    content = response.text
    tree = etree.HTML(content)
    all_url = tree.xpath("//div[@class='fl']/ul/li/a/@href")
    from concurrent import futures
    # for url in all_url:
    #     parse_district(url)
    with futures.ThreadPoolExecutor(max_workers=10) as executer:
        executer.map(parse_district, all_url)
    


if __name__ == '__main__':
    main()