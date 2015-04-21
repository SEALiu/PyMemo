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


# reload(sys)
# sys.setdefaultencoding('gbk')
# conn = connect_db('db_pymemo.db')
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
#         "'00000300000', 'pear', '梨', " \
#         " '2015-04-20', '2015-05-20', '2015-05-20', 16, 1.5, 0)"
#
#
#
# deleteSQL1 = "DELETE FROM record where recordId='00000300000'"
# deleteSQL2 = "DELETE FROM record where "
#
# selectSQL1 = "SELECT * FROM library"
# selectSQL2 = "SELECT * FROM record"
# selectSQL3 = "SELECT * FROM record WHERE recordId LIKE '%001'"
#
# updateSQL = "UPDATE library set name='孤儿院' where libId=000"

# update(conn, insertSQL1)
# update(conn, insertSQL2)
# update(conn, insertSQL3)

# update(conn, deleteSQL1)
# update(conn, deleteSQL2)
# commit(conn)
# cursor = select(conn, selectSQL3)
# print cursor.fetchall()
# for rows in cursor:
#     print "libId = ", rows[0]
#
# close_db(conn)