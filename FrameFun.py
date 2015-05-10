# -*- coding: utf-8 -*-
import DBFun
import time
import datetime


def find_all():
    conn = DBFun.connect_db('db_pymemo.db')
    conn.text_factory = str
    sql = "SELECT * FROM record"
    cursor = DBFun.select(conn, sql)
    all_record = cursor.fetchall()
    return all_record


def find_new():
    """
    找到新记录并返回
    :return:
    """
    conn = DBFun.connect_db('db_pymemo.db')
    conn.text_factory = str
    sql = "SELECT * FROM record WHERE interval = -1"
    cursor = DBFun.select(conn, sql)
    new_record = cursor.fetchall()
    DBFun.close_db(conn)
    return new_record


def find_expired():
    """
    找到已经到期的记录并返回
    :return:
    """
    expired_list = []
    conn = DBFun.connect_db('db_pymemo.db')
    conn.text_factory = str
    sql = "SELECT * FROM record WHERE interval != -1"
    cursor = DBFun.select(conn, sql)
    today = datetime.date.today()
    for rows in cursor.fetchall():
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
    DBFun.close_db(conn)
    return expired_list


def find_remembered():
    """
    找到已经记住的记录并返回
    :return:
    """
    conn = DBFun.connect_db('db_pymemo.db')
    conn.text_factory = str
    sql = "SELECT * FROM record WHERE EF>=3.0"
    cursor = DBFun.select(conn, sql)
    remembered_list = cursor.fetchall()
    DBFun.close_db(conn)
    return remembered_list


def find_learned():
    today = datetime.date.today().strftime('%Y/%m/%d')
    conn = DBFun.connect_db('db_pymemo.db')
    conn.text_factory = str
    sql = "SELECT * FROM record WHERE reviewTime == '" + today + "'"
    cursor = DBFun.select(conn, sql)
    learned_record = cursor.fetchall()
    DBFun.close_db(conn)
    return learned_record


def find_hard():
    """
    找到始终记不住的记录并返回
    :return:
    """
    conn = DBFun.connect_db('db_pymemo.db')
    conn.text_factory = str
    sql = "SELECT * FROM record WHERE EF=1.3"
    cursor = DBFun.select(conn, sql)
    hard_list = cursor.fetchall()
    DBFun.close_db(conn)
    return hard_list


def find_today():
    """
    找到今天添加的记录并返回
    :return:
    """
    today_record = []
    conn = DBFun.connect_db('db_pymemo.db')
    conn.text_factory = str
    sql = "SELECT * FROM record WHERE interval = -1"
    cursor = DBFun.select(conn, sql)

    for rows in cursor.fetchall():
        add_date = rows[3]
        add_time = time.mktime(time.strptime(str(add_date), '%Y/%m/%d'))
        now_time = time.mktime(time.strptime(str(datetime.date.today()), '%Y-%m-%d'))
        if add_time == now_time:
            today_record.append(rows)
    DBFun.close_db(conn)
    return today_record