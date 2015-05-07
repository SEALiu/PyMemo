import wx


class ListCtrlLeft(wx.ListCtrl):
    def __init__(self, parent, i):
        wx.ListCtrl.__init__(self, parent, i, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)
        self.parent = parent
        self.Bind(wx.EVT_SIZE, self.on_size)

        self.InsertColumn(0, '')
        self.InsertStringItem(0, 'library-one')
        self.InsertStringItem(0, 'library-two')
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_lib_select)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_lib_right_click)

    def on_size(self, event):
        size = self.parent.GetSize()
        self.SetColumnWidth(0, size.x - 5)

    def on_lib_select(self, evt):
        print "Item selected"

    def on_lib_right_click(self, evt):
        print "Item right-clicked"


class Memo(wx.Frame):
    def __init__(self, parent, i, title, size):
        wx.Frame.__init__(self, parent, i, title=title, size=size)
        self._create_splitter_windows()
        self.Centre()
        self.Show(True)

    def _create_splitter_windows(self):
        horizontal_box = wx.BoxSizer(wx.HORIZONTAL)
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE | wx.SP_NOBORDER)
        splitter.SetMinimumPaneSize(250)
        vertical_box_left = wx.BoxSizer(wx.VERTICAL)
        panel_left = wx.Panel(splitter, -1)
        panel_left_top = wx.Panel(panel_left, -1, size=(-1, 30))
        panel_left_top.SetBackgroundColour('#53728c')
        panel_left_str = wx.StaticText(panel_left_top, -1, 'Libraries', (5, 5))
        panel_left_str.SetForegroundColour('white')

        panel_left_bottom = wx.Panel(panel_left, -1, style=wx.BORDER_NONE)
        vertical_box_left_bottom = wx.BoxSizer(wx.VERTICAL)
        # Here!!!!
        list_1 = ListCtrlLeft(panel_left_bottom, -1)
        # ----------
        vertical_box_left_bottom.Add(list_1, 1, wx.EXPAND)
        panel_left_bottom.SetSizer(vertical_box_left_bottom)

        vertical_box_left.Add(panel_left_top, 0, wx.EXPAND)
        vertical_box_left.Add(panel_left_bottom, 1, wx.EXPAND)

        panel_left.SetSizer(vertical_box_left)

        # right
        vertical_box_right = wx.BoxSizer(wx.VERTICAL)
        panel_right = wx.Panel(splitter, -1)

        panel_right.SetSizer(vertical_box_right)

        horizontal_box.Add(splitter, -1, wx.EXPAND | wx.TOP, 1)
        self.SetSizer(horizontal_box)
        splitter.SplitVertically(panel_left, panel_right, 250)

    def on_quit(self, evt):
        self.Close()
        evt.Skip()

if __name__ == "__main__":
    app = wx.App()
    Memo(None, -1, 'PyMemo', (500, 300))
    app.MainLoop()