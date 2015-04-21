# PyMemo
毕业设计——单词记忆软件

----

这是我的一项毕业设计，课题为：基于Python的单词记忆软件开发。

目前仍处于开发阶段！

----

GUI：wxpython2.7.9

IDE：PyCharm

----

其中的图标大部分都来自：[http://findicons.com](http://findicons.com)

向所有提出过建议，报告bug的人表示感谢！

----

Emial：iliuyang@foxmail.com


##表结构

###library:

		CREATE TABLE library (
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
		)

- recordId 记录的ID (内容为：前6位为CardId，第7位和第8位为类型[00为基本卡；1X为逆转卡(X为0表示逆转卡的第一张，X为1表示逆转卡的第二张)]，后3位为LibraryId)
- ques 记录的正面内容
- ans 记录的反面内容
- addTime 记录添加的时间
- reviewTime 最后的复习时间
- alertTime 记录最后的修改时间
- interval 间隔天数
- EF E-Factor（这个值默认为2.5，根据SM-2算法进行变化，从而影响interval）
- isPaused 是否被挂起（挂起的记录意味着在学习记忆库的时候不会出现，这种情况可能是这个单词很简单，或者暂时不想学习这个单词）

###record:

		CREATE TABLE record (
		    recordId text,
		    ques text,
		    ans text,
		    addTime text,
		    reviewTime text,
		    alertTime text,
		    interval integer,
		    EF integer,
		    isPaused boolean
		)

- libId 词库ID
- name 词库名称
- libDesc 词库描述
- createTime 创建时间
- maxReviewsPerDay 每日最大复习单词卡片数目
- newCardsPerDay 每日最大学习单词卡片数目
- easyInterval ‘简单’反馈的间隔天数
- maxInterval 最大时间间隔（天）
- maxAnswerTime 最长回答秒数
- isShowAnswerTime 时候显示计时器(True/False)

