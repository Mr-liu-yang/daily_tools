#!/usr/bin/env python
# encoding: utf-8

import time
import requests

url = 'http://192.168.30.74:5000/api/task/get_task_check_report'
# url = 'http://127.0.0.1:5000/api/project/add_cached_profile'

s = requests.session()
login_url = 'http://192.168.30.74:5000/api/login'
s.post(login_url, json={'username': "admin", 'password': "admin"})
'''
data = {
    'task_id': 'ad60d20b01a84367bcb3907199fb5088',
    'status': 1,
    "plugin_id": "v01",
    "path": "/home/pangu/d/work/device_data/20180607/7d8cbe764ebb4e18924945f300b1fda4/v02",
    "payload": {},
    "err_msg": ""
}
'''
data = {
        'task_id': '98949be6d6d44662addec9329dbbbc21'
        }

time.sleep(1)
r = s.get(url, params=data)
print(r.content)

