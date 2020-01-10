#!/usr/bin/env python
# encoding: utf-8

import json,xlwt
import sys

def writeM():
    title = ['appid',  '名称', 'MD5', 'version_code',  '开发者', '下载量', '介绍']
    book = xlwt.Workbook() # 创建一个excel对象
    sheet = book.add_sheet('Sheet1',cell_overwrite_ok=True) # 添加一个sheet页
    for i in range(len(title)): # 循环列
        sheet.write(0,i,title[i]) # 将title数组中的字段写入到0行i列中
    with open('./beijing.json') as f:
        for index, line in enumerate(f.readlines()):
            index += 1
            line = json.loads(line.replace('\n', ''))
            # import pdb;pdb.set_trace()
            new_line = {
                    'appid': line.get('appid', ''),
                    'name': line.get('name', ''),
                    'hash': line.get('hash', ''),
                    'version_code': line.get('version_code', ''),
                    'developer': line.get('developer', ''),
                    'download_count': line.get('download_count', ''),
                    'description': line.get('description', '')
                    }
            for i, j_ in enumerate(new_line):
                try:
                    sheet.write(index, i, new_line[j_])
                except:
                    print(new_line)
                    # import pdb;pdb.set_trace()
                    if new_line['download_count'].get('$numberLong', ''):
                        new_line['download_count'] = int(new_line['download_count']['$numberLong'])
                    try:
                        sheet.write(index, i, new_line[j_])
                    except Exception as e:
                        print(e)

    book.save(sys.argv[1])

if __name__ == '__main__':
    writeM()
