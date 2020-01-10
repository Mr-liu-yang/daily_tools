# -*- coding: utf-8 -*-
import os
import sys
import shutil

__author__ = 'ly'

import subprocess

def deal_with_apk(origin_file):
    cwd = os.getcwd()
    _set = os.path.split(origin_file)
    apk_table = _set[0]
    apk_name = _set[1]
    deal_apk_name = apk_name.split('.apk')[0]
    os.chdir(apk_table)
    command = 'unzip {} -d {}'.format(apk_name, deal_apk_name)  # com.anzhui.apk , com.anzhui
    process = __run_command(command)
    process.communicate()
    process.terminate()
    os.remove(origin_file)
    
    os.chdir(os.path.join(apk_table, deal_apk_name))
    command = 'zip -q -r {} *'.format(apk_name)
    process = __run_command(command)
    process.communicate()
    process.terminate()
    
    command = 'mv {} {}'.format(apk_name, apk_table)
    process = __run_command(command)
    process.communicate()
    process.terminate()
    shutil.rmtree(os.path.join(apk_table, deal_apk_name))
    os.chdir(cwd)
    
def __run_command(command):
    print(command)
    return subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)


def main():
    deal_with_apk(sys.argv[1])
    pass

if __name__ == '__main__':
    main()