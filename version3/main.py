from tkinter import Tk
from tkinter import Text
from tkinter import Menu

# parse.py与python包名冲突
from mylexer import Lexer
from myparser import Parser


textBox = None

def callLexer():
	# '1.0' 第一行第一列开始
	str = textBox.get('1.0', "end")
	# Lexer(string, show=False)
	# show=True显示分析过程
	tokens = Lexer(str, show=True)

def callParser():
	str = textBox.get('1.0', "end")
	# Parser(string, show=False)
	# show=True显示分析过程
	Parser(str, show=True)

def callPainter():
	str = textBox.get('1.0', "end")
	# Parser(string, show=False)
	# paint=True函数绘图
	Parser(str, paint=True)

def main():
	tk = Tk()
	tk.title("izcat's Interpreter for Functional Painting Language")
	tk.geometry("800x600")

	menuBar = Menu(tk)
	menuOpt = Menu(menuBar, tearoff=0)
	menuOpt.add_command(label="词法分析", command=callLexer)
	menuOpt.add_command(label="语法分析", command=callParser)
	menuOpt.add_command(label="函数绘图", command=callPainter)
	menuOpt.add_separator()
	menuBar.add_cascade(label="选择操作", menu=menuOpt)
	tk.config(menu=menuBar)

	global textBox
	textBox = Text(tk, width=800, height=300)
	textBox.pack()

	tk.mainloop()

if __name__=='__main__':
	main()

