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

INSERT INTO library (libId, name, libDesc, createTime, maxReviewsPerDay, newCardsPerDay, easyInterval, maxInterval, maxAnswerTime, isShowAnswerTime )
VALUES ('001', 'library-one', 'The first library', '2015-04-13', 50, 50, 3, 3650, 30, 1)
