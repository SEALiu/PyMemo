import wx

########################################################################
class MyForm(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "List Control Tutorial")

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.index = 0

        self.list_ctrl = wx.ListCtrl(panel, size=(-1,100),
                                     style=wx.LC_REPORT
                                     |wx.BORDER_SUNKEN
                                     )
        self.list_ctrl.InsertColumn(0, 'Subject')
        self.list_ctrl.InsertColumn(1, 'Due')
        self.list_ctrl.InsertColumn(2, 'Location', width=125)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onItemSelected)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)
        self.add_line('')

        btn = wx.Button(panel, label="Add Line")
        btn.Bind(wx.EVT_BUTTON, self.add_line)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_ctrl, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(sizer)

    #----------------------------------------------------------------------
    def add_line(self, event):
        line = "Line %s" % self.index
        self.list_ctrl.InsertStringItem(self.index, line)
        self.list_ctrl.SetStringItem(self.index, 1, "01/19/2010")
        self.list_ctrl.SetStringItem(self.index, 2, "USA")
        self.index += 1

    #----------------------------------------------------------------------
    def onItemSelected(self, event):
        """"""
        print "Item selected"

    #----------------------------------------------------------------------
    def onRightClick(self, event):
        """"""
        print "Item right-clicked"

#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()