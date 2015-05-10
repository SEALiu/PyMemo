# -*- coding: gbk -*-
import time
import wx
import FrameFun
from memo import *


# Lib Dialog
class AddNewLib(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '�½��ʿ�', size=(-1, 270),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        v_box = wx.BoxSizer(wx.VERTICAL)
        name_text = wx.StaticText(panel, -1, "�ʿ����ƣ�")
        lib_name = wx.TextCtrl(panel, -1, "", style=wx.TE_CAPITALIZE)

        desc_text = wx.StaticText(panel, -1, "�ʿ�������")
        lib_desc = wx.TextCtrl(panel, -1, "", size=(-1, 80), style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, -1, label='ȷ��')
        cancel_button = wx.Button(panel, wx.ID_CANCEL, label='ȡ��')
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
        create_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))

        insert_lib_sql = "INSERT INTO library(libId, name, libDesc, createTime) VALUES ('" + lib_id + "', '" + lib_name + "', '" +\
                         lib_desc + "', '" + create_time + "')"
        conn = DBFun.connect_db('db_pymemo.db')
        if DBFun.update(conn, insert_lib_sql):
            conn.commit()
        conn.close()
        ListCtrlLeft.on_refresh()
        self.Close()


class RenameLib(wx.Dialog):
    def __init__(self, old_name, old_desc, lib_id):
        wx.Dialog.__init__(self, None, -1, '�޸�' + old_name + '���ƺ�����', size=(-1, 270),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        v_box = wx.BoxSizer(wx.VERTICAL)

        name_text = wx.StaticText(panel, -1, "�ʿ����ƣ�")
        lib_name = wx.TextCtrl(panel, -1, old_name, style=wx.TE_CAPITALIZE)

        desc_text = wx.StaticText(panel, -1, "�ʿ�������")
        lib_desc = wx.TextCtrl(panel, -1, old_desc, size=(-1, 80), style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, -1, label='ȷ��')
        cancel_button = wx.Button(panel, wx.ID_CANCEL, label='ȡ��')
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
        conn = DBFun.connect_db('db_pymemo.db')
        conn.text_factory = str
        if DBFun.update(conn, update_lib_sql):
            conn.commit()
            ListCtrlLeft.on_refresh()
        conn.close()
        self.Close()


class LibInfo(wx.Dialog):
    def __init__(self, lib_info):
        wx.Dialog.__init__(self, None, -1, lib_info[1].decode('utf-8') + '�ʿ����Ϣ', size=(-1, 300),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)

        v_box = wx.BoxSizer(wx.VERTICAL)

        panel = wx.Panel(self, -1, style=wx.BORDER)
        panel.SetBackgroundColour('white')
        v_box_panel = wx.BoxSizer(wx.VERTICAL)
        lib_id = wx.StaticText(panel, -1, '�ʿ�ID��' + lib_info[0])
        name_text = wx.StaticText(panel, -1, '�ʿ����ƣ�' + lib_info[1].decode('utf-8'))
        desc_text = wx.StaticText(panel, -1, '�ʿ�������' + lib_info[2].decode('utf-8'))
        create_time = wx.StaticText(panel, -1, '����ʱ�䣺' + str(lib_info[3]))
        max_reviews = wx.StaticText(panel, -1, 'ÿ�ո�ϰ��' + str(lib_info[4]))
        max_new = wx.StaticText(panel, -1, 'ÿ��ѧϰ��' + str(lib_info[5]))
        easy_interval = wx.StaticText(panel, -1, '�򵥼����' + str(lib_info[6]) + '���죩' )
        max_interval = wx.StaticText(panel, -1, '�������' + str(lib_info[7]) + '���죩')
        max_time = wx.StaticText(panel, -1, '��ش�' + str(lib_info[8]) + '���룩')
        is_show_timer = wx.StaticText(panel, -1, '��ʾ��ʱ����' + lib_info[9])


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
        ok_button = wx.Button(self, wx.ID_OK, label='ȷ��')
        h_box.Add(ok_button, 1, wx.RIGHT, border=5)

        v_box.Add(panel, 1, wx.EXPAND | wx.ALL, 10)
        v_box.Add(h_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        self.SetSizer(v_box)
        self.Centre()
        self.Show(True)


class DeleteLib(wx.Dialog):
    def __init__(self, lib_name, lib_id):
        wx.Dialog.__init__(self, None, -1, 'ɾ��' + lib_name + '�ʿ�', size=(-1, 180),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('white')
        v_box = wx.BoxSizer(wx.VERTICAL)
        info_text = wx.StaticText(panel, -1, lib_name + '�ʿ⽫��ɾ�����ʿ��еļ�¼�ᱻת�����¶�Ժ��\n��ȷ��Ҫ������ô��')
        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, -1, label='ȷ��')
        self.Bind(wx.EVT_BUTTON, lambda evt, i=lib_id: self.on_delete(evt, i), ok_button)
        cancel_button = wx.Button(panel, wx.ID_CANCEL, label='ȡ��')
        h_box.Add(ok_button, 1, wx.RIGHT, border=5)
        h_box.Add(cancel_button, 1)

        v_box.Add(info_text, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP , 20)
        v_box.Add(h_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)

        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    def on_delete(self, evt, i):
        conn = DBFun.connect_db('db_pymemo.db')
        delete_lib_sql = "DELETE FROM library WHERE libId='" + i + "'"
        delete_record_sql = "DELETE FROM record WHERE recordId LIKE '%" + i + "'"
        DBFun.update(conn, delete_lib_sql)
        DBFun.update(conn, delete_record_sql)
        DBFun.commit(conn)
        DBFun.close_db(conn)
        ListCtrlLeft.on_refresh()
        ListCtrlRight.on_refresh()
        self.Close()


# Record Dialog
class RecordInfo(wx.Dialog):
    def __init__(self, detail):
        wx.Dialog.__init__(self, None, -1, '��¼����Ϣ', size=(-1, 300),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)

        v_box = wx.BoxSizer(wx.VERTICAL)

        panel = wx.Panel(self, -1, style=wx.BORDER)
        panel.SetBackgroundColour('white')
        v_box_panel = wx.BoxSizer(wx.VERTICAL)
        lib_id = wx.StaticText(panel, -1, '��¼ID��' + detail[0][0:5])
        name_text = wx.StaticText(panel, -1, '�ʿ�ID��' + detail[0][5:])
        desc_text = wx.StaticText(panel, -1, '���⣨���棩��' + detail[1].decode('utf-8'))
        create_time = wx.StaticText(panel, -1, '�𰸣����棩��' + detail[2].decode('utf-8'))
        max_reviews = wx.StaticText(panel, -1, '���ʱ�䣺' + detail[3].decode('utf-8'))
        max_new = wx.StaticText(panel, -1, '��ϰʱ�䣺' + str(detail[4]).decode('utf-8'))
        easy_interval = wx.StaticText(panel, -1, '�޸�ʱ�䣺' + str(detail[5]).decode('utf-8'))
        max_interval = wx.StaticText(panel, -1, '�����' + str(detail[6]) + '���죩')
        max_time = wx.StaticText(panel, -1, 'E-Factor��' + str(detail[7]))
        is_show_timer = wx.StaticText(panel, -1, '�Ƿ����' + detail[8])

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
        close_button = wx.Button(self, wx.ID_CANCEL, label='�ر�')
        h_box.Add(close_button, 1, wx.RIGHT, border=5)

        v_box.Add(panel, 1, wx.EXPAND | wx.ALL, 10)
        v_box.Add(h_box, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 10)

        self.SetSizer(v_box)
        self.Centre()
        self.Show(True)


class UpdateRecord(wx.Dialog):
    def __init__(self, detail):
        wx.Dialog.__init__(self, None, -1, '�޸ļ�¼', size=(-1, 260),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        v_box = wx.BoxSizer(wx.VERTICAL)

        ques_text = wx.StaticText(panel, -1, "���⣨���棩��")
        record_ques = wx.TextCtrl(panel, -1,
                                  detail[1].decode('utf-8'),
                                  size=(-1, 50),
                                  style=wx.TE_MULTILINE)

        ans_text = wx.StaticText(panel, -1, "�𰸣����棩��")
        record_ans = wx.TextCtrl(panel, -1,
                                 detail[2].decode('utf-8'),
                                 size=(-1, 50),
                                 style=wx.TE_MULTILINE)

        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, -1, label='�޸�')
        self.Bind(wx.EVT_BUTTON,
                  lambda evt, ques=record_ques, ans=record_ans, i=detail[0]:
                  self.on_submit(evt, ques, ans, i),
                  ok_button)

        cancel_button = wx.Button(panel, wx.ID_CANCEL, label='ȡ��')

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
        alert_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        update_record_sql = "UPDATE record SET" \
                            " ques = '" + ques + "', ans = '" + ans + "', alertTime = '" + alert_time + "' WHERE" \
                            " recordId = '" + i + "'"
        conn = DBFun.connect_db('db_pymemo.db')
        conn.text_factory = str
        if DBFun.update(conn, update_record_sql):
            conn.commit()
            ListCtrlRight.on_refresh()
        conn.close()
        self.Close()


class AddNewRecord(wx.Dialog):
    def __init__(self, LIBRARIES, flag):
        wx.Dialog.__init__(self, None, -1, '����һ����¼', size=(-1, 350),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        self.lib_id = -1
        v_box = wx.BoxSizer(wx.VERTICAL)
        h_box_info = wx.BoxSizer(wx.HORIZONTAL)

        lib_items = ['��ѡ��ʿ�']
        for index, element in enumerate(LIBRARIES):
            lib_items.append(LIBRARIES[element].decode('utf-8'))

        lib_combo_box = wx.ComboBox(panel, choices=lib_items, style=wx.CB_READONLY)

        # ��תLIBRARIES�ֵ䣬�Ա��ڸ��ݴʿ����ƻ�ȡ�ʿ��ID������������ݿ⡣
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

        name_text = wx.StaticText(panel, -1, "���⣨���棩��")
        record_ques = wx.TextCtrl(panel, -1, "", size=(-1, 80), style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

        desc_text = wx.StaticText(panel, -1, "�𰸣����棩��")
        record_ans = wx.TextCtrl(panel, -1, "", size=(-1, 80), style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

        h_box_btn = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, -1, label='ȷ��')
        close_button = wx.Button(panel, wx.ID_CANCEL, label='ȡ��')

        self.Bind(wx.EVT_BUTTON, lambda evt, ques=record_ques, ans=record_ans: self.on_submit(evt, ques, ans), ok_button)
        h_box_btn.Add(ok_button, 1, wx.RIGHT, border=5)
        h_box_btn.Add(close_button, 1)

        v_box.Add(h_box_info, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(name_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        v_box.Add(record_ques, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(desc_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(record_ans, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(h_box_btn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    def set_lib_id(self, value):
        self.lib_id = value

    def get_lib_id(self):
        return self.lib_id

    def on_submit(self, evt, ques, ans):
        # print self.get_lib_id(), '\n', ques.GetValue().encode('utf-8'), '\n', ans.GetValue().encode('utf-8')
        if self.get_lib_id() == -1:
            msg_dlg = wx.MessageDialog(self, '��ȷ��ѡ����һ���ʿ⣡',
                           '��ʾ',
                           wx.OK | wx.ICON_WARNING)
            msg_dlg.ShowModal()
            msg_dlg.Destroy()
        else:
            record_ques = ques.GetValue().encode('utf-8')
            record_ans = ans.GetValue().encode('utf-8')
            next_record_id = DBFun.max_record('recordId') + 1
            record_id = str(next_record_id).zfill(5) + self.get_lib_id()
            # ���ã�����ڶ������� self.get_lib_id() != -1, ����û��ѡ��ʿ�Ҳ���Բ����¼��
            self.set_lib_id(-1)
            # addTime: type is str
            add_time = time.strftime('%Y/%m/%d', time.localtime(time.time()))
            insert_sql = "INSERT INTO record(recordId, ques, ans, addTime) VALUES" \
                         " ('" + record_id + "', '" + record_ques + "', '" + record_ans + "', '" + add_time + "')"
            conn = DBFun.connect_db('db_pymemo.db')
            if DBFun.update(conn, insert_sql):
                conn.commit()
            conn.close()
            ListCtrlRight.on_refresh()
            self.Close()
        pass

    def test(self, evt, ob, lib):
        lib_name = ob.GetValue().encode('utf-8')
        if lib_name in lib.keys():
            self.set_lib_id(lib[lib_name])
            print self.get_lib_id()
        else:
            print lib_name


        # if cursor == None:
        #     print '��ѡ��ʿ�'
        # else:
        #     for rows in cursor:
        #         self.set_lib_id(rows[0])
        # DBFun.close_db(conn)
        # print self.get_lib_id()
        pass


class DeleteRecord(wx.Dialog):
    def __init__(self, detail):
        wx.Dialog.__init__(self, None, -1, '����/ɾ����¼', size=(-1, 180),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('white')
        v_box = wx.BoxSizer(wx.VERTICAL)
        info_text = wx.StaticText(panel, -1,
                                  '�����¼�󣬸ü�¼������ѧϰ�г��֣�ֱ����ȡ������'
                                  '\nע�⣬������������¼֮������ѧϰ���̽������á�'
                                  '\n\nɾ����¼�󣬸ü�¼��������ʧ��')
        h_box = wx.BoxSizer(wx.HORIZONTAL)

        delete_button = wx.Button(panel, -1, label='ɾ��')
        cancel_button = wx.Button(panel, wx.ID_CANCEL, label='ȡ��')

        self.Bind(wx.EVT_BUTTON, lambda evt, i=detail[0]: self.on_delete(evt, i), delete_button)

        if detail[-1] == 'True':
            play_button = wx.Button(panel, -1, label='ȡ������')
            self.Bind(wx.EVT_BUTTON, lambda evt, i=detail[0], flag='False': self.on_is_pause(evt, i, flag), play_button)
            h_box.Add(play_button, 1, wx.RIGHT, border=5)
        else:
            pause_button = wx.Button(panel, -1, label='����')
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
        conn = DBFun.connect_db('db_pymemo.db')
        conn.text_factory = str
        if DBFun.update(conn, pause_sql):
            conn.commit()
            ListCtrlRight.on_refresh()
        conn.close()
        self.Close()

    def on_delete(self, evt, i):
        delete_sql = "DELETE FROM record WHERE recordId = '" + i + "'"
        conn = DBFun.connect_db('db_pymemo.db')
        DBFun.update(conn, delete_sql)
        DBFun.commit(conn)
        DBFun.close_db(conn)
        ListCtrlRight.on_refresh()
        self.Close()


# Other Dialogs
class AboutDialog(wx.AboutDialogInfo):
    def __init__(self):
        wx.AboutDialogInfo.__init__(self)
        description = "PyMemo��һ�������ظ�ѧϰԭ��ļ�������������ã���Ѳ���Դ��\n" \
            "PyMeomo��AGPL3Э�鷢����\n\n" \
            "�����ҵ�һ���ҵ��ƣ�����Ϊ������Python�ĵ��ʼ����������\n" \
            "GUI�⣺wxpython 2.7.9\n\n" \
            "�������ߣ�pyCharm Community Edition 4.0.4\n" \
            "��Щͼ���������ڲ�ͬ����Դ\n���д󲿷����ԣ�http://findicons.com/\n\n" \
            "�ر��л�����ι���ʦ��ָ��\n\n" \
            "��������������飬����Bug��������л��\n\n" \
            "��ϵ��iliuyang@foxmail.com"
        self.SetIcon(wx.Icon('images/64/PyMemo_logo_white.png', wx.BITMAP_TYPE_PNG))
        self.SetName("PyMemo")
        self.SetVersion('1.0')
        self.SetDescription(description)
        self.SetCopyright('(c)2015 ����')
        wx.AboutBox(self)


class SettingDialog(wx.Dialog):
    def __init__(self, LIBRARIES, flag):
        wx.Dialog.__init__(self, None, -1, '�ʿ�����', size=(200, 400),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        # global lib_index
        lib_items = ['��ѡ��ʿ�']
        for index, element in enumerate(LIBRARIES):
            lib_items.append(LIBRARIES[element].decode('utf-8'))

        v_box = wx.BoxSizer(wx.VERTICAL)
        panel_combo = wx.Panel(self, -1)
        h_box_combo = wx.BoxSizer(wx.HORIZONTAL)
        lib_text = wx.StaticText(panel_combo, -1, "��������Щ����Ӧ�����ĸ��ʿ��ϣ�")

        lib_combo_box = wx.ComboBox(panel_combo, choices=lib_items, style=wx.CB_READONLY)
        if flag == -1:
            lib_combo_box.SetSelection(0)
        else:
            lib_index = lib_items.index(LIBRARIES[flag].decode('utf-8'))
            lib_combo_box.SetSelection(lib_index)

        h_box_combo.Add(lib_text, 0, wx.TOP | wx.RIGHT, 10)
        h_box_combo.Add(lib_combo_box, 0, wx.TOP | wx.LEFT, 5)
        panel_combo.SetSizer(h_box_combo)

        v_box.Add(panel_combo, 0, wx.TOP | wx.LEFT | wx.RIGHT, 10)

        line_1 = wx.StaticLine(self, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)
        v_box.Add(line_1, 0, wx.EXPAND | wx.ALL, 10)

        grid_sizer = wx.GridSizer(2, 2, 5, 5)
        # (0, 0)
        panel_left_top = wx.Panel(self)
        preview_setting = wx.StaticBox(panel_left_top, -1, label='ѧϰ��Ƭ����')
        sbs1 = wx.StaticBoxSizer(preview_setting, orient=wx.VERTICAL)

        show_interval = wx.CheckBox(panel_left_top,
                            label='�ڻش�ť����ʾ��һ�θ�ϰʱ��',
                            style=wx.CHK_3STATE)
        show_rest = wx.CheckBox(panel_left_top,
                            label='�ڸ�ϰ��ʱ����ʾʣ�࿨Ƭ��',
                            style=wx.CHK_3STATE)
        show_duration = wx.CheckBox(panel_left_top,
                            label='�ڸ�ϰ��ʱ����ʾ����ʱ��',
                            style=wx.CHK_3STATE)
        show_interval.SetValue(True)
        show_rest.SetValue(True)
        show_duration.SetValue(True)

        sbs1.Add(show_interval, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=10)
        sbs1.Add(show_rest, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=10)
        sbs1.Add(show_duration, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=10)

        panel_left_top.SetSizer(sbs1)

        grid_sizer.Add(panel_left_top, 3, wx.EXPAND | wx.ALL, border=10)

        # (0, 1)
        panel_right_top = wx.Panel(self)
        study_setting = wx.StaticBox(panel_right_top, -1, label='�Զ���ѧϰ��Ƭ')
        sbs2 = wx.StaticBoxSizer(study_setting, orient=wx.VERTICAL)
        grid1 = wx.FlexGridSizer(0, 2, 0, 0)

        # group of controls:
        self.group_ctrl = []
        text1 = wx.StaticText(panel_right_top, label="ÿ��ѧϰ��Ƭ���ޣ��ţ�")
        text2 = wx.StaticText(panel_right_top, label="ÿ�ո�ϰ��Ƭ���ޣ��ţ�")
        text3 = wx.StaticText(panel_right_top, label="��ʱ��ʾ��Ƭ���棨�룩")

        study_limit = wx.SpinCtrl(panel_right_top, -1)
        study_limit.SetRange(1, 200)
        study_limit.SetValue(50)

        review_limit = wx.SpinCtrl(panel_right_top, -1)
        review_limit.SetRange(1, 200)
        review_limit.SetValue(50)

        deadline_limit = wx.SpinCtrl(panel_right_top, -1)
        deadline_limit.SetRange(1, 60)
        deadline_limit.SetValue(30)

        self.group_ctrl.append((text1, study_limit))
        self.group_ctrl.append((text2, review_limit))
        self.group_ctrl.append((text3, deadline_limit))

        for text, spin_ctrl in self.group_ctrl:
            grid1.Add(text, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP, 5)
            grid1.Add(spin_ctrl, 0, wx.ALIGN_CENTRE | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        sbs2.Add(grid1, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        panel_right_top.SetSizer(sbs2)
        grid_sizer.Add(panel_right_top, 1, wx.EXPAND | wx.ALL, border=10)

        # (1, 0)
        panel_left_bottom = wx.Panel(self)
        order_setting = wx.StaticBox(panel_left_bottom, -1, label='ѧϰ��Ƭ��˳��')
        sbs3 = wx.StaticBoxSizer(order_setting, orient=wx.VERTICAL)

        old_after_new = wx.RadioButton(panel_left_bottom, -1, "�¿�Ƭѧϰ��֮���ٸ�ϰ�ɿ�Ƭ")
        new_after_old = wx.RadioButton(panel_left_bottom, -1, "�ɿ�Ƭ��ϰ��֮����ѧϰ�¿�Ƭ")
        new_or_old = wx.RadioButton(panel_left_bottom, -1, "�¾ɿ�Ƭ�������")

        new_or_old.SetValue(True)

        sbs3.Add(old_after_new, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=10)
        sbs3.Add(new_after_old, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=10)
        sbs3.Add(new_or_old, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=10)

        panel_left_bottom.SetSizer(sbs3)

        grid_sizer.Add(panel_left_bottom, 1, wx.EXPAND | wx.ALL, border=10)

        # (1, 1)
        panel_right_bottom = wx.Panel(self)
        font_setting = wx.StaticBox(panel_right_bottom, -1, label='��������')
        sbs4 = wx.StaticBoxSizer(font_setting, orient=wx.VERTICAL)
        # h_box_1 = wx.BoxSizer(wx.HORIZONTAL)
        h_box_2 = wx.BoxSizer(wx.HORIZONTAL)

        # font_family_list = ['font-family-one',
        #                    'font-family-two',
        #                    'font-family-three',
        #                    'font-family-flour']
        # font_family_text = wx.StaticText(panel_right_bottom, -1, "���壺",)
        # font_family = wx.Choice(panel_right_bottom, -1, choices=font_family_list)
        #
        # h_box_1.Add(font_family_text, 1, wx.LEFT | wx.TOP, border=10)
        # h_box_1.Add(font_family, 3, wx.TOP, border=10)

        font_size_text = wx.StaticText(panel_right_bottom, -1, "�ֺţ�")
        font_size = wx.SpinCtrl(panel_right_bottom, -1)
        font_size.SetRange(1, 30)
        font_size.SetValue(12)

        h_box_2.Add(font_size_text, 1, wx.LEFT | wx.TOP, border=10)
        h_box_2.Add(font_size, 3, wx.TOP, border=10)

        # sbs4.Add(h_box_1, wx.LEFT, border=5)
        sbs4.Add(h_box_2, wx.LEFT, border=5)

        panel_right_bottom.SetSizer(sbs4)
        grid_sizer.Add(panel_right_bottom, 1, wx.EXPAND | wx.ALL, border=10)
        v_box.Add(grid_sizer, 1)

        # (2, 1)
        h_box = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, -1, label='ȷ��')
        apply_button = wx.Button(self, -1, label="Ӧ��")
        close_button = wx.Button(self, -1, label='�ر�')
        h_box.Add(ok_button, 1, wx.RIGHT, border=5)
        h_box.Add(apply_button, 1, wx.RIGHT, border=5)
        h_box.Add(close_button, 1, wx.RIGHT, border=10)

        v_box.Add(h_box, 0, wx.ALIGN_RIGHT | wx.BOTTOM, border=10)

        self.Bind(wx.EVT_BUTTON, self.on_close, close_button)

        self.SetSizer(v_box)
        self.Fit()
        self.Centre()
        self.Show(True)

    def on_close(self, e):
        self.Destroy()
        e.Skip()


class Export(wx.DirDialog):
    def __init__(self, parent):
        wx.DirDialog.__init__(self, parent, "��ѡ��һ���ļ������浼���Ĵʿ⣺",
                          style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        self.CentreOnParent()
        self.Show(True)


class Import(wx.FileDialog):
    def __init__(self, parent):
        wx.FileDialog.__init__(self, parent, "ѡ����Ĵʿ��ļ�",
                               wildcard="BMP and GIF files (*.bmp*.gif)|*.bmp*.gif|PNG files (*.png)|*.png",
                               style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_CHANGE_DIR
                               )
        self.Centre()
        self.Show(True)


class MemoQues(wx.Dialog):
    """
    ������Щ���⣬Ӧ��ֻˢ�� panel_word �� panel_btn
    ���������ٵ�ǰ�ĶԻ������»���һ���µģ���
    """
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, 'ѧϰ', size=(-1, 470),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)

        panel = wx.Panel(self, -1)
        font_ques = wx.Font(14, wx.FONTFAMILY_DEFAULT,
                            wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD,
                            faceName="Consolas",
                            underline=False)
        font_api = wx.Font(13, wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_ITALIC,
                           wx.FONTWEIGHT_NORMAL,
                           faceName="Consolas",
                           underline=False)
        # font_ans = wx.Font(12, wx.FONTFAMILY_DEFAULT,
        #                    wx.FONTSTYLE_NORMAL,
        #                    wx.FONTWEIGHT_NORMAL,
        #                    faceName="Consolas",
        #                    underline=False)

        # ------

        v_box = wx.BoxSizer(wx.VERTICAL)

        h_box_title = wx.BoxSizer(wx.HORIZONTAL)
        lib_name = wx.StaticText(panel, -1, "��ǰѧϰ�Ĵʿ�����")
        backward = wx.BitmapButton(panel, -1, wx.Bitmap('images/32/backward.png'), style=wx.NO_BORDER)
        more = wx.BitmapButton(panel, -1, wx.Bitmap('images/other-size/more26.png'), style=wx.NO_BORDER)

        h_box_title.Add(lib_name, 1, wx.TOP | wx.RIGHT, 10)
        h_box_title.Add(backward, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 5)
        h_box_title.Add(more, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.TOP, 5)

        # ------

        line_1 = wx.StaticLine(panel, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)

        # ------

        h_box_info = wx.BoxSizer(wx.HORIZONTAL)
        rest_list = [68, 8, 65]
        rest_text = "ʣ�࿨Ƭ��"

        for label in rest_list:
            rest_text += str(label) + " " * 2

        rest_label = wx.StaticText(panel, -1, rest_text)
        duration_label = wx.StaticText(panel, -1, "01:09")

        h_box_info.Add(rest_label, 1, wx.RIGHT, 10)
        h_box_info.Add(duration_label, 0, wx.ALIGN_RIGHT)

        # ------

        ques = "general"
        ipa = "['d?en?r?l]".encode('utf-8')
        # ans = "[n.] ����\n[adj.]ȫ��ģ��ܵģ��ձ��"
        panel_word = wx.Panel(panel, -1, size=(-1, 300), style=wx.BORDER_THEME)
        panel_word.SetBackgroundColour('white')
        v_box_pw = wx.BoxSizer(wx.VERTICAL)
        ques_text = wx.StaticText(panel_word, -1, ques)
        ipa_text = wx.StaticText(panel_word, -1, ipa)
        # ans_text = wx.StaticText(panel_word, -1, ans)
        ques_text.SetFont(font_ques)
        ipa_text.SetFont(font_api)
        # ans_text.SetFont(font_ans)
        line_2 = wx.StaticLine(panel_word, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)

        v_box_pw.Add(ques_text, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 20)
        v_box_pw.Add(ipa_text, 0, wx.ALIGN_CENTER_HORIZONTAL)
        v_box_pw.Add(line_2, 0, wx.EXPAND | wx.ALL, 10)
        # v_box_pw.Add(ans_text, 1, wx.ALIGN_CENTER_HORIZONTAL)
        panel_word.SetSizer(v_box_pw)

        # ---------

        panel_btn = wx.Panel(panel, -1)
        h_box_btn = wx.BoxSizer(wx.HORIZONTAL)
        show_ans = wx.Button(panel_btn, -1, "��ʾ��")
        self.Bind(wx.EVT_BUTTON, self.on_show_ans, show_ans)
        h_box_btn.Add(show_ans, 1, wx.EXPAND)
        panel_btn.SetSizer(h_box_btn)

        v_box.Add(h_box_title, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(line_1, 0, wx.EXPAND)
        v_box.Add(h_box_info, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(panel_word, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(panel_btn, 1, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    def on_show_ans(self, evt):
        self.Destroy()
        dlg = MemoAns()
        dlg.ShowModal()
        dlg.Destroy()
        evt.Skip()


class MemoAns(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, 'ѧϰ', size=(-1, 470),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        font_ques = wx.Font(14, wx.FONTFAMILY_DEFAULT,
                            wx.FONTSTYLE_NORMAL,
                            wx.FONTWEIGHT_BOLD,
                            faceName="Consolas",
                            underline=False)
        font_api = wx.Font(13, wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_ITALIC,
                           wx.FONTWEIGHT_NORMAL,
                           faceName="Consolas",
                           underline=False)
        font_ans = wx.Font(12, wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL,
                           wx.FONTWEIGHT_NORMAL,
                           faceName="Consolas",
                           underline=False)

        # ------

        v_box = wx.BoxSizer(wx.VERTICAL)

        h_box_title = wx.BoxSizer(wx.HORIZONTAL)
        lib_name = wx.StaticText(panel, -1, "��ǰѧϰ�Ĵʿ�����")
        backward = wx.BitmapButton(panel, -1, wx.Bitmap('images/32/backward.png'), style=wx.NO_BORDER)
        more = wx.BitmapButton(panel, -1, wx.Bitmap('images/other-size/more26.png'), style=wx.NO_BORDER)

        h_box_title.Add(lib_name, 1, wx.TOP | wx.RIGHT, 10)
        h_box_title.Add(backward, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.TOP, 5)
        h_box_title.Add(more, 0, wx.ALIGN_RIGHT | wx.LEFT | wx.TOP, 5)

        # ------

        line_1 = wx.StaticLine(panel, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)

        # ------

        h_box_info = wx.BoxSizer(wx.HORIZONTAL)
        rest_list = [68, 8, 65]
        rest_text = "ʣ�࿨Ƭ��"
        for label in rest_list:
            rest_text += str(label) + " " * 2

        rest_label = wx.StaticText(panel, -1, rest_text)
        duration_label = wx.StaticText(panel, -1, "01:09")

        h_box_info.Add(rest_label, 1, wx.RIGHT, 10)
        h_box_info.Add(duration_label, 0, wx.ALIGN_RIGHT)

        # ------

        ques = "general"
        ipa = "['d?en?r?l]".encode('utf-8')
        ans = "[n.] ����\n[adj.]ȫ��ģ��ܵģ��ձ��"
        panel_word = wx.Panel(panel, -1, size=(-1, 300), style=wx.BORDER_THEME)
        panel_word.SetBackgroundColour('white')
        v_box_pw = wx.BoxSizer(wx.VERTICAL)
        ques_text = wx.StaticText(panel_word, -1, ques)
        ipa_text = wx.StaticText(panel_word, -1, ipa)
        ans_text = wx.StaticText(panel_word, -1, ans)
        ques_text.SetFont(font_ques)
        ipa_text.SetFont(font_api)
        ans_text.SetFont(font_ans)
        line_2 = wx.StaticLine(panel_word, -1, size=(-1, -1), style=wx.LI_HORIZONTAL)

        v_box_pw.Add(ques_text, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP, 20)
        v_box_pw.Add(ipa_text, 0, wx.ALIGN_CENTER_HORIZONTAL)
        v_box_pw.Add(line_2, 0, wx.EXPAND | wx.ALL, 10)
        v_box_pw.Add(ans_text, 1, wx.ALIGN_CENTER_HORIZONTAL)
        panel_word.SetSizer(v_box_pw)

        # ---------

        panel_btn = wx.Panel(panel, -1)
        h_box_btn = wx.BoxSizer(wx.HORIZONTAL)
        again = wx.Button(panel_btn, -1, "����")
        hard = wx.Button(panel_btn, -1, "����")
        good = wx.Button(panel_btn, -1, "һ��")
        easy = wx.Button(panel_btn, -1, "��")

        self.Bind(wx.EVT_BUTTON, self.on_again, again)
        self.Bind(wx.EVT_BUTTON, self.on_hard, hard)
        self.Bind(wx.EVT_BUTTON, self.on_good, good)
        self.Bind(wx.EVT_BUTTON, self.on_easy, easy)

        h_box_btn.Add(again, 1, wx.EXPAND | wx.RIGHT, 5)
        h_box_btn.Add(hard, 1, wx.EXPAND | wx.RIGHT, 5)
        h_box_btn.Add(good, 1, wx.EXPAND | wx.RIGHT, 5)
        h_box_btn.Add(easy, 1, wx.EXPAND)
        panel_btn.SetSizer(h_box_btn)

        v_box.Add(h_box_title, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(line_1, 0, wx.EXPAND)
        v_box.Add(h_box_info, 0, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(panel_word, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(panel_btn, 1, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)

    def on_again(self, evt):
        pass

    def on_hard(self, evt):
        pass

    def on_good(self, evt):
        pass

    def on_easy(self, evt):
        pass


class SelectLib(wx.Dialog):
    def __init__(self, lib):
        wx.Dialog.__init__(self, None, -1, 'ѧϰ',
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)

        print FrameFun.find_new('000')


        panel = wx.Panel(self, -1)
        v_box = wx.BoxSizer(wx.VERTICAL)
        text_info = wx.StaticText(panel, -1, "ѡ��Ҫѧϰ�Ĵʿ⣺")

        list_ctrl = wx.ListCtrl(panel, size=(-1,100),
                                     style=wx.LC_REPORT
                                     |wx.BORDER_SUNKEN
                                     )
        list_ctrl.InsertColumn(0, '�ʿ���')
        list_ctrl.InsertColumn(1, '��')
        list_ctrl.InsertColumn(2, 'ѧϰ')
        list_ctrl.InsertColumn(3, '��ϰ')

        for index, rows in enumerate(lib):
            list_ctrl.InsertStringItem(index, lib[rows].decode('utf-8'))

        v_box.Add(text_info, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(list_ctrl, 0, wx.EXPAND | wx.CENTER | wx.LEFT | wx.RIGHT, 10)
        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)