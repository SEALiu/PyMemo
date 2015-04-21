# -*- coding: gbk -*-
class Record(object):
    """
    ��¼��
    ���ݼ�¼�����ͣ�������¼������ת��¼�������п�Ƭ������
    ����ǻ�����¼����ôֻ����1�ſ�Ƭ
    �������ת��¼����ô����2�ſ�Ƭ�������ſ�Ƭ������ǡ���෴�����������Ŷ����Ŀ�Ƭ

    recordId ��¼��ID (����Ϊ��ǰ6λΪCardId����7λ�͵�8λΪ����[00Ϊ��������1XΪ��ת��(XΪ0��ʾ��ת���ĵ�һ�ţ�XΪ1��ʾ��ת���ĵڶ���)]����3λΪLibraryId)
    ques ��¼����������
    ans ��¼�ķ�������
    addTime ��¼��ӵ�ʱ��
    reviewTime ���ĸ�ϰʱ��
    alertTime ��¼�����޸�ʱ��
    interval �������
    EF E-Factor�����ֵĬ��Ϊ2.5������SM-2�㷨���б仯���Ӷ�Ӱ��interval��
    isPaused �Ƿ񱻹��𣨹���ļ�¼��ζ����ѧϰ������ʱ�򲻻���֣��������������������ʺܼ򵥣�������ʱ����ѧϰ������ʣ�
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

    # get/set ����
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