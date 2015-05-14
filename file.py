import FrameFun
import os


def fetch_statistic(fn):
    f = open(fn, 'r')
    statistic = {}
    for eachLine in f:
        if eachLine.strip()[0] != '#':
            statistic[eachLine[0]] = int(eachLine[2])
    f.close()
    return statistic


def write_rs(fn, ls, v):
    f = open(fn, 'a')
    for rows in ls:
        f.write('\n')
        for item in FrameFun.tuple_add_front(rows, v):
            f.write('%s%s' % (item, ' '))
    f.close()
    return True


def is_exist(url, name):
    dir_ls = os.listdir(url)
    return dir_ls.count(name)

