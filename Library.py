# -*- coding: gbk -*-
class Library():
    """
    词库类
    通过记录生成词条（单词卡片），具有相同的libraryId的记录所生成的卡片所在的词库相同
    本软件中词库也叫做记忆库，因为每次记忆需要选择记忆的对象
    这里记忆对象就是词库
    对记忆效果的统计也是以词库为划分的

    libId 词库ID
    name 词库名称
    libDesc 词库描述
    createTime 创建时间
    maxReviewsPerDay 每日最大复习单词卡片数目
    newCardsPerDay 每日最大学习单词卡片数目
    easyInterval ‘简单’反馈的间隔天数
    maxInterval 最大时间间隔（天）
    maxAnswerTime 最长回答秒数
    isShowAnswerTime 时候显示计时器(True/False)
    """
    def __init__(self, libId, name, createTime,
                 libDesc=" ", maxReviewsPerDay=50, newCardsPerDay=50, easyInterval=3,
                 maxInterval = 3650, maxAnswerTime = 30, isShowAnswerTime = True):
        self.libId = libId
        self.name = name
        self.libDesc = libDesc
        self.createTime = createTime
        self.maxReviewsPerDay = maxReviewsPerDay
        self.newCardsPerDay = newCardsPerDay
        self.easyInterval = easyInterval
        self.maxInterval = maxInterval
        self.maxAnswerTime = maxAnswerTime
        self.isShowAnswerTime = isShowAnswerTime

    def getLibId(self):
        return  self.libId

    def getName(self):
        return self.name

    def setName(self, text):
        self.name = text

    def getLibDesc(self):
        return self.libDesc

    def setLibDesc(self, content):
        self.libDesc = content

    def getCreateTime(self):
        return self.createTime

    def setCreateTime(self, time):
        self.createTime = time

    def getMaxReviewsPerDay(self):
        return  self.maxReviewsPerDay

    def setMaxReviewsPerDay(self, number):
        self.maxReviewsPerDay = number

    def getNewCardsPerDay(self):
        return self.newCardsPerDay

    def setNewCardsPerDay(self, number):
        self.newCardsPerDay = number

    def getEasyInterval(self):
        return self.easyInterval

    def setEasyInterval(self, number):
        self.easyInterval = number

    def getMaxInterval(self):
        return self.maxInterval

    def setMaxInterval(self, number):
        self.maxInterval = number

    def getMaxAnswerTime(self):
        return self.maxAnswerTime

    def setMaxAnswerTime(self, number):
        self.maxAnswerTime = number

    def getIsShowAnswerTime(self):
        return self.IsShowAnswerTime

    def setIsShowAnswerTime(self, flag):
        self.IsShowAnswerTime = flag