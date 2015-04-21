# -*- coding: gbk -*-
class Record(object):
    """
    记录类
    根据记录的类型（基本记录，和逆转记录）来进行卡片的生成
    如果是基本记录，那么只生成1张卡片
    如果是逆转记录，那么生成2张卡片，这两张卡片正反面恰好相反，但是是两张独立的卡片

    recordId 记录的ID (内容为：前6位为CardId，第7位和第8位为类型[00为基本卡；1X为逆转卡(X为0表示逆转卡的第一张，X为1表示逆转卡的第二张)]，后3位为LibraryId)
    ques 记录的正面内容
    ans 记录的反面内容
    addTime 记录添加的时间
    reviewTime 最后的复习时间
    alertTime 记录最后的修改时间
    interval 间隔天数
    EF E-Factor（这个值默认为2.5，根据SM-2算法进行变化，从而影响interval）
    isPaused 是否被挂起（挂起的记录意味着在学习记忆库的时候不会出现，这种情况可能是这个单词很简单，或者暂时不想学习这个单词）
    """
    def __init__(self, recordId, ques, ans, addTime, reviewTime, alertTime, interval, EF=2.5, isPaused=False):
        self.recordId = recordId
        self.question = ques
        self.answer = ans
        self.type = type
        self.addTime = addTime
        self.reviewTime = reviewTime
        self.alertTime = alertTime
        self.interval = interval
        self.EF = EF
        self.isPaused = isPaused

    # get/set 方法
    def getId(self):
        return self.recordId

    def getQues(self):
        return self.question

    def setQues(self, content):
        self.question = content

    def getAns(self):
        return self.answer

    def setAns(self, content):
        self.answer = content

    def getAddTime(self):
        return self.addTime

    def getReviewTime(self):
        return self.reviewTime

    def setReviewTime(self, time):
        self.reviewTime = time

    def getAlertTime(self):
        return self.alertTime

    def setAlertTime(self, time):
        self.alertTime = time

    def getInterval(self):
        return self.interval

    def setInterval(self, inter):
        self.interval = inter

    def getEF(self):
        return self.EF

    def setEF(self, ef):
        self.EF = ef

    def getIsPaused(self):
        return self.isPaused

    def setIsPaused(self, flag):
        self.isPaused = flag