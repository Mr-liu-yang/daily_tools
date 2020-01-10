# -* -coding: UTF-8 -* -

import os
import shutil
import sys
import time
from distutils.core import setup

from Cython.Build import cythonize

starttime = time.time()
currdir = os.path.abspath('.')
parentpath = sys.argv[1] if len(sys.argv) > 1 else ""
setupfile = os.path.join(os.path.abspath('.'), __file__)
build_dir = "build" + "/" + parentpath
build_tmp_dir = build_dir + "/temp"

"""
exclude_file_list = [
    parentpath + '/conf/settings.py',
    parentpath + '/lib/ios_scan',
    parentpath + '/staticPlug',
    parentpath + '/sqlmap',
    parentpath + '/web',
]
"""


def getpy(basepath=os.path.abspath('.'), parentpath='', name='', excepts=(), copyOther=False, delC=False):
    fullpath = os.path.join(basepath, parentpath, name)
    for fname in os.listdir(fullpath):
        ffile = os.path.join(fullpath, fname)
        if os.path.isdir(ffile) and fname != build_dir and not fname.startswith('.'):
            for f in getpy(basepath, os.path.join(parentpath, name), fname, excepts, copyOther, delC):
                yield f
        elif os.path.isfile(ffile):
            ext = os.path.splitext(fname)[1]
            if ext == ".c":
                if delC and os.stat(ffile).st_mtime > starttime:
                    os.remove(ffile)
            elif ffile not in excepts and os.path.splitext(fname)[1] not in ('.pyc', '.pyx'):
                if os.path.splitext(fname)[1] in ('.py', '.pyx') and not fname.startswith('__'):
                    yield os.path.join(parentpath, name, fname)
                elif copyOther:
                    dstdir = os.path.join(basepath, build_dir, '/'.join(parentpath.split('/')[1:]), name)
                    if not os.path.isdir(dstdir):
                        os.makedirs(dstdir)
                    shutil.copyfile(ffile, os.path.join(dstdir, fname))


# 获取py列表
module_list = list(getpy(basepath=currdir, parentpath=parentpath, excepts=(setupfile)))
try:
    setup(ext_modules=cythonize(module_list), script_args=["build_ext", "-b", build_dir, "-t", build_tmp_dir])
except Exception as e:
    print(e)
else:
    module_list = list(getpy(basepath=currdir, parentpath=parentpath, excepts=(setupfile), copyOther=True))
module_list = list(getpy(basepath=currdir, parentpath=parentpath, excepts=(setupfile), delC=True))
if os.path.exists(build_tmp_dir):
    shutil.rmtree(build_tmp_dir)
print("complate! time:", time.time() - starttime, 's')

