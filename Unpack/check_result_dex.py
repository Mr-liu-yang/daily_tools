# -*- coding: utf-8 -*-
__author__ = 'ly'

import os

root_path = os.path.dirname(os.path.abspath(__name__))

result_path = os.path.join(root_path, 'result')

def check_result_dex():
    for apk in os.listdir(result_path):
        result_dex_path = os.path.join(result_path, apk, 'result.dex')
        print(result_dex_path)
        
        flag = False
        with open(result_dex_path, 'rb+') as ff:
            first_line = ff.readline().strip()
            print(first_line)
            if first_line:
                first_line = bytes.decode(first_line)
                if not first_line.startswith('dex'):
                    print(first_line)
                    flag = True
                else:
                    print('startswith dex')
                    pass
        if flag:
            __first_line_switch(result_dex_path)
        pass

def __first_line_switch(dst_file, s=1):
    # 默认替换第一行内容
    with open(dst_file, 'rb+') as ff:
        lines = ff.readlines()
    with open(dst_file, 'wb+') as f:
        n = 0
        if s == 1:
            for line in lines:
                line = b'dex\n'
                # line = line.strip().replace(line, b'dex')
                f.write(line)
                n += 1
                break
            for i in range(n, len(lines)):
                f.write(lines[i])
    print('switch success!')
    
def main():
    check_result_dex()
    
if __name__ == '__main__':
    main()