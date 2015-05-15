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
    conn.execute(sql)
    conn.commit()
    conn.close()


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









# conn = connect_db('db_pymemo.db')
# conn.text_factory = str
# insertSQL1 = "INSERT INTO library (" \
#         "libId, name, libDesc, createTime, " \
#         "maxReviewsPerDay, newCardsPerDay, " \
#         "easyInterval, maxInterval, maxAnswerTime," \
#         " isShowAnswerTime ) " \
#       "VALUES (" \
#         "'000', '孤儿院', '存放没有归属词库的记录，并且此词库不能被删除'," \
#         " '2015-04-13', 50, 50, 3, 3650, 30, 1)"
#
# insertSQL2 = "INSERT INTO library (" \
#         "libId, name, libDesc, createTime, " \
#         "maxReviewsPerDay, newCardsPerDay, " \
#         "easyInterval, maxInterval, maxAnswerTime," \
#         " isShowAnswerTime ) " \
#       "VALUES (" \
#         "'001', 'library-one', 'The first library'," \
#         " '2015-04-13', 50, 50, 3, 3650, 30, 1)"
#
# insertSQL3 = "INSERT INTO record (" \
#         "recordId, ques, ans, addTime, " \
#         "reviewTime, alertTime, " \
#         "interval, EF, isPaused) " \
#       "VALUES (" \
#         "'00000100000', 'pear', '梨', " \
#         " '2015-04-20', '2015-05-20', '2015-05-20', 16, 1.5, 0)"
#
#
#
# deleteSQL1 = "DELETE FROM record"
# deleteSQL2 = "DELETE FROM library"
#
# selectSQL1 = "SELECT * FROM library"
# selectSQL2 = "SELECT * FROM record"
# selectSQL3 = "SELECT * FROM record WHERE recordId LIKE '%001'"
#
# updateSQL = "UPDATE library set name='孤儿院', libDesc='' where libId = '000'"
# conn.execute(updateSQL)
# update(conn, insertSQL1)
# update(conn, insertSQL2)
# update(conn, insertSQL3)

# update(conn, deleteSQL1)
# update(conn, deleteSQL2)
# update(conn, updateSQL)
# commit(conn)
# cursor = select(conn, "SELECT * FROM library where libId = '000'")
# for rows in cursor:
#     print rows[1]
# print cursor.fetchall()
# for rows in cursor:
#     print "libId = ", rows[0]
#
# close_db(conn)