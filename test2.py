# -*- coding: utf-8 -*-
import wx
import file
import wx.lib.buttons as buttons
import threading
import random


class WorkerThread(threading.Thread):
    def __init__(self, threadNum, window):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()
        self.messageCount = random.randint(1, 5)
        self.messageDelay = 0.1 + 2.0 * random.random()

    def stop(self):
        self.timeToQuit.set()

    def run(self):
        msg = "Thread %d iterating %d times with a delay of %1.4f\n" % (self.threadNum, self.messageCount, self.messageDelay)
        wx.CallAfter(self.window.LogMessage, msg)

        for i in range(1, self.messageCount + 1):
            self.timeToQuit.wait(self.messageDelay)
            if self.timeToQuit.isSet():
                break
            msg = "Message %d from thread %d\n" % (i, self.threadNum)
            wx.CallAfter(self.window.LogMessage, msg)
        else:
            wx.CallAfter(self.window.ThreadFinished, self)


class MemoDialog(wx.Dialog):
    def __init__(self, lib, i):
        wx.Dialog.__init__(self, None, -1, 'Study', size=(-1, 470),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        self.fn = 'recordstack_' + str(i) + '.txt'
        self.n_list = file.fetch_nsr(self.fn, 'N')
        self.s_list = file.fetch_nsr(self.fn, 'S')
        self.r_list = file.fetch_nsr(self.fn, 'R')
        self.flag = 1

        self.panel = wx.Panel(self)
        self.v_box_main = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self.panel, -1, lib[i].encode('utf8'))
        more = wx.BitmapButton(self.panel, -1, wx.Bitmap('images/other-size/more26.png'), style=wx.NO_BORDER)
        line_1 = wx.StaticLine(self.panel, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)

        h_box_title = wx.BoxSizer(wx.HORIZONTAL)
        h_box_title.Add(title, 1, wx.TOP | wx.RIGHT, 10)
        h_box_title.Add(more, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.TOP, 5)

        self.v_box_main.Add(h_box_title, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        self.v_box_main.Add(line_1, 0, wx.EXPAND)

        # ---------------

        self.cl = wx.StaticText(self.panel, -1, "剩余卡片数: 0 0 0")
        h_box_info = wx.BoxSizer(wx.HORIZONTAL)
        h_box_info.Add(self.cl, 1, wx.RIGHT, 10)
        self.v_box_main.Add(h_box_info, 0, wx.EXPAND | wx.ALL, 10)

        # ---------------

        panel_qa = wx.Panel(self.panel, -1, style=wx.BORDER_MASK)
        panel_qa.SetBackgroundColour('white')
        v_box_qa = wx.BoxSizer(wx.VERTICAL)

        self.ques = wx.StaticText(panel_qa, -1, self.n_list[2][2].encode('utf-8'))
        self.ans = wx.StaticText(panel_qa, -1, "")
        line_2 = wx.StaticLine(panel_qa, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)

        v_box_qa.Add(self.ques, 0, wx.LEFT | wx.TOP, 20)
        v_box_qa.Add(line_2, 0, wx.EXPAND | wx.ALL, 10)
        v_box_qa.Add(self.ans, 0, wx.LEFT, 20)
        panel_qa.SetSizer(v_box_qa)
        self.v_box_main.Add(panel_qa, 18, wx.EXPAND | wx.ALL, 10)

        # ----------------
        self.h_box_ans = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_ans = wx.Panel(self.panel, -1)
        # ----------------
        self.h_box_btn_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_btn_2 = wx.Panel(self.panel, -1)
        self.panel_btn_2.SetBackgroundColour('red')
        # ----------------
        self.h_box_btn_3 = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_btn_3 = wx.Panel(self.panel, -1)
        self.panel_btn_3.SetBackgroundColour('blue')
        # ----------------
        self.h_box_btn_4 = wx.BoxSizer(wx.HORIZONTAL)
        self.panel_btn_4 = wx.Panel(self.panel, -1)
        self.panel_btn_4.SetBackgroundColour('green')
        # ----------------
        self.LoadBtn()

        self.panel.SetSizer(self.v_box_main)
        self.Centre()
        self.Show(True)

    def LoadBtn(self):
        if self.flag == 1:
            self.panel_btn_2.Destroy()
            self.panel_btn_3.Destroy()
            self.panel_btn_4.Destroy()
            show_ans = buttons.GenButton(self.panel_ans, -1, "显示答案")
            show_ans.SetBezelWidth(1)
            show_ans.SetBackgroundColour('white')
            self.h_box_ans.Add(show_ans, 1, wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, lambda evt, item=self.n_list[2]: self.OnShowAns(evt, item), show_ans)
            self.panel_ans.SetSizer(self.h_box_ans)
            self.v_box_main.Add(self.panel_ans, 0, wx.EXPAND | wx.ALL, 10)
        elif self.flag == 2:
            self.panel_ans.Destroy()
            self.panel_btn_3.Destroy()
            self.panel_btn_4.Destroy()
            again = buttons.GenButton(self.panel_btn_2, -1, "重来")
            again.SetBezelWidth(1)
            again.SetBackgroundColour('white')
            good = buttons.GenButton(self.panel_btn_2, -1, "一般")
            good.SetBezelWidth(1)
            good.SetBackgroundColour('white')
            self.h_box_btn_2.Add(again, 1, wx.EXPAND)
            self.h_box_btn_2.Add(good, 1, wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, self.OnAgain, again)
            self.Bind(wx.EVT_BUTTON, self.OnGood, good)
            self.panel_btn_2.SetSizer(self.h_box_btn_2)
            self.v_box_main.Add(self.panel_btn_2, 0, wx.EXPAND | wx.ALL, 10)
        elif self.flag == 3:
            self.panel_ans.Destroy()
            self.panel_btn_2.Destroy()
            self.panel_btn_4.Destroy()
            again = buttons.GenButton(self.panel_btn_3, -1, "重来")
            again.SetBezelWidth(1)
            again.SetBackgroundColour('white')
            good = buttons.GenButton(self.panel_btn_3, -1, "一般")
            good.SetBezelWidth(1)
            good.SetBackgroundColour('white')
            easy = buttons.GenButton(self.panel_btn_3, -1, "简单")
            easy.SetBezelWidth(1)
            easy.SetBackgroundColour('white')
            self.h_box_btn_3.Add(again, 1, wx.EXPAND)
            self.h_box_btn_3.Add(good, 1, wx.EXPAND)
            self.h_box_btn_3.Add(easy, 1, wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, self.OnAgain, again)
            self.Bind(wx.EVT_BUTTON, self.OnGood, good)
            self.Bind(wx.EVT_BUTTON, self.OnEasy, easy)
            self.panel_btn_3.SetSizer(self.h_box_btn_3)
            self.v_box_main.Add(self.panel_btn_3, 0, wx.EXPAND | wx.ALL, 10)
        elif self.flag == 4:
            self.panel_ans.Destroy()
            self.panel_btn_3.Destroy()
            self.panel_btn_4.Destroy()
            again = buttons.GenButton(self.panel_btn_4, -1, "重来")
            again.SetBezelWidth(1)
            again.SetBackgroundColour('white')
            hard = buttons.GenButton(self.panel_btn_4, -1, "困难")
            hard.SetBezelWidth(1)
            hard.SetBackgroundColour('white')
            good = buttons.GenButton(self.panel_btn_4, -1, "一般")
            good.SetBezelWidth(1)
            good.SetBackgroundColour('white')
            easy = buttons.GenButton(self.panel_btn_4, -1, "简单")
            easy.SetBezelWidth(1)
            easy.SetBackgroundColour('white')
            self.h_box_btn_4.Add(again, 1, wx.EXPAND)
            self.h_box_btn_4.Add(hard, 1, wx.EXPAND)
            self.h_box_btn_4.Add(good, 1, wx.EXPAND)
            self.h_box_btn_4.Add(easy, 1, wx.EXPAND)
            self.Bind(wx.EVT_BUTTON, self.OnAgain, again)
            self.Bind(wx.EVT_BUTTON, self.OnHard, hard)
            self.Bind(wx.EVT_BUTTON, self.OnGood, good)
            self.Bind(wx.EVT_BUTTON, self.OnEasy, easy)
            self.panel_btn_4.SetSizer(self.h_box_btn_4)
            self.v_box_main.Add(self.panel_btn_4, 0, wx.EXPAND | wx.ALL, 10)

    def OnShowAns(self, evt, i):
        self.SetAnswer(i[3].decode('utf-8'))
        # self.SetFlag(i[8])
        self.flag = 3
        self.LoadBtn()

    def SetQuestion(self, ques):
        self.ques.SetLabel(ques)
        self.SetAnswer("")
        self.SetCardsLeft()

    def SetAnswer(self, ans):
        self.ans.SetLabel(ans)

    def SetFlag(self, ef):
        if float(ef) < 2.5:
            self.flag = 2
        elif float(ef) == 2.5:
            self.flag = 3
        elif float(ef) > 2.5:
            self.flag = 4

    def SetCardsLeft(self):
        dic = file.fetch_statistic(self.fn)
        self.cl.SetLabel("剩余卡片数: %d %d %d" % (dic['N'], dic['S'], dic['R']))

    def FetchACard(self, nsr):
        if nsr == 'N':
            return self.n_list.pop(0)
        elif nsr == 'S':
            return self.s_list.pop(0)
        elif nsr == 'R':
            return self.r_list.pop(0)

    def OnAgain(self, evt):
        pass

    def OnHard(self, evt):
        pass

    def OnGood(self, evt):
        pass

    def OnEasy(self, evt):
        pass


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Multi-threaded GUI")
        panel = wx.Panel(self)
        main = wx.BoxSizer(wx.VERTICAL)
        startBtn = wx.Button(panel, -1, "Start")
        main.Add(startBtn, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 15)
        startBtn.Bind(wx.EVT_BUTTON, self.OnStart, startBtn)
        panel.SetSizer(main)

    def OnStart(self, evt):
        lib = {'001': 'CET-4'}
        i = '001'
        memo_dlg = MemoDialog(lib, i)
        memo_dlg.ShowModal()
        memo_dlg.Destroy()

app = wx.PySimpleApp()
frm = MyFrame()
frm.Show()
app.MainLoop()