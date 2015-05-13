# -*- coding: utf-8 -*-
# 对recordstack.py进行操作


def fetch_statistic():
    f = open("recordstack.pm", 'r')
    statistic = {}
    for eachLine in f:
        if eachLine.strip()[0] != '#':
            statistic[eachLine[0]] = int(eachLine[2])
    f.close()
    return statistic


def write_statistic():
    f = open("recordstack.pm", 'w') 

print fetch_statistic()
