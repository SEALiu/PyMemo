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
    n = 0
    s = 0
    r = 0
    statistic = {}
    for eachLine in f:
        if eachLine.strip()[0] == 'N':
            n += 1
        elif eachLine.strip()[0] == 'S':
            s += 1
        elif eachLine.strip()[0] == 'R':
            r += 1
    statistic['N'] = n - 1
    statistic['S'] = s - 1
    statistic['R'] = r - 1
    return statistic


def set_statistic(fn, name, value):
    """
    设置NSR的统计数据
    :param fn:
    :param name:
    :param value:
    :return:
    """
    f1_list = read_rs(fn)
    if name == 'N':
        f1_list[0] = 'N:' + str(value) + '\n'
    elif name == 'S':
        f1_list[1] = 'S:' + str(value) + '\n'
    elif name == 'R':
        f1_list[2] = 'R:' + str(value) + '\n'
    f2 = open(fn, 'w+')
    f2.writelines(f1_list)
    f2.close()


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
    set_statistic(fn, v, fetch_statistic(fn)[v])
    return True


def read_rs(fn):
    f = open(fn)
    f_list = f.readlines()
    f.close()
    return f_list


def is_exist(url, name):
    """
    文件name是否存在路径url下
    :param url:
    :param name:
    :return:
    """
    dir_ls = os.listdir(url)
    return dir_ls.count(name)


def exist_id(fn):
    """
    返回fn文件中已经存在的记录的id列表
    :param fn: file_name
    :return:
    """
    exist_ls = []
    result_ls = read_rs(fn)
    for index, rows in enumerate(result_ls):
        if index >= 3:
            exist_ls.append(rows[2:10])
    return exist_ls


def filter_repeat(fn, ls):
    e_id = exist_id(fn)
    ls_temp = []
    for index, item in enumerate(ls):
        if e_id.count(item[0]) != 0:
            ls_temp.append(item)
    for index in ls_temp:
        ls.remove(index)
    return ls


def fetch_nsr(fn, nsr):
    """
    获取fn中的NSR_list，并分别返回
    :param fn: file_name <type str>
    :param nsr: N, S, R <type str>
    :return:
    """
    nsr_list = []
    new_ls = []
    for items in read_rs(fn):
        if items[0] == nsr:
            nsr_list.append(items)
    ls = nsr_list[1:]

    for item in ls:
        new_ls.append(tuple(item.split()))
    return new_ls
