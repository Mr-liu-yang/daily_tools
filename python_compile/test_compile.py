# -*- coding:utf-8 -*-
import distutils.core
import Cython.Build
import os

py_file_name = '/home/pangu/Desktop/py_test.py'


def test_compile():
    a = Cython.Build.cythonize(py_file_name)
    distutils.core.setup(
        name='pyd的编译',  # 包名称
        version="1.0",  # 包版本号
        ext_modules=a,  # 扩展模块
        author="123",  # 作者
        author_email='456@163.com'  # 作者邮箱

    )


def get_py_file():
    path = '/opt/ziggurat/api/'
    a_list = []
    for ele in os.listdir(path):
        if ele.endswith('.py'):
            a = Cython.Build.cythonize(path + ele)[0]
            a_list.append(a)

    distutils.core.setup(
        name='pyd的编译',  # 包名称
        version="1.0",  # 包版本号
        ext_modules=a_list,  # 扩展模块
        author="123",  # 作者
        author_email='456@163.com'  # 作者邮箱

    )


if __name__ == '__main__':
    test_compile()
    #get_py_file()

