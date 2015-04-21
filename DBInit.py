# -*- coding: gbk -*-
import sqlite3

conn = sqlite3.connect('db_pymemo.db')
c = conn.cursor()
c.execute(
    '''CREATE TABLE library (
libId text PRIMARY KEY NOT NULL UNIQUE,
name text NOT NULL,
libDesc text NOT NULL,
createTime text,
maxReviewsPerDay integer DEFAULT 50,
newCardsPerDay integer DEFAULT 50,
easyInterval integer DEFAULT 3,
maxInterval integer DEFAULT 3650,
maxAnswerTime integer DEFAULT 30,
isShowAnswerTime boolean DEFAULT True
)''')

c.execute(
    '''CREATE TABLE record (
recordId text PRIMARY KEY NOT NULL UNIQUE,
ques text,
ans text,
addTime text,
reviewTime text,
alertTime text,
interval integer DEFAULT -1,
EF integer DEFAULT 2.5,
isPaused boolean DEFAULT FALSE
)''')
