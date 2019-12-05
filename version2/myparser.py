from mylexer import Lexer
from expnode import *
from mypainter import *
import math
import sys

########################################
# 语法分析器
########################################

tokenIter = None
tokenNow = Token(TokenType.NONTOKEN, '')
showProcess = False

Origin_x = 0.0
Origin_y = 0.0
Scale_x = 1.0
Scale_y = 1.0
Rot_angle = 0.0



def setDefaultValue(show):
	global Origin_x
	global Origin_y
	global Scale_x
	global Scale_y
	global Rot_angle
	global showProcess # 没有global showProcess一直为False
	Origin_x = 0.0
	Origin_y = 0.0
	Scale_x = 1.0
	Scale_y = 1.0
	Rot_angle = 0.0
	showProcess = show



# 从词法分析器的tokens获得token
def FetchToken():
	global tokenNow
	try:
		tokenNow = next(tokenIter)
		return tokenNow
	except StopIteration:
		sys.exit()

def MatchToken(tokenType, show=False):
	if show:
		tokenNow.show()
	if tokenNow.tokenType==tokenType:
		FetchToken()
		return True
	else:
		print("Excepted ", tokenType, "received ", tokenNow.tokenType)
		print("error!")
		return False
		exit(-1)


def Msg(op, str):
	global showProcess
	if not showProcess:
		return
	if op==0:
		print("Enter %s" % str)
	else:
		print("Exit %s" % str)


##########################################
# 表达式
# ########################################

# 二叉树节点
# + - * / ** T CONST_ID FUNC
# '('  ')' 匹配过程中扔掉
# 叶子节点： T CONST_ID
# 非叶子节点： 非终结符

# 加法运算 
# 左结合
# 新的 + - 为根节点
# Example： 1+2-3
#     -
#    / \
#   +   3
#  / \
# 1   2
# 

def Expression():
	Msg(0, "Expression")
	left = Term()
	root = None
	while tokenNow.tokenType==TokenType.PLUS or tokenNow.tokenType==TokenType.MINUS:
		root = ExpNode(tokenNow)
		MatchToken(tokenNow.tokenType)
		right = Term()
		root.addson(left)
		root.addson(right)
		left = root
		# left.dfs()
	Msg(1, "Expression")
	return left

# def Expression():
# 	Msg(0, "Expression")
# 	left = Term()
# 	root = None
# 	while tokenNow.tokenType==TokenType.PLUS or tokenNow.tokenType==TokenType.MINUS:
# 		root = ExpNode(tokenNow)
# 		MatchToken(tokenNow.tokenType)
# 		right = Expression()
# 		root.addson(left)
# 		root.addson(right)
# 		left = root
# 	Msg(1, "Expression")
# 	return left

# 乘法运算 
# 左结合
# 新的 * / 为根节点
# Example： 1*2*3
#     *
#    / \
#   *   3
#  / \
# 1   2
def Term():
	Msg(0, "Term")
	left = Factor()
	root = None
	while tokenNow.tokenType==TokenType.MUL or tokenNow.tokenType==TokenType.DIV:
		root = ExpNode(tokenNow)
		MatchToken(tokenNow.tokenType)
		right = Factor()
		root.addson(left)
		root.addson(right)
		left = root

	Msg(1, "Term")
	return left

def Factor():
	Msg(0, "Factor")
	if tokenNow.tokenType==TokenType.PLUS or tokenNow.tokenType==TokenType.MINUS:
		root = ExpNode(tokenNow)
		MatchToken(tokenNow.tokenType);
		son = Factor()	
		root.addson(son)
		Msg(1, "Factor")
		return root
	else:
		Msg(1, "Factor")
		return Component()		

# 乘方运算
# 右结合
# 不支持 CONST_ID ** MINUS CONST_ID, 需要添括号
def Component():
	Msg(0, "Component")
	left = Atom()
	if tokenNow.tokenType==TokenType.POWER:
		root = ExpNode(tokenNow)
		MatchToken(tokenNow.tokenType)
		right = Component()

		root.addson(left)
		root.addson(right)
		Msg(1, "Component")
		return root
	else:
		Msg(1, "Component")
		return left

# 函数节点 FUNC <- CONST_ID | T
# 叶子节点 CONST_ID | T
def Atom():
	Msg(0, "Atom")
	if tokenNow.tokenType==TokenType.CONST_ID or tokenNow.tokenType==TokenType.T:
		root = ExpNode(tokenNow)
		MatchToken(tokenNow.tokenType)
		Msg(1, "Atom")
		return root

	elif tokenNow.tokenType==TokenType.FUNC:
		root = ExpNode(tokenNow)
		MatchToken(tokenNow.tokenType)
		MatchToken(TokenType.L_BRACKET)
		son = Expression()
		MatchToken(TokenType.R_BRACKET)
		root.addson(son)
		Msg(1, "Atom")
		return root

	elif tokenNow.tokenType==TokenType.L_BRACKET:
		MatchToken(TokenType.L_BRACKET)
		root = Expression()
		MatchToken(TokenType.R_BRACKET)
		Msg(1, "Atom")
		return root
	else:
		print("Atom Error!")



def OriginStatement():
	Msg(0, "OriginStatement")
	global Origin_x
	global Origin_y
	MatchToken(TokenType.ORIGIN)
	MatchToken(TokenType.IS)
	MatchToken(TokenType.L_BRACKET)
	Origin_x = Expression().getValue()
	MatchToken(TokenType.COMMA)
	Origin_y = Expression().getValue()
	MatchToken(TokenType.R_BRACKET)

	Msg(1, "OriginStatement")

def	ScaleStatement():
	Msg(0, "ScaleStatement")
	global Scale_x
	global Scale_y
	MatchToken(TokenType.SCALE)
	MatchToken(TokenType.IS)
	MatchToken(TokenType.L_BRACKET)
	Scale_x = Expression().getValue()
	MatchToken(TokenType.COMMA)
	Scale_y = Expression().getValue()
	# print(Scale_x)
	# print(Scale_y)
	MatchToken(TokenType.R_BRACKET)

	Msg(1, "ScaleStatement")

def	RotStatement():
	Msg(0, "RotStatement")
	global Rot_angle
	MatchToken(TokenType.ROT)
	MatchToken(TokenType.IS)
	Rot_angle = Expression().getValue()

	Msg(1, "RotStatement")

def	ForStatement():
	Msg(0, "ForStatement")
	MatchToken(TokenType.FOR)
	MatchToken(TokenType.T)
	MatchToken(TokenType.FROM)
	T_start = Expression().getValue()
	MatchToken(TokenType.TO)
	T_end = Expression().getValue()
	MatchToken(TokenType.STEP)
	T_step = Expression().getValue()

	
	MatchToken(TokenType.DRAW)
	MatchToken(TokenType.L_BRACKET)
	Point_x = Expression()
	MatchToken(TokenType.COMMA)
	Point_y = Expression()
	MatchToken(TokenType.R_BRACKET)

	# global T_value
	Painter.set(Origin_x, Origin_y, Scale_x, Scale_y, Rot_angle)
	Painter.paint(T_start, T_end, T_step, Point_x, Point_y)

	Msg(1, "ForStatement")

# Statement -> OriginStatement | ScaleStatement | RotStatement | ForStatement
def Statement():
	Msg(0, "Statement")
	if tokenNow.tokenType==TokenType.ORIGIN:
		OriginStatement()
	elif tokenNow.tokenType==TokenType.SCALE:
		ScaleStatement()
	elif tokenNow.tokenType==TokenType.ROT:
		RotStatement()
	elif tokenNow.tokenType==TokenType.FOR:
		ForStatement()
	else:
		print("Statement Error!")

	Msg(0, "Statement")


def Program():
	Msg(0, "Program")
	while tokenNow.tokenType!=TokenType.NONTOKEN:
		Statement()
		matched = MatchToken(TokenType.SEMICO)
		if not matched:
			print("Program Error")
			break
	Msg(1, "Program")

def Parser(string, show=False, paint=False):
	global tokenIter			# 必须要 global

	# 调用词法分析器 得到记号表
	tokenList = Lexer(string)
	tokenIter = iter(tokenList)

	setDefaultValue(show)
	FetchToken()
	Program()

	if paint:
		Painter.showPic()



def test():
	# Parser("--hello fad\n  //fadfjl\n ROT is pi/2   ; SCALE is (  1, 2*2);   \n   ORIGIN is ((2), 242/4);")
	str = "ORigin is (-30, 0); SCALE is (  20, 25); for t from 0 to 2*pi step 0.01 draw (sin(t), cos(t));  SCALE is (  30, 20); for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, t);for t from -1 to 1 step 0.01 draw (2, t); FOR t from 0 to 1 step 0.01 draw (2+t, -t);for t from 0 to 2*pi step 0.01 draw (1+3*sin(t), 3*cos(t)); "

	Parser(str);
	# print("(%f, %f)" % (Origin_x, Origin_y))
	# print("(%f, %f)" % (Scale_x, Scale_y))
	# print("%f" % Rot_angle)

	Painter.showPic()

# test()