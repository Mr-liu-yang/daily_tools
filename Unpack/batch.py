import os
import traceback
import copy
import time
import sys
import subprocess
from logging import handlers
from multiprocessing import Pool, Process, Manager
import shutil
import logging
import datetime


root_path = os.path.dirname(os.path.abspath(__name__))
LOG_DIR = os.path.join(root_path, 'log')
log_name = 'unpack_apk.log' + datetime.datetime.now().strftime("%Y%m%d")
logger = logging.getLogger(__name__)
formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
filehandler = handlers.RotatingFileHandler(os.path.join(LOG_DIR, log_name))
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)
logger.setLevel(logging.INFO)

failed_apk_path = os.path.join(root_path, 'failed_apk.txt')
success_result_path = os.path.join(root_path, 'result')
failed_result_path = os.path.join(root_path, 'result_failed')

class unpack2:
    def __init__(self, serialno, apk_filepath):
        self.__inited = False
        file_dir = os.path.abspath(__file__)
        self.__path = os.path.dirname(file_dir)
        self.__apk_filepath = os.path.abspath(apk_filepath)
        pullname = os.path.split(self.__apk_filepath)[1].rsplit(".", 1)[0]
        self.__pullname = pullname  # 包名
        self.__result_failed = os.path.join(self.__path, 'result_failed')
        pull_dst = os.path.join(self.__path, "result")
        self.__pull_dst = os.path.join(pull_dst, pullname)
        if not os.path.exists(self.__pull_dst):
            os.makedirs(self.__pull_dst)
        self.__build_dex = os.path.join(self.__path, "build_dex")
        self.__adb_path = os.path.join(self.__path, "adb")
        self.__adb_command = self.__adb_path + " -s " + serialno + " "
        self.__packagename, self.__activity_name = self.__get_package_and_activity(apk_filepath)
        self.__packagepath = "/data/data/" + self.__packagename
        self.__unpackfilepath = self.__packagepath + "/dexInfos"
        # self.__logfile = os.path.join(self.__path, "log.txt")
        print(serialno, apk_filepath, self.__packagename)
        self.__inited = True

    def __del__(self):
        if not self.__inited:
            return
        self.__force_stop()
        self.__uninstall_apk()

    def __run_command(self, command):
        print(command)
        return subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)


    def __get_package_and_activity(self, apk_filepath):
        aapt = os.path.join(self.__path, "aapt")
        command = aapt + " d badging " + apk_filepath + " | awk -F \" |\'|:\" \'{if($1 == \"package\")print $4; if($1 == \"launchable-activity\")print $4;}\' "
        process = self.__run_command(command)
        lines = process.stdout.readlines()
        try:
            package_name = lines[0].strip().decode()
            activity_name = lines[1].strip().decode()
        except Exception as e:
            process.terminate()
            # unzip and zip
            self.__deal_with_apk(apk_filepath)
            aapt = os.path.join(self.__path, "aapt")
            command = aapt + " d badging " + apk_filepath + " | awk -F \" |\'|:\" \'{if($1 == \"package\")print $4; if($1 == \"launchable-activity\")print $4;}\' "
            process = self.__run_command(command)
            lines = process.stdout.readlines()
            try:
                package_name = lines[0].strip().decode()
                activity_name = lines[1].strip().decode()
            except Exception as e:
                process.terminate()
                # move to failed result
                self.__move_to_failed_result()
                raise
        return package_name, activity_name
    
    def __move_to_failed_result(self):
        if os.path.exists(self.__pull_dst):
            command = 'mv {} {}'.format(self.__pull_dst, self.__result_failed)
            process = self.__run_command(command)
            process.communicate()
            process.terminate()
        else:
            os.makedirs(os.path.join(self.__result_failed, self.__pullname))

    def __deal_with_apk(self, origin_file):
        cwd = os.getcwd()
        _set = os.path.split(origin_file)
        apk_table = _set[0]
        apk_name = _set[1]
        deal_apk_name = apk_name.split('.apk')[0]
        os.chdir(apk_table)
        command = 'unzip {} -d {}'.format(apk_name, deal_apk_name)  # com.anzhui.apk , com.anzhui
        process = self.__run_command(command)
        process.communicate()
        process.terminate()
        os.remove(origin_file)
    
        os.chdir(os.path.join(apk_table, deal_apk_name))
        command = 'zip -q -r {} *'.format(apk_name)
        process = self.__run_command(command)
        process.communicate()
        process.terminate()
    
        command = 'mv {} {}'.format(apk_name, apk_table)
        process = self.__run_command(command)
        process.communicate()
        process.terminate()
        shutil.rmtree(os.path.join(apk_table, deal_apk_name))
        os.chdir(cwd)

    def __launch_start(self):
        command = self.__adb_command + " shell am start -n " + self.__packagename + "/" + self.__activity_name
        process = self.__run_command(command)
        process.communicate()
        process.terminate()

    def __install_apk(self):
        command = self.__adb_command + " install -r " + self.__apk_filepath
        process = self.__run_command(command)
        process.communicate()
        process.terminate()

    def __uninstall_apk(self):
        command = self.__adb_command + " uninstall " + self.__packagename
        process = self.__run_command(command)
        process.communicate()
        process.terminate()

    def __force_stop(self):
        command = self.__adb_command + " shell am force-stop " + self.__packagename
        process = self.__run_command(command)
        process.communicate()
        process.terminate()

    def __check_end_file(self):
        command = self.__adb_command + " shell ls " + self.__unpackfilepath + "/end"
        process = self.__run_command(command)
        if(process.stdout.read().find(b"No such file or directory") == -1):
            process.terminate()
            return True
        process.terminate()
        return False

    def __check_process(self):
        command = self.__adb_command + " shell \"ps | grep " + self.__packagename + "\""
        process = self.__run_command(command)
        if(process.stdout.read() == b''):
            process.terminate()
            return False
        process.terminate()
        return True

    def __get_classes_size(self):
        command = self.__adb_command + " shell ls -l " + self.__unpackfilepath + "/classes | awk \'{print $4;}\'"
        process = self.__run_command(command)
        readres = process.stdout.read().strip()
        process.terminate()
        if(readres == b'file'):
            return -1
        return int(readres)


    def __restart_app(self):
        self.__force_stop()
        self.__launch_start()

    def __pull_files(self):
        time.sleep(3)
        command = self.__adb_command + " pull " + self.__unpackfilepath + "/ " + self.__pull_dst
        process = self.__run_command(command)
        process.communicate()
        process.terminate()
        time.sleep(3)


    def __rebuild_dex(self):
        cwd = os.getcwd()
        os.chdir(self.__pull_dst)
        lines = []
        try:
            with open("dex", "rb") as dex:
                lines = dex.readlines()
        except Exception as e:
            logger.info(e)
            raise
        with open("dex", "wb") as dex:
            for line in lines[1:]:
                dex.write(line)
        command = self.__build_dex
        process = self.__run_command(command)
        process.communicate()
        process.terminate()
        os.chdir(cwd)

    def __check_device(self):
        command = self.__adb_command + " shell id " # adb  -s  serialno shell id
        process = self.__run_command(command)
        if(len(process.stderr.read()) > 0):
            process.terminate()
            return False
        process.terminate()
        return True
    
    def __check_result_dex(self):
        result_dex_path = os.path.join(self.__pull_dst, 'result.dex')
        print(result_dex_path)
        if os.path.exists(result_dex_path):
            flag = False
            with open(str(result_dex_path), 'rb+') as ff:
                first_line = ff.readline().strip()
                if first_line:
                    first_line = bytes.decode(first_line)
                    if not first_line.startswith('dex'):
                        print(first_line)
                        flag = True
                    else:
                        print('startswith dex')
                        pass
            if flag:
                self.__first_line_switch(result_dex_path,)
                
    def __first_line_switch(self, dst_file, s=1):
        with open(dst_file, 'rb+') as ff:
            ff.seek(40, 0)
            remain = ff.read()
        # 默认替换第一行内容
        with open(dst_file, 'wb+') as f:
            f.write(remain)
        print('switch success!')
        
    def start(self):
        if not self.__check_device():
            return -2
        self.__uninstall_apk()
        self.__install_apk()
        self.__launch_start()
        time.sleep(10)
        lastsize = 0
        restarttimes = 0
        while True:
            if(self.__check_end_file() == True):
                break
            if(self.__check_process() == False):
                if(self.__get_classes_size() == -1):
                    return -1
                self.__restart_app()
            current_size = self.__get_classes_size()
            if(lastsize < current_size):
                lastsize = current_size
            elif(lastsize >= current_size):
                self.__restart_app()
                restarttimes = restarttimes + 1
            if(restarttimes > 30):
                return -1
            time.sleep(3)
        self.__pull_files()
        self.__rebuild_dex()
        self.__check_result_dex() # 检查生成的result.dex文件
        #todo dey2dex 已解决
        return 0


serialnos = []
def unpack_process(serialno, apkpath):
    try:
        un = unpack2(serialno, apkpath)
        # retval = un.start()
    except Exception as e:
        logger.info(traceback.format_exc())
        retval = -1
    else:
        try:
            retval = un.start()
        except Exception as e:
            logger.info(traceback.format_exc())
            retval = -1
    if(retval == -1):
        apk_name = os.path.split(apkpath)[1]
        pack_name = apk_name.split('.apk')[0]
        if os.path.exists(os.path.join(success_result_path, pack_name)):
            # move to failed result
            pack_path = os.path.join(success_result_path, pack_name)
            dst_path = failed_result_path
            move_to_failed_result(pack_path, dst_path)
        
        logger.info("unpack failed with " + apkpath)
        with open(failed_apk_path, 'a')as f:
            f.write(apk_name + '\n')
    else:
        logger.info('success unpack with ' + apkpath)
    return serialno,

def __run_command(command):
    logger.info(command)
    # print(command)
    return subprocess.Popen(command, shell = True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr = subprocess.PIPE)

def move_to_failed_result(origin_path, dst_path):
    command = 'mv {} {}'.format(origin_path, dst_path)
    process = __run_command(command)
    process.communicate()
    process.terminate()

def reuse(args):
    global serialnos
    
    serialnos.remove(args[0])

def adb_devices():
    senos = []
    adb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "adb")
    process = subprocess.Popen(adb_path + " devices", shell = True, stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    lines = process.stdout.readlines()
    for line in lines:
        arr = line.split()
        if len(arr) == 2 and arr[1] == b'device':
            senos.append(arr[0].decode())
    return senos


def unpack_apks(apklist):
    global serialnos
    pool = Pool(10)
    for apkpath in apklist:
        apkpath = apkpath.strip()
        while(True):
            senos = adb_devices()
            flag = False
            for seno in senos:
                if seno not in serialnos:
                    flag = True
                    break
            if flag:
                break
        serialnos.append(seno)
        pool.apply_async(unpack_process, args = (seno, apkpath), callback = reuse)
    pool.close()
    pool.join()

def main():
    with open("list", "r") as fff:
        lines = fff.readlines()
    unpack_apks(lines)


if __name__ == '__main__':
    main()
