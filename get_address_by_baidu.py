# -*- coding: utf-8 -*-
import pymongo

__author__ = 'ly'

import os
import sys
import json
import urllib
import requests
from urllib.request import urlopen
from urllib.parse import quote

conn = pymongo.MongoClient('127.0.0.1', 27017, connect=False)
test = conn.huawei
# Api
def get_address(address):
    l = 0
    result = {
        'provice': '',
        'city': '',
        'district': '',
        'adress': ''
    }
    while 1:
        try:
            url = 'http://api.map.baidu.com/geocoder/v2/'
            # url = 'http://api.map.baidu.com/reverse_geocoding/v3/'
            # 输出类型
            output = 'json'
            # 密钥
            # ak = 'n1gSoDYwG5BHkHmBsFVjq6dYFUyahad1'
            ak = 'cspIkCfqY7sAqyONsWnNXpuYpgz8sGzF'
            # ak = 'ooGhUcqh0I6ZRBRXULGrbAVYGi9ptGBL1' # xiaoqiu
            # ak = '981d0z6iXaUWld0FxBq2ySq56o0VxSG3' # taoge
            
            # 为防止乱码，先进行编码
            address = quote(address)
            uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
            # 请求第一次获得经纬度
            req = requests.get(uri)
            # 返回为json,进行解析
            temp = json.loads(req.text)
            # 获得经纬度
            try:
                lat = temp['result']['location']['lat']
            except:
                break
            lng = temp['result']['location']['lng']
            # 请求第二次用经纬度去获得位置信息
            url_reback = 'http://api.map.baidu.com/geocoder/v2/?location=' + str(lat) + ',' + str(
                lng) + '&output=' + output + '&pois=1&ak=' + ak
            req_reback = requests.get(url_reback)
            data = json.loads(req_reback.text)
            result['provice'] = data['result']['addressComponent']['province']
            result['city'] = data['result']['addressComponent']['city']
            result['district'] = data['result']['addressComponent']['district']
            result['adress'] = data['result']['formatted_address']
            break
        except:
            l += 1
        if l == 3:
            break
    return result

def main():
    # 把公司地址解析具体地址并更新到huawei_address表中去
    # results = test.huawei_step3.find()
    results = test.huawei_address.find({'city': ''})
    for res in results:
        # if test.huawei_address.find_one({'_id': res['_id']}): continue
        data = get_address(res['developer'])
        # if provice and adress:
        if data['city']:
            res['provice'] = data['provice']
            res['city'] = data['city']
            res['district'] = data['district']
            res['address'] = data['adress']
            try:
                test.huawei_address.update_one({'_id': res['_id']}, {'$set': res}, upsert=True)
            except:
                pass
        else:
            pass
            # continue


if __name__ == '__main__':
    # main()
    get_address('咪咕音乐有限公司')