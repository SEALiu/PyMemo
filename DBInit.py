# # -*- coding: utf-8 -*-
# # Copyright (c) 2015 - sealiu <iliuyang@foxmail.com>
# import sqlite3
# import time
#
# conn = sqlite3.connect('db_pymemo.db')
# c = conn.cursor()
# c.execute(
#     '''CREATE TABLE library (
# libId text PRIMARY KEY NOT NULL UNIQUE,
# name text NOT NULL,
# libDesc text NOT NULL,
# createTime text,
# maxReviewsPerDay integer DEFAULT 50,
# newCardsPerDay integer DEFAULT 50,
# easyInterval integer DEFAULT 3,
# maxInterval integer DEFAULT 3650,
# isShowRest text DEFAULT 'True'
# )''')
#
# c.execute(
#     '''CREATE TABLE record (
# recordId text PRIMARY KEY NOT NULL UNIQUE,
# ques text,
# ans text,
# addTime text,
# reviewTime text,
# alertTime text,
# interval REAL DEFAULT -1.0,
# EF REAL DEFAULT 2.5,
# isPaused text DEFAULT 'False'
# )''')
#
# create_time = time.strftime('%Y/%m/%d', time.localtime(time.time()))
# insert_lib_sql = "INSERT INTO library(libId, name, libDesc, createTime) " \
#                  "VALUES ('000', '孤儿院', '存放没有归属词库的记录，并且此词库不能被删除', '" + create_time + "')"
# c.execute(insert_lib_sql)
# conn.commit()
#
# c.close()
# conn.close()