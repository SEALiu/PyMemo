# -*- coding: gbk -*-
import sqlite3

conn = sqlite3.connect('db_pymemo.db')
c = conn.cursor()
c.execute(
    '''CREATE TABLE library (
libId text,
name text,
libDesc text,
createTime text,
maxReviewsPerDay integer,
newCardsPerDay integer,
easyInterval integer,
maxInterval integer,
maxAnswerTime integer,
isShowAnswerTime boolean
)''')

c.execute(
    '''CREATE TABLE record (
recordId text,
ques text,
ans text,
addTime text,
reviewTime text,
alertTime text,
interval integer,
EF integer,
isPaused boolean
)''')
