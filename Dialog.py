# -*- coding: gbk -*-
import wx
# import FrameFun


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
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '�ʿ�����', size=(200, 400),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        v_box = wx.BoxSizer(wx.VERTICAL)

        panel_combo = wx.Panel(self, -1)
        h_box_combo = wx.BoxSizer(wx.HORIZONTAL)
        lib_text = wx.StaticText(panel_combo, -1, "��������Щ����Ӧ�����ĸ��ʿ��ϣ�")
        lib_items = ['��ѡ��ʿ�',
                     '��Ƶ�ּ��ʻ��',
                     '��Ƶ�ּ��ʻ���',
                     '��Ƶ�ּ��ʻ���',
                     'CET-4��Ƶ�ʻ�']
        lib_combo_box = wx.ComboBox(panel_combo, choices=lib_items, style=wx.CB_READONLY)
        lib_combo_box.SetSelection(0)
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
        study_limit.SetValue(80)

        review_limit = wx.SpinCtrl(panel_right_top, -1)
        review_limit.SetRange(1, 200)
        review_limit.SetValue(80)

        deadline_limit = wx.SpinCtrl(panel_right_top, -1)
        deadline_limit.SetRange(1, 60)
        deadline_limit.SetValue(10)

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

        sbs3.Add(old_after_new, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=10)
        sbs3.Add(new_after_old, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=10)
        sbs3.Add(new_or_old, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM, border=10)

        panel_left_bottom.SetSizer(sbs3)

        grid_sizer.Add(panel_left_bottom, 1, wx.EXPAND | wx.ALL, border=10)

        # (1, 1)
        panel_right_bottom = wx.Panel(self)
        font_setting = wx.StaticBox(panel_right_bottom, -1, label='��������')
        sbs4 = wx.StaticBoxSizer(font_setting, orient=wx.VERTICAL)
        h_box_1 = wx.BoxSizer(wx.HORIZONTAL)
        h_box_2 = wx.BoxSizer(wx.HORIZONTAL)

        font_family_list = ['font-family-one',
                           'font-family-two',
                           'font-family-three',
                           'font-family-flour']
        font_family_text = wx.StaticText(panel_right_bottom, -1, "���壺",)
        font_family = wx.Choice(panel_right_bottom, -1, choices=font_family_list)

        h_box_1.Add(font_family_text, 1, wx.LEFT | wx.TOP, border=10)
        h_box_1.Add(font_family, 3, wx.TOP, border=10)

        font_size_text = wx.StaticText(panel_right_bottom, -1, "�ֺţ�")
        font_size = wx.SpinCtrl(panel_right_bottom, -1)
        font_size.SetRange(1, 30)
        font_size.SetValue(12)

        h_box_2.Add(font_size_text, 1, wx.LEFT | wx.TOP, border=10)
        h_box_2.Add(font_size, 3, wx.TOP, border=10)

        sbs4.Add(h_box_1, wx.LEFT, border=5)
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


class CardInfoDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '���ʿ�Ƭ��ϸ��Ϣ', size=(300, 400),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        info_dir = {1: ['���ʱ��', '2015-3-24'],
                   2: ['�״�ѧϰ', '2015-3-24'],
                   3: ['�����ϰ', '2015-3-24'],
                   4: ['����ʱ��', '2015-3-24'],
                   5: ['���', '9��'],
                   6: ['��ϰ����', '2'],
                   7: ['�������', '2'],
                   8: ['�����ʿ�', 'CET-4��Ƶ�ʻ�'],
                   9: ['��ƬID', '15456468465'],
                   10: ['�ʿ�ID', '564645635218']}

        v_box = wx.BoxSizer(wx.VERTICAL)
        head_title = wx.StaticText(panel, label="���ʿ�Ƭ����ϸ��Ϣ")
        add_time = wx.StaticText(panel, label=info_dir[1][0] + " " * 6 + info_dir[1][1])
        first_study_time = wx.StaticText(panel, label=info_dir[2][0] + " " * 6 + info_dir[2][1])
        review_time = wx.StaticText(panel, label=info_dir[3][0] + " " * 6 + info_dir[3][1])
        dead_line = wx.StaticText(panel, label=info_dir[4][0] + " " * 6 + info_dir[4][1])
        interval_day = wx.StaticText(panel, label=info_dir[5][0] + " " * 6 + info_dir[5][1])
        review_num = wx.StaticText(panel, label=info_dir[6][0] + " " * 6 + info_dir[6][1])
        error_num = wx.StaticText(panel, label=info_dir[7][0] + " " * 6 + info_dir[7][1])
        belong_lib = wx.StaticText(panel, label=info_dir[8][0] + " " * 6 + info_dir[8][1])
        record_id = wx.StaticText(panel, label=info_dir[9][0] + " " * 6 + info_dir[9][1])
        lib_id = wx.StaticText(panel, label=info_dir[10][0] + " " * 6 + info_dir[10][1])

        v_box.Add(head_title, 1, wx.CENTER | wx.TOP, border=10)
        v_box.Add(add_time, 1, wx.ALL, border=10)
        v_box.Add(first_study_time, 1, wx.ALL, border=10)
        v_box.Add(review_time, 1, wx.ALL, border=10)
        v_box.Add(dead_line, 1, wx.ALL, border=10)
        v_box.Add(interval_day, 1, wx.ALL, border=10)
        v_box.Add(review_num, 1, wx.ALL, border=10)
        v_box.Add(error_num, 1, wx.ALL, border=10)
        v_box.Add(belong_lib, 1, wx.ALL, border=10)
        v_box.Add(record_id, 1, wx.ALL, border=10)
        v_box.Add(lib_id, 1, wx.ALL, border=10)

        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)


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
        close_button = wx.Button(panel, -1, label='ȡ��')
        h_box.Add(ok_button, 1, wx.RIGHT, border=5)
        h_box.Add(close_button, 1)

        v_box.Add(name_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)
        v_box.Add(lib_name, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(desc_text, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        v_box.Add(lib_desc, 0, wx.EXPAND | wx.ALL, 10)
        v_box.Add(h_box, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        panel.SetSizer(v_box)
        self.Centre()
        self.Show(True)


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


class AddNewRecord(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, '����һ����¼', size=(-1, 350),
                           style=wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)
        panel = wx.Panel(self, -1)
        v_box = wx.BoxSizer(wx.VERTICAL)
        h_box_info = wx.BoxSizer(wx.HORIZONTAL)

        lib_items = ['��ѡ�������ʿ�',
                     '��Ƶ�ּ��ʻ��',
                     '��Ƶ�ּ��ʻ���',
                     '��Ƶ�ּ��ʻ���',
                     'CET-4��Ƶ�ʻ�']
        lib_combo_box = wx.ComboBox(panel, choices=lib_items, style=wx.CB_READONLY)
        lib_combo_box.SetSelection(0)

        preview = wx.BitmapButton(panel, -1, wx.Bitmap('images/32/preview.png'), size=(32, 32), style=wx.NO_BORDER)
        h_box_info.Add(lib_combo_box, 1, wx.TOP | wx.RIGHT, 10)
        h_box_info.Add(preview, 0, wx.ALIGN_RIGHT | wx.TOP, 6)

        name_text = wx.StaticText(panel, -1, "���⣨���棩��")
        record_ques = wx.TextCtrl(panel, -1, "", size=(-1, 80), style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

        desc_text = wx.StaticText(panel, -1, "�𰸣����棩��")
        record_ans = wx.TextCtrl(panel, -1, "", size=(-1, 80), style=wx.TE_MULTILINE | wx.TE_NO_VSCROLL)

        h_box_btn = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(panel, -1, label='ȷ��')
        close_button = wx.Button(panel, -1, label='ȡ��')
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


class StartMemoQues(wx.Dialog):
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
        dlg = StartMemoAns()
        dlg.ShowModal()
        dlg.Destroy()
        evt.Skip()


class StartMemoAns(wx.Dialog):
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