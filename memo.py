# -*- coding: utf-8 -*-
# memo.py
import sys
import wx
import Dialog
import DBFun
import wx.lib.dialogs
import FrameFun

LIBRARIES = {}
RECORDS = []
LIBRARY_ID = []


class ListCtrlLeft(wx.ListCtrl):
    def __init__(self, parent, i):
        wx.ListCtrl.__init__(self, parent, i, style=wx.LC_REPORT
                                                                     | wx.LC_HRULES
                                                                     | wx.LC_NO_HEADER
                                                                     | wx.LC_SINGLE_SEL)
        self.parent = parent
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.load_data_left(LIBRARIES)

    @staticmethod
    def fetch_lib():
        select_sql = "SELECT * FROM library"
        result_list = DBFun.select('db_pymemo.db', select_sql)
        LIBRARIES.clear()
        LIBRARY_ID[:] = []
        for rows in result_list:
            LIBRARY_ID.append(rows[0])
            LIBRARIES[rows[0]] = rows[1]

    def load_data_left(self, LIBRARIES):
        self.DeleteAllItems()
        self.fetch_lib()
        self.il = wx.ImageList(32, 32)
        lib_img = wx.Bitmap('images/32/library.png')
        for i in range(len(LIBRARIES)):
            self.il.Add(lib_img)

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, '')

        for index, element in enumerate(LIBRARIES):
            self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_lib_select)
            self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_lib_right_click)
            self.InsertStringItem(0, LIBRARIES[element].decode('utf-8'))
            # print element
            self.SetItemImage(0, index)

    def on_size(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x - 5)
        event.Skip()


    @staticmethod
    def on_refresh():
        window = wx.FindWindowByName('ListControlOnLeft', parent=None)
        ListCtrlLeft.fetch_lib()
        window.load_data_left(LIBRARIES)

    @staticmethod
    def on_lib_select(evt):
        index = evt.GetIndex()
        sql = "SELECT * FROM record WHERE recordId LIKE '%" + LIBRARY_ID[index] + "'"
        cursor = DBFun.select('db_pymemo.db', sql)
        r = []
        for rows in cursor:
            r.append(rows)
        RECORDS = r
        window = wx.FindWindowByName('ListControlOnRight', parent=None)
        window.load_data_right(RECORDS)

    def on_lib_right_click(self, event):
        index = event.GetIndex()
        menu = wx.Menu()
        item_rename = wx.MenuItem(menu, -1, "修改名称或描述")
        item_info = wx.MenuItem(menu, -1, "查看词库的信息")
        item_add = wx.MenuItem(menu, -1, '增加一条记录')
        item_setting = wx.MenuItem(menu, -1, '设置')
        item_delete = wx.MenuItem(menu, -1, '删除这个词库')
        self.Bind(wx.EVT_MENU, lambda evt, i=index: self.on_lib_rename(evt, i), item_rename)
        self.Bind(wx.EVT_MENU, lambda evt, i=index: self.on_item_info(evt, i), item_info)
        self.Bind(wx.EVT_MENU, lambda evt, i=index: self.on_item_add(evt, i), item_add)
        self.Bind(wx.EVT_MENU, lambda evt, i=index: self.on_lib_setting(evt, i), item_setting)
        self.Bind(wx.EVT_MENU, lambda evt, i=index: self.on_lib_delete(evt, i), item_delete)

        menu.AppendItem(item_rename)
        menu.AppendItem(item_info)
        menu.AppendItem(item_add)
        menu.AppendItem(item_setting)
        menu.AppendItem(item_delete)

        self.PopupMenu(menu)
        menu.Destroy()

    @staticmethod
    def on_lib_rename(evt, i):
        lib_desc = ''
        lib_id = LIBRARY_ID[i]
        lib_name = LIBRARIES[LIBRARY_ID[i]].decode('utf-8')
        select_sql = "SELECT * FROM library WHERE libId = '" + lib_id + "'"
        cursor = DBFun.select('db_pymemo.db', select_sql)
        for rows in cursor:
            lib_desc = rows[2].decode('utf-8')
        rename_dlg = Dialog.RenameLib(lib_name, lib_desc, lib_id)
        rename_dlg.ShowModal()
        rename_dlg.Destroy()
        pass

    @staticmethod
    def on_item_info(evt, i):
        lib_info = ()
        lib_id = LIBRARY_ID[i]
        lib_name = LIBRARIES[LIBRARY_ID[i]].decode('utf-8')

        select_sql = "SELECT * FROM library WHERE libId = '" + lib_id + "'"
        cursor = DBFun.select('db_pymemo.db', select_sql)
        for rows in cursor:
            lib_info = rows
        # print lib_info
        info_dlg = Dialog.LibInfo(lib_info)
        info_dlg.ShowModal()
        info_dlg.Destroy()
        pass

    @staticmethod
    def on_item_add(evt, i):
        new_card_dlg = Dialog.AddNewRecord(LIBRARIES, LIBRARY_ID[i])
        new_card_dlg.ShowModal()
        new_card_dlg.Destroy()
        pass

    @staticmethod
    def on_lib_setting(evt, i):
        # print "setting", LIBRARY_ID[i]
        setting_dlg = Dialog.SettingDialog(LIBRARIES, LIBRARY_ID[i])
        setting_dlg.ShowModal()
        setting_dlg.Destroy()
        pass

    def on_lib_delete(self, evt, i):
        lib_id = LIBRARY_ID[i]
        if lib_id == '000':
            msg_dlg = wx.MessageDialog(self, '默认词库无法被删除！',
                               '提示',
                               wx.OK | wx.ICON_WARNING)
            msg_dlg.ShowModal()
            msg_dlg.Destroy()
        else:
            lib_name = LIBRARIES[LIBRARY_ID[i]].decode('utf-8')
            delete_dlg = Dialog.DeleteLib(lib_name, lib_id)
            delete_dlg.ShowModal()
            delete_dlg.Destroy()


class ListCtrlRight(wx.ListCtrl):
    def __init__(self, parent, i):
        wx.ListCtrl.__init__(self, parent, i, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_SINGLE_SEL)
        self.parent = parent
        select_sql = 'SELECT * FROM record'
        RECORDS = DBFun.select('db_pymemo.db', select_sql)
        self.load_data_right(RECORDS)

    def load_data_right(self, RECORDS):
        self.DeleteAllItems()
        self.DeleteAllColumns()
        self.list_head_name = ['记录ID',
                               '正面',
                               '反面',
                               '添加时间',
                               '复习时间',
                               '修改时间',
                               '间隔天数',
                               'E-Fator',
                               '是否挂起'
                               ]
        for i in range(len(self.list_head_name)):
            self.InsertColumn(i, self.list_head_name[i], width=wx.LIST_AUTOSIZE)

        for i in RECORDS:
            index = self.InsertStringItem(sys.maxint, i[0])
            self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, lambda e, record=RECORDS: self.on_record_right_click(e, record))
            for j in range(len(self.list_head_name)):
                self.SetStringItem(index, j, str(i[j]).decode('utf-8'))

    @staticmethod
    def on_refresh():
        window = wx.FindWindowByName('ListControlOnRight', parent=None)
        select_sql = "SELECT * FROM record"
        RECORDS = DBFun.select('db_pymemo.db', select_sql)
        window.load_data_right(RECORDS)

    def on_record_right_click(self, evt, record):
        index = evt.GetIndex()
        detail = record[index]
        menu = wx.Menu()
        record_update = wx.MenuItem(menu, -1, "修改")
        record_info = wx.MenuItem(menu, -1, "详细信息")
        record_delete = wx.MenuItem(menu, -1, '挂起/删除')

        self.Bind(wx.EVT_MENU, lambda e, d=detail: self.on_record_update(e, d), record_update)
        self.Bind(wx.EVT_MENU, lambda e, d=detail: self.on_record_info(e, d), record_info)
        self.Bind(wx.EVT_MENU, lambda e, d=detail: self.on_record_delete(e, d), record_delete)

        menu.AppendItem(record_update)
        menu.AppendItem(record_info)
        menu.AppendItem(record_delete)

        self.PopupMenu(menu)
        menu.Destroy()

    @staticmethod
    def on_record_update(evt, d):
        record_update_dlg = Dialog.UpdateRecord(d)
        record_update_dlg.ShowModal()
        record_update_dlg.Destroy()
        pass

    @staticmethod
    def on_record_info(evt, d):
        record_info_dlg = Dialog.RecordInfo(d)
        record_info_dlg.ShowModal()
        record_info_dlg.Destroy()
        pass

    @staticmethod
    def on_record_delete(evt, d):
        record_delete_dlg = Dialog.DeleteRecord(d)
        record_delete_dlg.ShowModal()
        record_delete_dlg.Destroy()
        pass


class CombinePanelRight(wx.Panel):
    def __init__(self, parent, i, records):
        wx.Panel.__init__(self, parent, i, style=wx.BORDER_NONE)

        filter_list = ['过滤器',
                     '显示所有记录',
                     '已到期的',
                     '已记住的',
                     '今天待学习的',
                     '今天已学习的',
                     '始终记不住的',
                     '今天添加的']
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        lib_combo_box = wx.ComboBox(self,
                                    pos=(0, 5),
                                    choices=filter_list,
                                    style=wx.CB_READONLY
                                    )
        self.Bind(wx.EVT_COMBOBOX,
                  lambda evt, ob=lib_combo_box, f=filter_list: self.on_filter(evt, ob, f, RECORDS),
                  lib_combo_box)
        lib_combo_box.SetSelection(0)
        go = wx.BitmapButton(self,
                             -1,
                             wx.Bitmap('images/other-size/search26.png'),
                             size=(32, 32)
                             )
        search_ctrl = wx.TextCtrl(self, -1, size=(300, -1))

        horizontal_box.Add(lib_combo_box, 0, wx.TOP | wx.LEFT | wx.BOTTOM, border=6)
        horizontal_box.Add(search_ctrl, 0, wx.TOP | wx.LEFT | wx.BOTTOM, border=6)
        horizontal_box.Add(go, 0, wx.ALL, border=6)

        self.SetSizer(horizontal_box)
        self.Centre()
        self.Show(True)

    @staticmethod
    def on_filter(e, ob, f, r):
        filter_key = 0
        # 获取到筛选LIST的序号
        for i, album in enumerate(f):
            # filter_dic[i] = album
            if album == ob.GetValue():
                filter_key = i

        if filter_key == 1:
            r = FrameFun.find_all(-1)
            pass
        elif filter_key == 2:
            r = FrameFun.find_expired(-1)
            pass
        elif filter_key == 3:
            r = FrameFun.find_remembered()
            pass
        elif filter_key == 4:
            new_list = FrameFun.find_new(-1)[:50]
            review_list = FrameFun.find_expired(-1)[:50]
            r = new_list + review_list
            pass
        elif filter_key == 5:
            r = FrameFun.find_learned()
            pass
        elif filter_key == 6:
            r = FrameFun.find_hard()
            pass
        elif filter_key == 7:
            r = FrameFun.find_today()
            pass
        RECORDS = r
        window = wx.FindWindowByName('ListControlOnRight', parent=None)
        window.load_data_right(RECORDS)


class Memo(wx.Frame):
    def __init__(self, parent, i, title, size):
        wx.Frame.__init__(self, parent, i, title=title, size=size)
        self._create_menu_bar()
        self._create_tool_bar()
        self._create_splitter_windows()
        self.Centre()
        self.Show(True)

    def _create_menu_bar(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        port_menu = wx.Menu()
        tool_menu = wx.Menu()
        help_menu = wx.Menu()

        menu_bar.Append(file_menu, '文件')
        menu_bar.Append(port_menu, '拓展')
        menu_bar.Append(tool_menu, '工具')
        menu_bar.Append(help_menu, '帮助')

        new_lib_item = file_menu.Append(-1, '添加一个词库')
        new_record_item = file_menu.Append(-1, '添加一条记录')
        setting = file_menu.Append(-1, '偏好设置')
        file_menu.AppendSeparator()
        quit_item = file_menu.Append(-1, '离开')

        import_lib = port_menu.Append(-1, '导入词库...')
        export_lib = port_menu.Append(-1, '导出词库...')

        study_item = tool_menu.Append(-1, '开始学习')
        check = tool_menu.Append(-1, '检查空记录')

        guide_item = help_menu.Append(wx.ID_HELP, '用户手册')
        about_item = help_menu.Append(wx.ID_ABOUT, '关于')

        self.Bind(wx.EVT_MENU, self.on_new_lib, new_lib_item)
        self.Bind(wx.EVT_MENU, self.on_new_record, new_record_item)
        self.Bind(wx.EVT_MENU, self.on_import, import_lib)
        self.Bind(wx.EVT_MENU, self.on_export, export_lib)
        self.Bind(wx.EVT_MENU, self.on_setting, setting)
        self.Bind(wx.EVT_MENU, self.on_quit, quit_item)
        self.Bind(wx.EVT_MENU, self.on_study, study_item)
        self.Bind(wx.EVT_MENU, self.on_check, check)
        self.Bind(wx.EVT_MENU, self.on_guide, guide_item)
        self.Bind(wx.EVT_MENU, self.on_about, about_item)

        self.SetMenuBar(menu_bar)

    def _create_tool_bar(self):
        tool_id = {'import': wx.NewId(),
                   'new_lib': wx.NewId(),
                   'new_record': wx.NewId(),
                   'setting': wx.NewId(),
                   'learn': wx.NewId()}
        tool_bar = self.CreateToolBar(style=wx.TB_FLAT | wx.TB_TEXT | wx.TB_HORZ_LAYOUT)
        quit_item = tool_bar.AddLabelTool(wx.ID_EXIT, '退出', wx.Bitmap('images/32/quit.png'))
        tool_bar.AddSeparator()
        import_item = tool_bar.AddLabelTool(tool_id['import'], '导入词库', wx.Bitmap('images/32/import.png'))
        new_lib = tool_bar.AddLabelTool(tool_id['new_lib'], '新建词库', wx.Bitmap('images/32/library_add.png'))
        new_record = tool_bar.AddLabelTool(tool_id['new_record'], '添加记录', wx.Bitmap('images/32/card_add.png'))
        setting = tool_bar.AddLabelTool(tool_id['setting'], '设置', wx.Bitmap('images/32/setting.png'))
        tool_bar.AddSeparator()
        study = tool_bar.AddLabelTool(tool_id['learn'], '开始学习', wx.Bitmap('images/32/words_learn.png'))

        self.Bind(wx.EVT_TOOL, self.on_quit, quit_item)
        self.Bind(wx.EVT_TOOL, self.on_setting, setting)
        self.Bind(wx.EVT_TOOL, self.on_new_lib, new_lib)
        self.Bind(wx.EVT_TOOL, self.on_import, import_item)
        self.Bind(wx.EVT_TOOL, self.on_new_record, new_record)
        self.Bind(wx.EVT_TOOL, self.on_study, study)

        tool_bar.Realize()

    def _create_splitter_windows(self):
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE | wx.SP_NOBORDER)
        splitter.SetMinimumPaneSize(250)
        vertical_box_left = wx.BoxSizer(wx.VERTICAL)
        panel_left = wx.Panel(splitter, -1)
        panel_left.SetBackgroundColour('white')
        panel_left_top = wx.Panel(panel_left, -1)
        panel_left_top.SetBackgroundColour('#53728c')
        panel_left_str = wx.StaticText(panel_left_top, -1, '记忆库', pos=(15, 10), size=(-1, 30))
        panel_left_str.SetForegroundColour('white')

        panel_left_bottom = wx.Panel(panel_left, -1, style=wx.BORDER_NONE)
        vertical_box_left_bottom = wx.BoxSizer(wx.VERTICAL)
        list_1 = ListCtrlLeft(panel_left_bottom, -1)
        list_1.SetName('ListControlOnLeft')
        vertical_box_left_bottom.Add(list_1, 1, wx.EXPAND)
        panel_left_bottom.SetSizer(vertical_box_left_bottom)
        panel_left_bottom.SetBackgroundColour('white')

        vertical_box_left.Add(panel_left_top, 0, wx.EXPAND)
        vertical_box_left.Add(panel_left_bottom, 1, wx.EXPAND)

        panel_left.SetSizer(vertical_box_left)

        # right
        vertical_box_right = wx.BoxSizer(wx.VERTICAL)
        panel_right = wx.Panel(splitter, -1)
        vertical_box_right_top = wx.BoxSizer(wx.VERTICAL)
        panel_right_top = wx.Panel(panel_right, size=(-1, 40), style=wx.NO_BORDER)
        combine = CombinePanelRight(panel_right_top, -1, RECORDS)
        vertical_box_right_top.Add(combine, 1, wx.EXPAND)
        panel_right_top.SetSizer(vertical_box_right_top)

        panel_right_bottom = wx.Panel(panel_right, -1, style=wx.BORDER_NONE)
        vertical_box_right_bottom = wx.BoxSizer(wx.VERTICAL)
        list2 = ListCtrlRight(panel_right_bottom, -1)
        list2.SetName('ListControlOnRight')
        vertical_box_right_bottom.Add(list2, 1, wx.EXPAND)
        panel_right_bottom.SetSizer(vertical_box_right_bottom)
        panel_right_bottom.SetBackgroundColour('white')

        vertical_box_right.Add(panel_right_top, 0, wx.EXPAND)
        vertical_box_right.Add(panel_right_bottom, 1, wx.EXPAND)

        panel_right.SetSizer(vertical_box_right)

        horizontal_box.Add(splitter, -1, wx.EXPAND | wx.TOP, 1)
        self.SetSizer(horizontal_box)
        splitter.SplitVertically(panel_left, panel_right, 250)

    def on_quit(self, evt):
        self.Close()
        evt.Skip()

    @staticmethod
    def on_setting(evt):
        setting_dlg = Dialog.SettingDialog(LIBRARIES, -1)
        setting_dlg.ShowModal()
        setting_dlg.Destroy()

    @staticmethod
    def on_new_lib(evt):
        new_lib_dlg = Dialog.AddNewLib()
        new_lib_dlg.ShowModal()
        new_lib_dlg.Destroy()

    def on_import(self, evt):
        import_dlg = Dialog.Import(self)
        import_dlg.ShowModal()
        import_dlg.Destroy()

    def on_export(self, evt):
        export_dlg = Dialog.Export(self)
        export_dlg.ShowModal()
        export_dlg.Destroy()

    @staticmethod
    def on_new_record(evt):
        new_card_dlg = Dialog.AddNewRecord(LIBRARIES, -1)
        new_card_dlg.ShowModal()
        new_card_dlg.Destroy()

    @staticmethod
    def on_study(evt):
        start_dlg = Dialog.SelectLib(LIBRARIES)
        start_dlg.ShowModal()
        start_dlg.Destroy()

    @staticmethod
    def on_check(evt):
        """
        检查和优化数据库，包括合并重复的记录，删除空记录
        :param evt:
        :return:
        """
        pass

    def on_guide(self, evt):
        f = open("Dialog.py", "r")
        msg = f.read()
        f.close()
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, msg, "用户手册")
        dlg.ShowModal()

    @staticmethod
    def on_about(evt):
        about_dlg = Dialog.AboutDialog()

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    app = wx.App()
    Memo(None, -1, 'PyMemo', (1000, 500))
    app.MainLoop()