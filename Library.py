# -*- coding: gbk -*-
class Library():
    """
    �ʿ���
    ͨ����¼���ɴ��������ʿ�Ƭ����������ͬ��libraryId�ļ�¼�����ɵĿ�Ƭ���ڵĴʿ���ͬ
    ������дʿ�Ҳ��������⣬��Ϊÿ�μ�����Ҫѡ�����Ķ���
    ������������Ǵʿ�
    �Լ���Ч����ͳ��Ҳ���Դʿ�Ϊ���ֵ�

    libId �ʿ�ID
    name �ʿ�����
    libDesc �ʿ�����
    createTime ����ʱ��
    maxReviewsPerDay ÿ�����ϰ���ʿ�Ƭ��Ŀ
    newCardsPerDay ÿ�����ѧϰ���ʿ�Ƭ��Ŀ
    easyInterval ���򵥡������ļ������
    maxInterval ���ʱ�������죩
    maxAnswerTime ��ش�����
    isShowAnswerTime ʱ����ʾ��ʱ��(True/False)
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