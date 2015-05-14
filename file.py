# -*- coding: utf-8 -*-
import re
import FrameFun
import os


def fetch_statistic(fn):
    """
    获取NSR的统计数据
    :param fn:
    :return:
    """
    f = open(fn, 'r')
    statistic = {}
    for eachLine in f:
        if eachLine.strip()[0] != '#':
            statistic[eachLine[0]] = int(eachLine[2])
    f.close()
    return statistic


def set_statistic(fn, name, value):
    """
    设置NSR的统计数据
    :param fn:
    :param name:
    :param value:
    :return:
    """
    f1 = open(fn)
    f1_list = f1.readlines()
    f1.close()
    if name == 'N':
        f1_list[0] = 'N:' + str(value) + '\n'
    elif name == 'S':
        f1_list[1] = 'S:' + str(value) + '\n'
    elif name == 'R':
        f1_list[2] = 'R:' + str(value) + '\n'
    f2 = open(fn, 'w+')
    f2.writelines(f1_list)


def write_rs(fn, ls, v):
    """
    向指定文件中写入待学习内容，并更新NSR统计数据
    :param fn:file_name
    :param ls:NSR_list
    :param v:NSR
    :return:
    """
    f = open(fn, 'a')
    for rows in ls:
        f.write('\n')
        for item in FrameFun.tuple_add_front(rows, v):
            f.write('%s%s' % (item, ' '))
    f.close()
    set_statistic(fn, v, len(ls))
    return True


def is_exist(url, name):
    """
    文件name是否存在路径url下
    :param url:
    :param name:
    :return:
    """
    dir_ls = os.listdir(url)
    return dir_ls.count(name)