# -*- coding: gbk -*-
import sqlite3


def connect_db(url):
    """connect the DataBase"""
    return sqlite3.connect(url)


def close_db(conn):
    """close the connection of DB"""
    conn.close()


def commit(conn):
    """commit operation"""
    conn.commit()


def select(conn, sql):
    """execute the select sql"""
    return conn.execute(sql)


def update(conn, sql):
    """execute update, delete and insert SQL"""
    return conn.execute(sql)


def max_lib(column):
    """����library��ָ�������ֵ"""
    select_sql = "SELECT max(" + column + ") FROM library"
    conn = connect_db('db_pymemo.db')
    cursor = select(conn, select_sql)
    result_list = cursor.fetchall()
    close_db(conn)
    max_lib_id = result_list[0][0]
    if max_lib_id:
        return int(max_lib_id)
    else:
        return -1


def max_record(column):
    """����record��ָ���е����ֵ"""
    select_sql = "SELECT max(" + column + ") FROM record"
    conn = connect_db('db_pymemo.db')
    cursor = select(conn, select_sql)
    result_list = cursor.fetchall()
    close_db(conn)
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
#         "'000', '�¶�Ժ', '���û�й����ʿ�ļ�¼�����Ҵ˴ʿⲻ�ܱ�ɾ��'," \
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
#         "'00000100000', 'pear', '��', " \
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
# updateSQL = "UPDATE library set name='�¶�Ժ', libDesc='' where libId = '000'"
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