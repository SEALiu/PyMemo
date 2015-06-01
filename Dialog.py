# -*- coding: utf-8 -*-
import time
import os
import os.path
import wx
import wx.lib.buttons as buttons
import file
import math
from memo import *


# Lib Dialog
class AddNewLib(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '新建词库', size=(-1, 270),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        v_box = wx.BoxSizer(wx.VERTICAL)
        name_text = wx.StaticText(panel, -1, "词库名称：")
        lib_name = wx.TextCtrl(panel, -1, "", style=wx.TE_CAPITALIZE)

        desc_text = wx.StaticText(panel, -1, "词库描述：")
        lib_desc = wx.TextCtrl(panel, -1, "", size=(-1, 80), style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, -1, label='确定')
        cancel_button = wx.Button(panel, wx.ID_CANCEL, label='取消')
        self.Bind(wx.EVT_BUTTON, lambda evt, name=lib_name, desc=lib_desc: self.on_submit(evt, name, desc), ok_button)
        h_box.Add(ok_button, 1, wx.RIGHT, border=5)
        h_box.Add(cancel_button, 1)

        v_box.Add(name_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        v_box.Add(lib_name, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(desc_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(lib_desc, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(h_box, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    def on_submit(self, evt, name, desc):
        lib_name = name.GetValue().encode('utf-8')
        lib_desc = desc.GetValue().encode('utf-8')

        next_lib_id = DBFun.max_lib('libId') + 1
        lib_id = str(next_lib_id).zfill(3)
        create_time = time.strftime('%Y/%m/%d', time.localtime(time.time()))

        insert_lib_sql = "INSERT INTO library(libId, name, libDesc, createTime) VALUES ('" + lib_id + "', '" + lib_name + "', '" +\
                         lib_desc + "', '" + create_time + "')"

        DBFun.update('db_pymemo.db', insert_lib_sql)
        ListCtrlLeft.on_refresh()
        self.Close()


class RenameLib(wx.Dialog):
    def __init__(self, old_name, old_desc, lib_id):
        wx.Dialog.__init__(self, None, -1, '修改' + old_name + '名称和描述', size=(-1, 270),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        v_box = wx.BoxSizer(wx.VERTICAL)

        name_text = wx.StaticText(panel, -1, "词库名称：")
        lib_name = wx.TextCtrl(panel, -1, old_name, style=wx.TE_CAPITALIZE)

        desc_text = wx.StaticText(panel, -1, "词库描述：")
        lib_desc = wx.TextCtrl(panel, -1, old_desc, size=(-1, 80), style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, -1, label='确定')
        cancel_button = wx.Button(panel, wx.ID_CANCEL, label='取消')
        self.Bind(wx.EVT_BUTTON,
                  lambda evt, name=lib_name, desc=lib_desc, i=lib_id: self.on_submit(evt, name, desc, i),
                  ok_button)
        h_box.Add(ok_button, 1, wx.RIGHT, border=5)
        h_box.Add(cancel_button, 1)

        v_box.Add(name_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        v_box.Add(lib_name, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(desc_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(lib_desc, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(h_box, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    def on_submit(self, evt, name, desc, i):
        lib_name = name.GetValue().encode('utf-8')
        lib_desc = desc.GetValue().encode('utf-8')
        update_lib_sql = "UPDATE library SET " \
                         "name = '" + lib_name + "', libDesc = '" + lib_desc + "' WHERE libId = '" + i + "'"

        DBFun.update('db_pymemo.db', update_lib_sql)
        ListCtrlLeft.on_refresh()
        self.Close()


class LibInfo(wx.Dialog):
    def __init__(self, lib_info):
        wx.Dialog.__init__(self, None, -1, lib_info[1].decode('utf-8') + '词库的信息', size=(-1, 300),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)

        v_box = wx.BoxSizer(wx.VERTICAL)

        panel = wx.Panel(self, -1, style=wx.BORDER_MASK)
        panel.SetBackgroundColour('white')
        v_box_panel = wx.BoxSizer(wx.VERTICAL)
        lib_id = wx.StaticText(panel, -1, '词库ID：' + lib_info[0])
        name_text = wx.StaticText(panel, -1, '词库名称：' + lib_info[1].decode('utf-8'))
        desc_text = wx.StaticText(panel, -1, '词库描述：' + lib_info[2].decode('utf-8'))
        create_time = wx.StaticText(panel, -1, '创建时间：' + str(lib_info[3]))
        max_reviews = wx.StaticText(panel, -1, '每日复习：' + str(lib_info[4]))
        max_new = wx.StaticText(panel, -1, '每日学习：' + str(lib_info[5]))
        easy_interval = wx.StaticText(panel, -1, '简单间隔：' + str(lib_info[6]) + '（天）' )
        max_interval = wx.StaticText(panel, -1, '最大间隔：' + str(lib_info[7]) + '（天）')
        is_Show_Rest = wx.StaticText(panel, -1, '是否显示剩余卡片：' + lib_info[-1])


        v_box_panel.Add(lib_id, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        v_box_panel.Add(name_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(desc_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(create_time, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(max_reviews, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(max_new, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(easy_interval, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(max_interval, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(is_Show_Rest, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        panel.SetSizer(v_box_panel)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, wx.ID_OK, label='确定')
        h_box.Add(ok_button, 1, wx.RIGHT, border=5)

        v_box.Add(panel, 1, wx.EXPAND | wx.ALL, 10)
        v_box.Add(h_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        self.SetSizer(v_box)
        self.Centre()
        self.Show(True)


class DeleteLib(wx.Dialog):
    def __init__(self, lib_name, lib_id):
        wx.Dialog.__init__(self, None, -1, '删除' + lib_name + '词库', size=(-1, 180),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('white')
        v_box = wx.BoxSizer(wx.VERTICAL)
        info_text = wx.StaticText(panel, -1, lib_name + '词库将被删除，词库中的记录会被转移至孤儿院。\n你确定要这样做么？')
        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, -1, label='确定')
        self.Bind(wx.EVT_BUTTON, lambda evt, i=lib_id: self.on_delete(evt, i), ok_button)
        cancel_button = wx.Button(panel, wx.ID_CANCEL, label='取消')
        h_box.Add(ok_button, 1, wx.RIGHT, border=5)
        h_box.Add(cancel_button, 1)

        v_box.Add(info_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP , 20)
        v_box.Add(h_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)

        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    def on_delete(self, evt, i):
        delete_lib_sql = "DELETE FROM library WHERE libId='" + i + "'"
        update_record_sql = "UPDATE record SET recordId = replace(recordId, substr(recordId, 6, 3), '000') WHERE recordId LIKE '%" + i + "'"
        DBFun.update('db_pymemo.db', delete_lib_sql)
        DBFun.update('db_pymemo.db', update_record_sql)
        ListCtrlLeft.on_refresh()
        ListCtrlRight.on_refresh()
        f = 'recordstack_' + str(i) + '.txt'
        if os.path.exists(f):
            os.remove(f)
        self.Close()


# Record Dialog
class RecordInfo(wx.Dialog):
    def __init__(self, detail):
        wx.Dialog.__init__(self, None, -1, '记录的信息', size=(-1, 300),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)

        v_box = wx.BoxSizer(wx.VERTICAL)

        panel = wx.Panel(self, -1, style=wx.BORDER)
        panel.SetBackgroundColour('white')
        v_box_panel = wx.BoxSizer(wx.VERTICAL)
        lib_id = wx.StaticText(panel, -1, '记录ID：' + detail[0][0:5])
        name_text = wx.StaticText(panel, -1, '词库ID：' + detail[0][5:])
        desc_text = wx.StaticText(panel, -1, '问题（正面）：' + detail[1].decode('utf-8'))
        create_time = wx.StaticText(panel, -1, '答案（反面）：' + detail[2].decode('utf-8'))
        max_reviews = wx.StaticText(panel, -1, '添加时间：' + detail[3].decode('utf-8'))
        max_new = wx.StaticText(panel, -1, '复习时间：' + str(detail[4]).decode('utf-8'))
        easy_interval = wx.StaticText(panel, -1, '修改时间：' + str(detail[5]).decode('utf-8'))
        max_interval = wx.StaticText(panel, -1, '间隔：' + str(detail[6]) + '（天）')
        max_time = wx.StaticText(panel, -1, 'E-Factor：' + str(detail[7]))
        is_show_timer = wx.StaticText(panel, -1, '是否挂起：' + detail[8])

        v_box_panel.Add(lib_id, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        v_box_panel.Add(name_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(desc_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(create_time, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(max_reviews, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(max_new, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(easy_interval, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(max_interval, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(max_time, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_panel.Add(is_show_timer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        panel.SetSizer(v_box_panel)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        close_button = wx.Button(self, wx.ID_CANCEL, label='关闭')
        h_box.Add(close_button, 1, wx.RIGHT, border=5)

        v_box.Add(panel, 1, wx.EXPAND | wx.ALL, 10)
        v_box.Add(h_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        self.SetSizer(v_box)
        self.Centre()
        self.Show(True)


class UpdateRecord(wx.Dialog):
    def __init__(self, detail):
        wx.Dialog.__init__(self, None, -1, '修改记录', size=(-1, 260),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        v_box = wx.BoxSizer(wx.VERTICAL)

        ques_text = wx.StaticText(panel, -1, "问题（正面）：")
        record_ques = wx.TextCtrl(panel, -1,
                                  detail[1].decode('utf-8'),
                                  size=(-1, 50),
                                  style=wx.TE_MULTILINE)

        ans_text = wx.StaticText(panel, -1, "答案（反面）：")
        record_ans = wx.TextCtrl(panel, -1,
                                 detail[2].decode('utf-8'),
                                 size=(-1, 50),
                                 style=wx.TE_MULTILINE)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, -1, label='修改')
        self.Bind(wx.EVT_BUTTON,
                  lambda evt, ques=record_ques, ans=record_ans, i=detail[0]:
                  self.on_submit(evt, ques, ans, i),
                  ok_button)

        cancel_button = wx.Button(panel, wx.ID_CANCEL, label='取消')

        h_box.Add(ok_button, 1, wx.RIGHT, border=5)
        h_box.Add(cancel_button, 1)

        v_box.Add(ques_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        v_box.Add(record_ques, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(ans_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(record_ans, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(h_box, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    def on_submit(self, e, q, a, i):
        ques = q.GetValue().encode('utf-8')
        ans = a.GetValue().encode('utf-8')
        alert_time = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        update_record_sql = "UPDATE record SET" \
                            " ques = '" + ques + "', ans = '" + ans + "', alertTime = '" + alert_time + "' WHERE" \
                            " recordId = '" + i + "'"
        DBFun.update('db_pymemo.db', update_record_sql)
        ListCtrlRight.on_refresh()
        self.Close()


class AddNewRecord(wx.Dialog):
    def __init__(self, LIBRARIES, flag):
        wx.Dialog.__init__(self, None, -1, '增加一条记录', size=(-1, 350),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        self.lib_id = -1
        v_box = wx.BoxSizer(wx.VERTICAL)
        h_box_info = wx.BoxSizer(wx.HORIZONTAL)

        lib_items = ['请选择词库']
        for index, element in enumerate(LIBRARIES):
            lib_items.append(LIBRARIES[element].decode('utf-8'))

        lib_combo_box = wx.ComboBox(panel, choices=lib_items, style=wx.CB_READONLY)

        # 逆转LIBRARIES字典，以便于根据词库名称获取词库的ID，避免访问数据库。
        reverse_lib = {v: k for k, v in LIBRARIES.items()}
        self.Bind(wx.EVT_COMBOBOX, lambda evt, ob=lib_combo_box, lib=reverse_lib: self.test(evt, ob, lib), lib_combo_box)
        if flag == -1:
            lib_index = 0
        else:
            lib_index = lib_items.index(LIBRARIES[flag].decode('utf-8'))
            self.set_lib_id(str(flag).zfill(3))
        lib_combo_box.SetSelection(lib_index)
        # preview = wx.BitmapButton(panel, -1, wx.Bitmap('images/32/preview.png'), size=(32, 32), style=wx.NO_BORDER)
        h_box_info.Add(lib_combo_box, 1, wx.TOP, 10)
        # h_box_info.Add(preview, 0, wx.ALIGN_RIGHT | wx.TOP, 6)

        name_text = wx.StaticText(panel, -1, "问题（正面）：")
        self.record_ques = wx.TextCtrl(panel, -1, "", size=(-1, 80), style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

        desc_text = wx.StaticText(panel, -1, "答案（反面）：")
        self.record_ans = wx.TextCtrl(panel, -1, "", size=(-1, 80), style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

        h_box_btn = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, -1, label='确定')
        close_button = wx.Button(panel, wx.ID_CANCEL, label='取消')

        self.Bind(wx.EVT_BUTTON, lambda evt, ques=self.record_ques, ans=self.record_ans: self.on_submit(evt, ques, ans), ok_button)
        h_box_btn.Add(ok_button, 1, wx.RIGHT, border=5)
        h_box_btn.Add(close_button, 1)

        v_box.Add(h_box_info, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(name_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        v_box.Add(self.record_ques, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(desc_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(self.record_ans, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(h_box_btn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    def set_lib_id(self, value):
        self.lib_id = value

    def get_lib_id(self):
        return self.lib_id

    def on_submit(self, evt, ques, ans):
        if self.get_lib_id() == -1:
            msg_dlg = wx.MessageDialog(self, '请确保选择了一个词库！',
                           '提示',
                           wx.OK | wx.ICON_WARNING)
            msg_dlg.ShowModal()
            msg_dlg.Destroy()
        else:
            record_ques = ques.GetValue().encode('utf-8')
            record_ans = ans.GetValue().encode('utf-8')
            self.record_ques.SetValue('')
            self.record_ans.SetValue('')
            next_record_id = DBFun.max_record('recordId') + 1
            record_id = str(next_record_id).zfill(5) + self.get_lib_id()
            # 重置，避免第二次由于 self.get_lib_id() != -1, 导致没有选择词库也可以插入记录。
            self.set_lib_id(-1)
            # addTime: type is str
            add_time = time.strftime('%Y/%m/%d', time.localtime(time.time()))
            insert_sql = "INSERT INTO record(recordId, ques, ans, addTime) VALUES" \
                         " ('" + record_id + "', '" + record_ques + "', '" + record_ans + "', '" + add_time + "')"

            DBFun.update('db_pymemo.db', insert_sql)
            ListCtrlRight.on_refresh()


    def test(self, evt, ob, lib):
        lib_name = ob.GetValue().encode('utf-8')
        if lib_name in lib.keys():
            self.set_lib_id(lib[lib_name])
        else:
            self.set_lib_id(-1)


class DeleteRecord(wx.Dialog):
    def __init__(self, detail):
        wx.Dialog.__init__(self, None, -1, '挂起/删除记录', size=(-1, 160),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        v_box = wx.BoxSizer(wx.VERTICAL)
        info_text = wx.StaticText(panel, -1,
                                  '当你挂起这个记录之后，它的学习过程不会被重置。取消挂起之后继续学习'
                                  '\n删除记录后，该记录将永久消失！')
        h_box = wx.BoxSizer(wx.HORIZONTAL)

        delete_button = wx.Button(panel, -1, label='删除')
        cancel_button = wx.Button(panel, wx.ID_CANCEL, label='取消')

        self.Bind(wx.EVT_BUTTON, lambda evt, i=detail[0]: self.on_delete(evt, i), delete_button)

        if detail[-1] == 'True':
            play_button = wx.Button(panel, -1, label='取消挂起')
            self.Bind(wx.EVT_BUTTON, lambda evt, i=detail[0], flag='False': self.on_is_pause(evt, i, flag), play_button)
            h_box.Add(play_button, 1, wx.RIGHT, border=5)
        else:
            pause_button = wx.Button(panel, -1, label='挂起')
            self.Bind(wx.EVT_BUTTON, lambda evt, i=detail[0], flag='True': self.on_is_pause(evt, i, flag), pause_button)
            h_box.Add(pause_button, 1, wx.RIGHT, border=5)

        h_box.Add(delete_button, 1, wx.RIGHT, border=5)
        h_box.Add(cancel_button, 1)

        v_box.Add(info_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)
        v_box.Add(h_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)

        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    def on_is_pause(self, evt, i, flag):
        alert_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        pause_sql = "UPDATE record SET alertTime = '" + alert_time + "', isPaused = '" + flag + "'  WHERE recordId = '" + i + "'"

        DBFun.update('db_pymemo.db', pause_sql)
        ListCtrlRight.on_refresh()
        self.Close()

    def on_delete(self, evt, i):
        delete_sql = "DELETE FROM record WHERE recordId = '" + i + "'"
        DBFun.update('db_pymemo.db', delete_sql)
        ListCtrlRight.on_refresh()
        ListCtrlRight.on_refresh()
        self.Close()


# Other Dialogs
class AboutDialog(wx.AboutDialogInfo):
    def __init__(self):
        wx.AboutDialogInfo.__init__(self)
        description = "这是我的毕业设计成果，《基于Python的单词记忆软件开发》\n\n" \
            "GUI库：wxpython 2.7.9\n" \
            "IDE：pyCharm Community Edition 4.0.4\n" \
            "DB：SQLite3\n\n"\
            "向所有给予帮助，提出建议，报告Bug的人们致谢！\n\n" \
            "联系：iliuyang@foxmail.com"
        licence = """PyMemo is free software; you can redistribute
it and/or modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.
翻译：PyMemo是个开源软件，你可以基于GNU随便修改和二次发行。

PyMemo is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
翻译：但是我不负责软件的可靠性。（大概就这意思！）

"""

        self.SetIcon(wx.Icon('images/64/PyMemo_logo_white.png', wx.BITMAP_TYPE_PNG))
        self.SetName("PyMemo")
        self.SetVersion('1.0')
        self.SetDescription(description)
        self.WebSite = ("https://github.com/SEALiu/PyMemo", "Code on GitHub")
        self.SetCopyright('(c)2015 刘洋')
        self.Developers = ["刘洋"]
        self.Artists = ["刘洋", "图标部分来自：http://findicons.com/"]
        self.SetLicence(licence)
        wx.AboutBox(self)


class SettingDialog(wx.Dialog):
    def __init__(self, LIBRARIES, flag):
        wx.Dialog.__init__(self, None, -1, '词库设置', size=(400, 240),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)

        self.lib_id = -1
        self.old_setting = []
        panel = wx.Panel(self)
        v_box = wx.BoxSizer(wx.VERTICAL)
        h_box_combo = wx.BoxSizer(wx.HORIZONTAL)

        panel_combo = wx.Panel(panel)
        # global lib_index
        lib_items = ['请选择词库']
        for index, element in enumerate(LIBRARIES):
            lib_items.append(LIBRARIES[element].decode('utf-8'))

        lib_text = wx.StaticText(panel_combo, -1, "选择设置词库：")
        lib_combo_box = wx.ComboBox(panel_combo, choices=lib_items, style=wx.CB_READONLY)

        # 逆转LIBRARIES字典，以便于根据词库名称获取词库的ID，避免访问数据库。
        reverse_lib = {v: k for k, v in LIBRARIES.items()}
        self.Bind(wx.EVT_COMBOBOX, lambda evt, ob=lib_combo_box, lib=reverse_lib: self.test(evt, ob, lib), lib_combo_box)

        if flag == -1:
            lib_combo_box.SetSelection(0)
        else:
            lib_index = lib_items.index(LIBRARIES[flag].decode('utf-8'))
            lib_combo_box.SetSelection(lib_index)
            self.lib_id = str(flag).zfill(3)
            self.old_setting = self.fetch_setting(self.lib_id)

        h_box_combo.Add(lib_text, 0, wx.ALIGN_CENTER_VERTICAL)
        h_box_combo.Add(lib_combo_box, 0, wx.LEFT | wx.RIGHT, 10)

        panel_combo.SetSizer(h_box_combo)
        v_box.Add(panel_combo, 0, wx.EXPAND | wx.ALL, 10)
        line_1 = wx.StaticLine(panel, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)
        v_box.Add(line_1, 0, wx.EXPAND)

        panel_top = wx.Panel(panel, -1, style=wx.BORDER_MASK)
        panel_top.SetBackgroundColour('white')
        v_box_t = wx.BoxSizer(wx.VERTICAL)
        h_box_g1 = wx.BoxSizer(wx.HORIZONTAL)
        h_box_g2 = wx.BoxSizer(wx.HORIZONTAL)

        self.show_rest = wx.CheckBox(panel_top,
                            label='在复习的时候显示剩余卡片数',
                            style=wx.CHK_3STATE)
        if self.old_setting:
            if self.old_setting[2] == 'True':
                self.show_rest.SetValue(True)
            elif self.old_setting[2] == 'False':
                self.show_rest.SetValue(False)
        else:
            self.show_rest.SetValue(True)

        text1 = wx.StaticText(panel_top, label="每日学习卡片上限（张）")
        text2 = wx.StaticText(panel_top, label="每日复习卡片上限（张）")

        self.study_limit = wx.SpinCtrl(panel_top, -1)
        self.study_limit.SetRange(1, 200)
        if self.old_setting:
            self.study_limit.SetValue(int(self.old_setting[1]))
        else:
            self.study_limit.SetValue(50)

        self.review_limit = wx.SpinCtrl(panel_top, -1)
        self.review_limit.SetRange(1, 200)
        if self.old_setting:
            self.review_limit.SetValue(int(self.old_setting[0]))
        else:
            self.review_limit.SetValue(50)

        h_box_g1.Add(text1, 0, wx.ALIGN_CENTER_VERTICAL)
        h_box_g1.Add(self.study_limit, 0, wx.LEFT, 15)

        h_box_g2.Add(text2, 0)
        h_box_g2.Add(self.review_limit, 0, wx.LEFT, 15)

        v_box_t.Add(self.show_rest, 0, wx.LEFT | wx.TOP, 10)
        v_box_t.Add(h_box_g1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        v_box_t.Add(h_box_g2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, 10)

        panel_top.SetSizer(v_box_t)
        v_box.Add(panel_top, 0, wx.EXPAND | wx.ALL, 10)

        # ----------
        h_box_btn = wx.BoxSizer(wx.HORIZONTAL)

        ok_button = buttons.GenButton(panel, -1, "确定")
        ok_button.SetBezelWidth(1)
        ok_button.SetBackgroundColour('white')

        close_button = buttons.GenButton(panel, -1, "关闭")
        close_button.SetBezelWidth(1)
        close_button.SetBackgroundColour('white')

        h_box_btn.Add(ok_button, 1)
        h_box_btn.Add(close_button, 1, wx.LEFT, 10)

        v_box.Add(h_box_btn, 0, wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, border=10)

        ok_button.Bind(wx.EVT_BUTTON, self.OnSubmit)
        close_button.Bind(wx.EVT_BUTTON, self.on_close)

        panel.SetSizer(v_box)
        self.Centre()

    def test(self, evt, ob, lib):
        lib_name = ob.GetValue().encode('utf-8')
        if lib_name in lib.keys():
            self.lib_id = lib[lib_name]
        else:
            self.lib_id = -1

    def on_close(self, e):
        self.Destroy()

    def OnSubmit(self, evt):
        if self.lib_id == -1:
            msg_dlg = wx.MessageDialog(self, '请确保选择了一个词库！',
                           '提示',
                           wx.OK | wx.ICON_WARNING)
            msg_dlg.ShowModal()
            msg_dlg.Destroy()
        else:
            if self.show_rest.GetValue():
                sr = 'True'
            else:
                sr = 'False'
            sl = str(self.study_limit.GetValue())
            rl = str(self.review_limit.GetValue())
            li = self.lib_id
            sql = "UPDATE library SET " \
                         "maxReviewsPerDay = '" + rl + "', newCardsPerDay = '" + sl + "', isShowRest = '" + sr + "' " \
                         "WHERE libId = '" + li + "'"
            DBFun.update('db_pymemo.db', sql)
            # 重置，避免第二次由于 self.get_lib_id() != -1, 导致没有选择词库也可以插入记录。
            self.lib_id = -1
            self.Close()

    def fetch_setting(self, i):
        ls = []
        select_sql = "SELECT * FROM library WHERE libId = '" + i + "'"
        result_list = DBFun.select('db_pymemo.db', select_sql)
        for rows in result_list:
            ls.append(rows[4])
            ls.append(rows[5])
            ls.append(rows[-3])
        return ls


class Export(wx.DirDialog):
    def __init__(self, parent):
        wx.DirDialog.__init__(self, parent, "请选择一个文件来保存导出的词库：",
                          style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        self.CentreOnParent()
        self.Show(True)


class Import(wx.FileDialog):
    def __init__(self, parent):
        wx.FileDialog.__init__(self, parent, "选择导入的词库文件",
                               wildcard="BMP and GIF files (*.bmp*.gif)|*.bmp*.gif|PNG files (*.png)|*.png",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_CHANGE_DIR
                               )
        self.Centre()
        self.Show(True)


class Check(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '优化数据库', size=(400, 370),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self)
        v_box = wx.BoxSizer(wx.VERTICAL)

        # -----------
        h_box = wx.BoxSizer(wx.HORIZONTAL)

        check_button = buttons.GenButton(panel, -1, "开始优化")
        check_button.SetBezelWidth(1)
        check_button.SetBackgroundColour('white')
        check_button.Bind(wx.EVT_BUTTON, self.OnCheck)

        cancel_button = buttons.GenButton(panel, wx.ID_CANCEL, "取消")
        cancel_button.SetBezelWidth(1)
        cancel_button.SetBackgroundColour('white')

        h_box.Add(check_button, 1, wx.EXPAND)
        h_box.Add(cancel_button, 1, wx.EXPAND | wx.LEFT, 10)
        line = wx.StaticLine(panel, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)

        v_box.Add(h_box, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(line, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 10)

        # -----------
        text = "优化数据库是指：\n清除空卡片\n重置由于程序错误或设置不当造成信息错乱的词库\n点击开始优化按钮进行优化"
        self.tc = wx.TextCtrl(panel, -1, text, style=wx.TE_RICH | wx.TE_MULTILINE | wx.TE_READONLY)
        v_box.Add(self.tc, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(v_box)
        self.Center()

    def OnCheck(self, evt):
        ls = []
        self.tc.Clear()
        self.tc.AppendText("开始清除空卡片...\n\n")
        num = self.ClearBlank()
        self.tc.AppendText("成功清除空卡片" + str(num) + '张！\n\n')
        self.tc.AppendText("开始重置由于程序运行错误或设置不当信息错乱的词库...\n\n")
        ls = self.Reset()
        self.tc.AppendText("成功重置容易间隔少于3天的词库" + str(ls[0]) + '个！\n')
        self.tc.AppendText("成功重置最大间隔多于10年的词库" + str(ls[1]) + '个！\n')
        self.tc.AppendText("成功重置每日最大复习数量大于200的词库" + str(ls[2]) + '个！\n')
        self.tc.AppendText("成功重置每日最大学习数量大于200的词库" + str(ls[3]) + '个！\n\n')
        self.tc.AppendText('数据库已经保持最佳运行状态！\n')

    @staticmethod
    def ClearBlank():
        sql = "DELETE FROM record WHERE ques='' OR ans=''"
        num = DBFun.update('db_pymemo.db', sql)
        ListCtrlRight.on_refresh()
        return num

    @staticmethod
    def Reset():
        sql1 = "UPDATE library SET easyInterval = 3 WHERE easyInterval < 3"
        sql2 = "UPDATE library SET maxInterval = 3650 WHERE maxInterval > 3650"
        sql3 = "UPDATE library SET maxReviewsPerDay = 50 WHERE maxReviewsPerDay > 200"
        sql4 = "UPDATE library SET newCardsPerDay = 50 WHERE newCardsPerDay > 200"

        ei_num = DBFun.update('db_pymemo.db', sql1)
        mi_num = DBFun.update('db_pymemo.db', sql2)
        mrpd_num = DBFun.update('db_pymemo.db', sql3)
        ncpd_num = DBFun.update('db_pymemo.db', sql4)
        ListCtrlLeft.on_refresh()
        return [ei_num, mi_num, mrpd_num, ncpd_num]


# Study Dialogs
class MemoDialog(wx.Dialog):
    def __init__(self, lib, i):
        wx.Dialog.__init__(self, None, -1, 'Study', size=(-1, 470),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        self.fn = 'recordstack_' + str(i) + '.txt'
        self.n_list = file.fetch_nsr(self.fn, 'N')
        self.s_list = file.fetch_nsr(self.fn, 'S')
        self.r_list = file.fetch_nsr(self.fn, 'R')
        self.done = []
        self.undone = []
        self.lib = lib
        self.i = i

        self.panel = wx.Panel(self)
        v_box_main = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self.panel, -1, lib[i].encode('utf8'))
        more = wx.BitmapButton(self.panel, -1, wx.Bitmap('images/other-size/more26.png'), style=wx.NO_BORDER)
        line_1 = wx.StaticLine(self.panel, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)

        h_box_title = wx.BoxSizer(wx.HORIZONTAL)
        h_box_title.Add(title, 1, wx.TOP | wx.RIGHT, 10)
        h_box_title.Add(more, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.TOP, 5)

        v_box_main.Add(h_box_title, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box_main.Add(line_1, 0, wx.EXPAND)

        # ---------------
        dic = file.fetch_statistic(self.fn)
        self.cl = wx.StaticText(self.panel, -1, "剩余卡片数: %d %d %d" % (dic['N'], dic['S'], dic['R']))
        h_box_info = wx.BoxSizer(wx.HORIZONTAL)
        h_box_info.Add(self.cl, 1, wx.RIGHT, 10)
        v_box_main.Add(h_box_info, 0, wx.EXPAND | wx.ALL, 10)

        # ---------------

        panel_qa = wx.Panel(self.panel, -1, style=wx.BORDER_MASK)
        panel_qa.SetBackgroundColour('white')
        v_box_qa = wx.BoxSizer(wx.VERTICAL)

        # 当前显示的卡片的详细信息
        self.nrs_list = self.fetch()

        self.ques = wx.StaticText(panel_qa, -1, self.nrs_list[2].encode('utf-8'))
        self.ans = wx.StaticText(panel_qa, -1, "")
        line_2 = wx.StaticLine(panel_qa, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)

        v_box_qa.Add(self.ques, 0, wx.LEFT | wx.TOP, 20)
        v_box_qa.Add(line_2, 0, wx.EXPAND | wx.ALL, 10)
        v_box_qa.Add(self.ans, 0, wx.LEFT, 20)
        panel_qa.SetSizer(v_box_qa)
        v_box_main.Add(panel_qa, 18, wx.EXPAND | wx.ALL, 10)

        # ----------------
        self.panel_btn = wx.Panel(self.panel, -1)
        v_box_btn = wx.BoxSizer(wx.VERTICAL)
        h_box_btn = wx.BoxSizer(wx.HORIZONTAL)

        self.show_ans = buttons.GenButton(self.panel_btn, -1, "显示答案")
        self.show_ans.SetBezelWidth(1)
        self.show_ans.SetBackgroundColour('white')
        self.show_ans.Enable()

        line_3 = wx.StaticLine(self.panel_btn, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)

        self.again = buttons.GenButton(self.panel_btn, -1, "重来")
        self.again.SetBezelWidth(1)
        self.again.SetBackgroundColour('white')
        self.again.Disable()

        self.hard = buttons.GenButton(self.panel_btn, -1, "困难")
        self.hard.SetBezelWidth(1)
        self.hard.SetBackgroundColour('white')
        self.hard.Disable()

        self.good = buttons.GenButton(self.panel_btn, -1, "一般")
        self.good.SetBezelWidth(1)
        self.good.SetBackgroundColour('white')
        self.good.Disable()

        self.easy = buttons.GenButton(self.panel_btn, -1, "简单")
        self.easy.SetBezelWidth(1)
        self.easy.SetBackgroundColour('white')
        self.easy.Disable()

        self.show_ans.Bind(wx.EVT_BUTTON, self.OnShowAns)
        self.again.Bind(wx.EVT_BUTTON, self.OnAgain)
        self.hard.Bind(wx.EVT_BUTTON, self.OnHard)
        self.good.Bind(wx.EVT_BUTTON, self.OnGood)
        self.easy.Bind(wx.EVT_BUTTON, self.OnEasy)

        h_box_btn.Add(self.again, 1, wx.RIGHT, 5)
        h_box_btn.Add(self.hard, 1, wx.RIGHT, 5)
        h_box_btn.Add(self.good, 1, wx.RIGHT, 5)
        h_box_btn.Add(self.easy, 1, wx.RIGHT, 5)

        v_box_btn.Add(self.show_ans, 1, wx.EXPAND)
        v_box_btn.Add(line_3, 1, wx.EXPAND)
        v_box_btn.Add(h_box_btn, 1, wx.EXPAND)
        self.panel_btn.SetSizer(v_box_btn)

        v_box_main.Add(self.panel_btn, 0, wx.EXPAND | wx.ALL, 10)

        self.panel.SetSizer(v_box_main)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Centre()
        self.Show(True)

    def OnShowAns(self, evt):
        self.SetAnswer(self.nrs_list[3].encode('utf-8'))
        self.SetBtnAble(self.nrs_list[8])
        self.show_ans.Disable()

    def NextCard(self):
        self.nrs_list = self.fetch()
        if self.nrs_list:
            self.ques.SetLabel(self.nrs_list[2].encode('utf-8'))
            self.SetAnswer('')
            self.show_ans.Enable()
            self.again.Disable()
            self.hard.Disable()
            self.good.Disable()
            self.easy.Disable()
            self.SetCardsLeft()
        else:
            # 任务完成
            # 写入数据库
            self.write_db()
            # reset recordstack_xxx.txt
            file.reset_nsr(self.fn)
            # 显示任务完成页面
            self.Destroy()
            prepare_dlg = Prepare(self.i, self.lib)
            # 刷新卡片记录界面
            ListCtrlRight.on_refresh()
            pass

    def SetAnswer(self, ans):
        self.ans.SetLabel(ans)

    def SetBtnAble(self, ef):
        if float(ef) < 2.5:
            self.again.Enable()
            self.good.Enable()
        elif float(ef) == 2.5:
            self.again.Enable()
            self.good.Enable()
            self.easy.Enable()
        elif float(ef) > 2.5:
            self.again.Enable()
            self.hard.Enable()
            self.good.Enable()
            self.easy.Enable()

    def SetCardsLeft(self):
        dic = file.fetch_statistic(self.fn)
        self.cl.SetLabel("剩余卡片数: %d %d %d" % (len(self.n_list), len(self.s_list), len(self.r_list)))

    def OnAgain(self, evt):
        self.nrs_list[-2] = self.ef(self.nrs_list[-2], 0)
        self.nrs_list[-3] = self.interval(self.nrs_list[-2], self.nrs_list[-3], 0)
        self.nrs_list[0] = 'S'
        self.s_list.append(self.nrs_list)
        if self.undone.count(self.nrs_list) == 0:
            self.undone.append(self.nrs_list)
        self.NextCard()

    def OnHard(self, evt):
        self.nrs_list[-2] = self.ef(self.nrs_list[-2], 3)
        self.nrs_list[-3] = self.interval(self.nrs_list[-2], self.nrs_list[-3], 3)
        self.nrs_list[0] = 'S'
        self.s_list.append(self.nrs_list)
        self.undone.append(self.nrs_list)
        self.NextCard()

    def OnGood(self, evt):
        self.nrs_list[-2] = self.ef(self.nrs_list[-2], 4)
        self.nrs_list[-3] = self.interval(self.nrs_list[-2], self.nrs_list[-3], 4)
        self.nrs_list[0] = 'R'
        self.done.append(self.nrs_list)
        self.NextCard()

    def OnEasy(self, evt):
        self.nrs_list[-2] = self.ef(self.nrs_list[-2], 5)
        self.nrs_list[-3] = self.interval(self.nrs_list[-2], self.nrs_list[-3], 5)
        self.nrs_list[0] = 'R'
        self.done.append(self.nrs_list)
        self.NextCard()

    @staticmethod
    def ef(ef, q):
        new_ef = float(ef) - 0.8 + 0.28 * q - 0.02 * q ** 2
        if new_ef < 1.3:
            new_ef = 1.3
        return str(new_ef)

    @staticmethod
    def interval(ef, interval, q):
        interval_i = math.ceil(float(interval))
        if interval_i == -1:
            # N
            if q == 0:
                return '0'
            elif q == 4:
                return '1'
            elif q == 5:
                return '3'
        elif interval_i == 0:
            # S
            if q == 0:
                return '0'
            elif q == 4:
                return '1'
        else:
            # R
            if q == 0:
                return '0'
            else:
                return str(math.ceil(interval_i * float(ef)))

    def fetch(self):
        if self.n_list:
            return list(self.n_list.pop(0))
        elif self.r_list:
            return list(self.r_list.pop(0))
        elif self.s_list:
            return list(self.s_list.pop(0))
        else:
            return False

    def OnClose(self, evt):
        # 将现在的self.n_list, self.r_list, self.s_list写入recordstack_xxx.txt
        file.reset_nsr(self.fn)

        # 关闭时当前显示的卡片被弹出（pop）但是却没有给出评价，需要让其回到原来的list
        if self.nrs_list[0] == 'N':
            self.n_list.append(self.nrs_list)
        elif self.nrs_list[0] == 'S':
            self.s_list.append(self.nrs_list)
        elif self.nrs_list[0] == 'R':
            self.r_list.append(self.nrs_list)

        # 没有背完的卡片应该写回recordstack_xxx.txt中
        file.write_nsr(self.fn, self.n_list, 'N')
        file.write_nsr(self.fn, self.s_list, 'S')
        file.write_nsr(self.fn, self.r_list, 'R')
        # 写入数据库
        self.write_db()
        # 刷新界面
        ListCtrlRight.on_refresh()
        # 关闭窗口
        self.Destroy()
        pass

    def write_db(self):
        now = time.strftime('%Y/%m/%d', time.localtime(time.time()))

        if self.undone:
            for rows in self.undone:
                sql = "UPDATE record SET" \
                            " reviewTime = '" + now + "', interval = '" + rows[-3] + "', EF = '" + rows[-2] + "' WHERE" \
                            " recordId = '" + rows[1] + "'"
                DBFun.update('db_pymemo.db', sql)
        if self.done:
            for rows in self.done:
                sql = "UPDATE record SET" \
                            " reviewTime = '" + now + "', interval = '" + rows[-3] + "', EF = '" + rows[-2] + "' WHERE" \
                            " recordId = '" + rows[1] + "'"
                DBFun.update('db_pymemo.db', sql)


class SelectLib(wx.Dialog):
    def __init__(self, lib):
        wx.Dialog.__init__(self, None, -1, '学习', size=(-1, 350),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        v_box = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1, style=wx.BORDER_MASK)
        panel.SetBackgroundColour('white')
        v_box_p = wx.BoxSizer(wx.VERTICAL)

        info_text = wx.StaticText(panel, -1, "选择要学习的词库：")
        v_box_p.Add(info_text, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)
        for index, content in enumerate(lib):
            self.button = wx.Button(panel, -1, lib[content].decode('utf-8'))
            self.button.Bind(wx.EVT_BUTTON, lambda evt, i=content, l=lib: self.on_click(evt, i, l))
            v_box_p.Add(self.button, 0, wx.EXPAND | wx.ALL, 15)
        panel.SetSizer(v_box_p)
        close = wx.Button(self, wx.ID_CANCEL, "关闭")
        v_box.Add(panel, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(close, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    def on_click(self, evt, i, l):
        self.Close()
        pre_dlg = Prepare(i, l)
        pre_dlg.ShowModal()
        pre_dlg.Destroy()


class Prepare(wx.Dialog):
    def __init__(self, i, lib):
        """
        看工作目录下是否存在recordstack_i，如果不存在则创建然后写入前三行: NSR的统计数据（0, 0, 0）
        根据设置中每日学习和复习向recordstack_xxx.txt中添加记录信息
        不足设置的每日学习和复习的数量则补足（有多少补多少）
        :param i: 词库id
        :param lib:
        :return:
        """
        wx.Dialog.__init__(self, None, -1, '准备学习', size=(-1, 350),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)

        # -----------------------------------------

        file_name = 'recordstack_' + i + '.txt'
        if file.is_exist(os.getcwd(), file_name) == 0:
            f = open(file_name, 'w')
            f.write('N:0\nS:0\nR:0')
            f.close()
            pass
        file.no_blank(file_name)
        nsr = file.fetch_statistic(file_name)
        n_num = nsr['N']
        s_num = nsr['S']
        r_num = nsr['R']
        sql = "SELECT * FROM library WHERE libId = '" + i + "'"
        result = DBFun.select('db_pymemo.db', sql)
        r_s = result[0][4]
        n_s = result[0][5]
        review_list = file.filter_repeat(file_name, FrameFun.find_expired(i))
        new_list = file.filter_repeat(file_name, FrameFun.find_new(i))

        file.write_rs(file_name, new_list[:50], 'N')
        file.write_rs(file_name, review_list[:50], 'R')

        # -----------------------------------------

        v_box = wx.BoxSizer(wx.VERTICAL)
        # panel_1
        panel_1 = wx.Panel(self, -1, style=wx.BORDER_MASK)
        panel_1.SetBackgroundColour('white')
        v_box_1 = wx.BoxSizer(wx.VERTICAL)
        big_font_bold = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD, False)
        text_head = wx.StaticText(panel_1, -1, lib[i].decode('utf-8'))
        text_head.SetFont(big_font_bold)
        v_box_1.Add(text_head, 0, wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, 10)

        if n_num + r_num + s_num > 0:
            gs = wx.GridSizer(rows=3, cols=2, vgap=5, hgap=25)
            text_statistic = wx.StaticText(panel_1, -1, "今日到期：")
            text_new = wx.StaticText(panel_1, -1, "新卡片合计：")
            text_all = wx.StaticText(panel_1, -1, "全部卡片：")
            gs.Add(text_statistic, 0, wx.EXPAND)
            gs.Add(wx.StaticText(panel_1, -1, str(n_num) + ' ' + str(s_num) + ' ' + str(r_num)), 0, wx.EXPAND)
            gs.Add(text_new, 0, wx.EXPAND)
            gs.Add(wx.StaticText(panel_1, -1, str(len(new_list))))
            gs.Add(text_all, 0, wx.EXPAND)
            gs.Add(wx.StaticText(panel_1, -1, str(len(FrameFun.find_all(i)))))
            v_box_1.Add(gs, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 10)
        else:
            done_text = '''恭喜！你已经完成今天的学习计划。
    今天的复习数量限制已经达到，但仍有一些卡片需要复习。
    为了更好的记忆效果，你可以考虑调整你的学习计划。
    点击下面词库选项，调整学习计划'''
            tips = wx.StaticText(panel_1, -1, done_text, style=wx.ALIGN_CENTER_HORIZONTAL)
            v_box_1.Add(tips, 0, wx.EXPAND | wx.ALL, 10)

        panel_1.SetSizer(v_box_1)
        v_box.Add(panel_1, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)

        # -----------------------------------------
        # panel_2

        if n_num + r_num + s_num > 0:
            panel_2 = wx.Panel(self, -1, style=wx.BORDER_MASK)
            panel_2.SetBackgroundColour('white')
            h_box_2 = wx.BoxSizer(wx.HORIZONTAL)
            temp = wx.Image('images/other-size/flashcard48.jpg', wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
            flashcard = wx.StaticBitmap(panel_2, -1, temp)
            h_box_2.Add(flashcard, 0, wx.ALL, 10)

            start = buttons.GenButton(panel_2, -1, '开始学习')
            start.SetBezelWidth(0)
            start.SetBackgroundColour('white')
            start.Bind(wx.EVT_BUTTON, lambda evt, l=lib, index=i: self.on_study(evt, l, index))
            h_box_2.Add(start, 1, wx.EXPAND | wx.TOP | wx.BOTTOM | wx.RIGHT, 10)

            panel_2.SetSizer(h_box_2)
            v_box.Add(panel_2, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)
        else:
            pass

        line = wx.StaticLine(self, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)
        v_box.Add(line, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)

        setting_button = buttons.GenButton(self, -1, "词库选项")
        setting_button.SetBezelWidth(1)
        setting_button.SetBackgroundColour('white')
        setting_button.Bind(wx.EVT_BUTTON, lambda evt, l=lib, index=i: self.on_setting(evt, lib, i))

        v_box.Add(setting_button, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    @staticmethod
    def on_setting(evt, lib, i):
        setting_dlg = SettingDialog(lib, i)
        setting_dlg.ShowModal()
        setting_dlg.Destroy()

    def on_study(self, evt, lib, i):
        memo_dlg = MemoDialog(lib, i)
        memo_dlg.ShowModal()
        memo_dlg.Destroy()
        self.Destroy()