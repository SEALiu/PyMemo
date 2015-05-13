# -*- coding: utf-8 -*-
import DBFun
import time
import datetime


def find_all():
    sql = "SELECT * FROM record"
    return DBFun.select('db_pymemo.db', sql)


def find_new():
    """
    找到新记录并返回
    :return:
    """
    sql = "SELECT * FROM record WHERE interval = -1"
    new_record = DBFun.select('db_pymemo.db', sql)
    return new_record


def find_expired():
    """
    找到已经到期的记录并返回
    :return:
    """
    expired_list = []
    sql = "SELECT * FROM record WHERE interval != -1"
    today = datetime.date.today()
    for rows in DBFun.select('db_pymemo.db', sql):
        interval = rows[6]
        review_time = rows[4]
        # 下次应该复习时间
        review_time_date = datetime.datetime.strptime(review_time, '%Y/%m/%d').date()
        a_time_date = review_time_date + datetime.timedelta(days=interval)
        # 比较秒数
        a_time = time.mktime(time.strptime(str(a_time_date), '%Y-%m-%d'))
        b_time = time.mktime(time.strptime(str(today), '%Y-%m-%d'))
        if b_time >= a_time:
            expired_list.append(rows)
    return expired_list


def find_remembered():
    """
    找到已经记住的记录并返回
    :return:
    """
    sql = "SELECT * FROM record WHERE EF>=3.0"
    remembered_list = DBFun.select('db_pymemo.db', sql)
    return remembered_list


def find_learned():
    today = datetime.date.today().strftime('%Y/%m/%d')
    sql = "SELECT * FROM record WHERE reviewTime == '" + today + "'"
    learned_record = DBFun.select('db_pymemo.db', sql)
    return learned_record


def find_hard():
    """
    找到始终记不住的记录并返回
    :return:
    """
    sql = "SELECT * FROM record WHERE EF=1.3"
    hard_list = DBFun.select('db_pymemo.db', sql)
    return hard_list


def find_today():
    """
    找到今天添加的记录并返回
    :return:
    """
    today_record = []
    sql = "SELECT * FROM record WHERE interval = -1"
    for rows in DBFun.select('db_pymemo.db', sql):
        add_date = rows[3]
        add_time = time.mktime(time.strptime(str(add_date), '%Y/%m/%d'))
        now_time = time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d'))
        if add_time == now_time:
            today_record.append(rows)
    return today_record