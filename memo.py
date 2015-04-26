# -*- coding: gbk -*-
# memo.py
import sys
import wx
import Dialog
import DBFun
import wx.lib.dialogs

LIBRARIES = {}
RECORDS = []
LIBRARY_ID = []


class ListCtrlLeft(wx.ListCtrl):
    def __init__(self, parent, i):
        wx.ListCtrl.__init__(self, parent, i, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)
        self.parent = parent
        self.Bind(wx.EVT_SIZE, self.on_size)
        # self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select)
        self.load_data_left()

    @staticmethod
    def fetch_lib():
        conn = DBFun.connect_db('db_pymemo.db')
        conn.text_factory = str
        select_sql = "SELECT * FROM library"
        cursor = DBFun.select(conn, select_sql)
        result_list = cursor.fetchall()
        DBFun.close_db(conn)

        library_id = []
        for rows in result_list:
            LIBRARY_ID.append(rows[0])
            LIBRARIES[rows[0]] = rows[1]

        return library_id

    def load_data_left(self):
        LIBRARY_ID = self.fetch_lib()

        self.il = wx.ImageList(32, 32)
        lib_img = wx.Bitmap('images/32/library.png')
        for i in range(len(LIBRARIES)):
            self.il.Add(lib_img)

        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, '')

        for index, element in enumerate(LIBRARIES):
            self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_lib_clicked)
            self.InsertStringItem(0, LIBRARIES[element].decode('utf-8'))
            self.SetItemImage(0, index)


    def on_size(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x - 5)
        event.Skip()

    # def on_select(self, event):
    #     print 'hi,click me!'
    #     window = self.parent.GetGrandParent().FindWindowByName('ListControlOnRight')
    #     index = event.GetIndex()
    #     lib_id = LIBRARY_ID[index]
    #     print 'lib_id:', lib_id
    #     conn = DBFun.connect_db('db_pymemo.db')
    #     conn.text_factory = str
    #     select_sql = "SELECT * FROM record WHERE recordId LIKE '%" + lib_id + "'"
    #     cursor = DBFun.select(conn, select_sql)
    #     RECORDS = cursor.fetchall()
    #     DBFun.close_db(conn)
    #     # print 'RECORDS: ', RECORDS
    #     window.load_data_right(RECORDS)

    def on_lib_clicked(self, event):
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

    def on_lib_rename(self, evt, i):
        global lib_desc
        lib_id = LIBRARY_ID[i]
        lib_name = LIBRARIES[LIBRARY_ID[i]].decode('utf-8')
        conn = DBFun.connect_db('db_pymemo.db')
        conn.text_factory = str
        select_sql = "SELECT * FROM library WHERE libId = '" + lib_id + "'"
        cursor = DBFun.select(conn, select_sql)
        for rows in cursor:
            lib_desc = rows[2].decode('utf-8')
        DBFun.close_db(conn)

        rename_dlg = Dialog.RenameLib(lib_name, lib_desc, lib_id)
        rename_dlg.ShowModal()
        rename_dlg.Destroy()
        pass

    def on_item_info(self, evt, i):
        pass

    def on_item_add(self, evt, i):
        pass

    def on_lib_setting(self, evt, i):
        print "setting", LIBRARIES[LIBRARY_ID[i]]
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
        conn = DBFun.connect_db('db_pymemo.db')
        conn.text_factory = str
        select_sql = 'SELECT * FROM record'
        cursor = DBFun.select(conn, select_sql)
        RECORDS = cursor.fetchall()
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
            for j in range(len(self.list_head_name)):
                self.SetStringItem(index, j, str(i[j]))
        # print 'RECORDS: ', RECORDS


class CombinePanelRight(wx.Panel):
    def __init__(self, parent, i):
        wx.Panel.__init__(self, parent, i, style=wx.BORDER_NONE)

        lib_items = ['请选择筛选条件',
                     '当前词库所有的',
                     '正在学习的',
                     '已到期的',
                     '已记住的',
                     '今天已学习的',
                     '始终记不住的',
                     '今天添加的'
                     ]
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        lib_combo_box = wx.ComboBox(self,
                                    pos=(0, 5),
                                    choices=lib_items,
                                    style=wx.CB_READONLY
                                    )
        lib_combo_box.SetSelection(0)
        # lib_combo_box.Bind(wx.EVT_COMBOBOX, self.on_select)
        go = wx.BitmapButton(self,
                             -1,
                             wx.Bitmap('images/other-size/search26.png'),
                             size=(23, 25),
                             style=wx.NO_BORDER
                             )
        search_ctrl = wx.TextCtrl(self, -1)

        horizontal_box.Add(lib_combo_box, 1, wx.TOP | wx.LEFT, border=6)
        horizontal_box.Add(search_ctrl, 1, wx.TOP | wx.LEFT, border=6)
        horizontal_box.Add(go, 0, wx.ALL, border=6)

        self.SetSizer(horizontal_box)
        self.Centre()
        self.Show(True)


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
        panel_left_top = wx.Panel(panel_left, -1, size=(-1, 30))
        panel_left_top.SetBackgroundColour('#53728c')
        panel_left_str = wx.StaticText(panel_left_top, -1, '记忆库', (5, 5))
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
        combine = CombinePanelRight(panel_right_top, -1)
        vertical_box_right_top.Add(combine, 1, wx.EXPAND)
        panel_right_top.SetSizer(vertical_box_right_top)
        # panel_right_top.SetBackgroundColour('#53728c')

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
        setting_dlg = Dialog.SettingDialog()
        setting_dlg.ShowModal()
        setting_dlg.Destroy()
        evt.Skip()

    @staticmethod
    def on_new_lib(evt):
        new_lib_dlg = Dialog.AddNewLib()
        new_lib_dlg.ShowModal()
        new_lib_dlg.Destroy()
        evt.Skip()

    def on_import(self, evt):
        import_dlg = Dialog.Import(self)
        import_dlg.ShowModal()
        import_dlg.Destroy()
        evt.Skip()

    def on_export(self, evt):
        export_dlg = Dialog.Export(self)
        export_dlg.ShowModal()
        export_dlg.Destroy()
        evt.Skip()

    @staticmethod
    def on_new_record(evt):
        new_card_dlg = Dialog.AddNewRecord()
        new_card_dlg.ShowModal()
        new_card_dlg.Destroy()
        evt.Skip()

    @staticmethod
    def on_study(evt):
        start_dlg = Dialog.MemoQues()
        start_dlg.ShowModal()
        start_dlg.Destroy()
        evt.Skip()

    def on_check(self, evt):
        pass

    def on_guide(self, evt):
        f = open("Dialog.py", "r")
        msg = f.read()
        f.close()
        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, msg, "用户手册")
        dlg.ShowModal()
        evt.Skip()

    @staticmethod
    def on_about(evt):
        Dialog.AboutDialog()
        evt.Skip()


def main():
    reload(sys)
    sys.setdefaultencoding('gbk')
    app = wx.App()
    Memo(None, -1, 'PyMemo', (1000, 500))
    app.MainLoop()

if __name__ == '__main__':
    main()