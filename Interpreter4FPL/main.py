#-*- coding:utf-8 -*-
# @Time     : 2019/12/6 12:31
# @Author   : izcat
# @Site     : cnblogs.com/izcat
# @File     : main.py
# @Software : PyCharm
# @Desc     : 项目GUI与程序入口

from tkinter import Tk
from tkinter import Text
from tkinter import Menu
from tkinter import filedialog
import os

# parse.py与python包名冲突
from mylexer import Lexer
from myparser import Parser
from mypainter import Painter


textBox = None

def callLexer():
	# '1.0' 第一行第一列开始
	str = textBox.get('1.0', "end")
	# Lexer(string, show=False)
	# show=True显示分析过程
	Lexer(str, show=True)

def callParser():
	str = textBox.get('1.0', "end")
	# Parser(string, show=False)
	# show=True显示分析过程
	Parser(str, show=True)

def callPainter():
	str = textBox.get('1.0', "end")
	# 函数绘图
	Painter(str)

# 打开文件 显示到textBox上
def openFile():
	global textBox
	filePath = filedialog.askopenfilename(title=u'选择文件',
				initialdir=(os.path.expanduser(r"文件路径")))
	txtFile = open(filePath)
	content = txtFile.read()
	textBox.delete(0.0, "end")
	textBox.insert("insert", content)


def main():
	tk = Tk()
	tk.title("izcat's Interpreter for Functional Painting Language")
	tk.geometry("800x600")

	menuBar = Menu(tk)
	menuBar.add_command(label="文件", command=openFile)

	menuOpt = Menu(menuBar, tearoff=0)
	menuOpt.add_command(label="词法分析", command=callLexer)
	menuOpt.add_command(label="语法分析", command=callParser)
	menuOpt.add_command(label="函数绘图", command=callPainter)
	menuOpt.add_separator()
	menuBar.add_cascade(label="选择", menu=menuOpt)
	tk.config(menu=menuBar)

	global textBox
	textBox = Text(tk, width=800, height=300)
	textBox.pack()

	tk.mainloop()

if __name__=='__main__':
	main()

