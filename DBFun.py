# -*- coding: utf-8 -*-
import sqlite3


def connect_db(url):
    """connect the DataBase"""
    return sqlite3.connect(url)


def select(url, sql):
    """execute the select sql"""
    conn = connect_db(url)
    conn.text_factory = str
    r = conn.execute(sql).fetchall()
    conn.close()
    return r


def update(url, sql):
    """execute update, delete and insert SQL"""
    conn = connect_db(url)
    conn.text_factory = str
    result = conn.execute(sql)
    conn.commit()

    num = 0
    for rows in result:
        num += 1
    conn.close()
    return num


def max_lib(column):
    """返回library中指定列最大值"""
    select_sql = "SELECT max(" + column + ") FROM library"
    result_list = select('db_pymemo.db', select_sql)
    max_lib_id = result_list[0][0]
    if max_lib_id:
        return int(max_lib_id)
    else:
        return -1

def max_record(column):
    """返回record中指定列的最大值"""
    select_sql = "SELECT max(" + column + ") FROM record"
    result_list = select('db_pymemo.db', select_sql)
    max_record_id = result_list[0][0]
    if max_record_id:
        return int(max_record_id[:5])
    else:
        return -1