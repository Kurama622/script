# #!/usr/bin/env python3
# -*- coding:UTF-8 -*-
###############################################################
# File Name: dialog.py
# Author: stubborn vegeta
# Created Time: Sun 20 Sep 2020 10:39:13 PM CST
###############################################################
from SuperClearCR import *
import tkinter
from tkinter import messagebox as tm
from tkinter import Tk


if __name__ == '__main__':
    clipStringPre = pyperclip.paste()          # getclip
    cliplistpre = list(clipStringPre)
    JudgeChar(cliplistpre)
    clipStringPre = ''.join(cliplistpre)
    pyperclip.copy(clipStringPre)
    start = True
    while start:
        clipString = pyperclip.paste()          # getclip
        cliplist = list(clipString)
        JudgeChar(cliplist)
        clipString = ''.join(cliplist)
        pyperclip.copy(clipString)
        if clipString != clipStringPre:
            root = Tk()
            def func(event):
                if event.keycode == 66:
                    root.destroy()
            root.attributes('-type', 'dialog')
            root.bind('<Key>', func)
            clipStringPre = clipString
            newString = clipString
            print(newString)
            yd = Google()
            youdao_api = yd.google_api(newString)
            data = newString + '\n' + youdao_api + '\n'
            ChineseText = youdao_api + '\n'
            text = tm.showinfo(message=youdao_api)
            # text=tkinter.Text(font='微软雅黑')
            # text.insert(tkinter.END, youdao_api)
            text.pack()
            root.mainloop()
