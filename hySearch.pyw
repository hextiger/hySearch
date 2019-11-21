# -*- coding: utf-8 -*-

# hySearch -hyDots (C)Hextiger 2019-2020 (Since 2019.09.02) Web:hxhy.blog.home

import os.path
import time

import pandas as pd
import pypinyin
import wx
import wx.html


class hySearch(wx.Frame):
    def __init__(self, parent, dpath=".\\", dfile="data.zip"):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            pos=wx.DefaultPosition,
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL | wx.MAXIMIZE,
        )
        # 类初始化， dpath：数据文件路径 dfile:数据文件名  D82.2
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.t_search = wx.SearchCtrl(
            self,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_PROCESS_ENTER,
        )
        self.t_search.ShowSearchButton(True)
        self.t_search.ShowCancelButton(True)
        bSizer1.Add(self.t_search, 0, wx.ALL | wx.EXPAND, 5)
        bSizer12 = wx.BoxSizer(wx.VERTICAL)
        self.t_result = wx.html.HtmlWindow(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 | wx.BORDER_SIMPLE
        )
        bSizer12.Add(self.t_result, 1, wx.ALL | wx.EXPAND, 5)
        bSizer1.Add(bSizer12, 6, wx.EXPAND, 5)
        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        menu = wx.Menu()
        add = menu.Append(-1, "添加题库")
        about = menu.Append(-1, "说明")
        self.t_search.SetMenu(menu)
        # Connect Eventst_
        self.t_search.Bind(wx.EVT_TEXT, self.pressup)
        self.t_search.Bind(wx.EVT_TEXT_ENTER, self.click_search)
        self.t_search.Bind(wx.EVT_MENU, self.about, about)
        self.t_search.Bind(wx.EVT_MENU, self.add, add)
        self.dfile = dpath + dfile
        self.dpath = dpath
        if os.path.isfile(self.dfile):
            self.df = pd.read_pickle(self.dfile, compression="zip")
            self.about(-1)
        else:
            self.df = pd.DataFrame(columns=["M", "S", "P", "C"])
            self.t_result.SetPage("数据文件未找到！ 需要通过导入或录入方式建立数据文件data.zip")

    def about(self, event):
        # 关于说明  D83.1
        dmtime = time.gmtime(os.path.getmtime(self.dfile))
        dver = "{}{:0>2d}{:0>2d}".format(dmtime[0], dmtime[1], dmtime[2])
        count = str(len(self.df))
        info = self.df.at[0, "M"] + "<br>数据文件Data版本:" + dver + " 共计" + count + "条记录"
        self.t_result.SetPage(info)

    def importdata(self, selectclass = False):
        # 导入数据  D95.1
        # selectclass False:无需选class,默认N，True：选定class
        # "M"主信息, "S"突显信息, "P"拼音，"C"类别, "N"计数
        c = "M"
        if selectclass:
            msg = "N：正常信息，H：帮助信息， V：视频, M: 客户自行添加"
            dialog0 = wx.TextEntryDialog(
            None, msg, "题库类型", "N", style=wx.OK | wx.CANCEL
        )
            if dialog0.ShowModal() == wx.ID_OK:
                c1 = dialog0.GetValue()
            dialog0.Destroy()
        msg = (
            "增加题库格式为：[AAA/BB]，其中AAA为题目，BB为答案，中间用/分割，每行1题,[]无需输入。\n"
            "如需从data.txt导入，请输入txt"
        )
        dialog1 = wx.TextEntryDialog(
            None, msg, "增加题库", "", style=wx.OK | wx.CANCEL | wx.TE_MULTILINE
        )
        if dialog1.ShowModal() == wx.ID_OK:
            value = dialog1.GetValue().split("\n")
            if value[0] == "txt":
                # 从data.txt文件导入
                f = open(self.dpath + "data.txt", "r", encoding="utf-8")
                value = f.readlines()
            df = pd.DataFrame(columns=["M", "S", "P", "C"])
            i = 0
            for line in value:
                if line[-1] == "\n":
                    # 文件导入时需要删除多余的换行符
                    line = line[:-1]
                if line[-1] == "r":
                    # 最后一个字符为r时，忽略该行
                    continue
                v = line.split("/")
                m = v[0]
                if len(v) == 2:
                    s = line.split("/")[1]
                else:
                    s = ""
                qpylist = pypinyin.lazy_pinyin(
                    m, style=pypinyin.Style.FIRST_LETTER, strict=False, errors="ignore"
                )
                p = "".join(qpylist)
                df.loc[i] = [m, s, p, c]
                i += 1
            self.df = pd.concat([self.df, df], axis=0)
            self.df = self.df.drop_duplicates(["P"])
            self.df.sort_values("P", inplace=True)
            self.df = self.df.reset_index(drop=True)
            self.df.to_pickle(self.dfile, compression="zip")
            dialog1.Destroy()
            return "数据已导入，当前题库共计" + str(len(self.df)) + "条"

    def add(self, event):
        # 添加数据  D39.7
        self.t_result.SetPage(self.importdata())

    def pressup(self, event):
        # 搜索框内容变更 D34.3
        self.search(self.t_search.GetValue())

    def click_search(self, event):
        # 点击搜索按钮 D35.4
        self.t_search.Clear()

    def search(self, key):
        # 搜索[key]拼音首字母对应的题目和答案 D37.3
        s = ""
        if key != "":
            rdf1 = self.df.loc[self.df["P"].str.contains(key)]
            rdf2 = self.df.loc[self.df["M"].str.contains(key)]
            rdf = pd.concat([rdf1, rdf2], axis=0)
            for idx, row in rdf.iterrows():
                s += (
                        '<font color="black">'
                        + row["M"]
                        + "</font><br>"
                        + '<font color="red">'
                        + "【"
                        + row["S"]
                        + "】"
                        + "</font><br>"
                )
            self.t_result.SetPage(s)


if __name__ == "__main__":
    # 直接运行hySearch  D84.1
    app = wx.App()
    frm = hySearch(None)
    frm.Show()
    app.MainLoop()
