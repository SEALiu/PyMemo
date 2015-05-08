# -*- coding: utf-8 -*-

# f = open('recordstack.pm', 'r')
# allLines = [line.strip() for line in f.readlines()]
# f.close()
# for eachLine in allLines:
#     print eachLine
import DBFun
import time


def find_new(i):
    """
    随机返回指定词库中的新记录
    :param i: lib_id
    :return:
    """
    conn = DBFun.connect_db('db_pymemo.db')
    sql = "SELECT * FROM record WHERE interval = -1 AND recordId LIKE '%" + i + "'"
    cursor = DBFun.select(conn, sql)
    return cursor.fetchall()


def find_expired(i):
    """
    找到指定词库中已经到期的记录并返回
    :param i:
    :return:
    """
    conn = DBFun.connect_db('db_pymemo.db')
    sql = "SELECT * FROM record WHERE interval = -1 AND reviewTime IS NOT NULL"
    cursor = DBFun.select(conn, sql)
    for rows in cursor.fetchall():
        print time.mktime(time.strptime(rows[4], '%Y/%m/%d'))
    # return cursor.fetchall()


def find_remembered(i):
    """
    找到指定词库中已经记住的记录并返回
    :param i: 词库id
    :return:
    """
    conn = DBFun.connect_db('db_pymemo.db')
    sql = "SELECT * FROM record WHERE EF>=3.0 AND recordId LIKE '%" + i + "'"
    cursor = DBFun.select(conn, sql)
    return cursor.fetchall()

find_expired('000')