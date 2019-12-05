# 表达式产生式 - 消除二义性、左递归

# Expression -> Term Expression'
# Expression' -> (PLUS | MINUS) Term Expression' | $
# 
# Term -> Factor Term'
# Term' -> (MUL | DIV) Factor | $
# 
# Factor -> (PLUS | MINUS) Factor | Component
# 
# Component -> Atom POWER Component | Atom
# 
# Atom -> CONST_ID | T 
# 		| FUNC L_BRACKET Expression R_BRACKET
# 		| L_BRACKET Expression R_BRACKET
# 		

# EBNF
# Expression -> Term { (PLUS | MINUS) Term }
# 
# Term -> Factor { (MUL | DIV) Factor }
# 
# Factor -> (PLUS | MINUS) Factor | Component
# 
# Component -> Atom POWER Component | Atom
# 
# Atom -> CONST_ID | T 
# 		| FUNC L_BRACKET Expression R_BRACKET
# 		| L_BRACKET Expression R_BRACKET



from lexer import *
import sys
# 二叉树节点
# + - * / ** T CONST_ID FUNC
# '('  ')' 匹配过程中扔掉
# 叶子节点： T CONST_ID
# 非叶子节点： 非终结符

T_value = 0.0

class ExpNode:
	def __init__(self, token, left=None, right=None):
		self.token = token
		self.lson = left
		self.rson = right
	def addson(self, son):
		if self.lson==None:
			self.lson = son
			return self
		elif self.rson==None:
			self.rson = son
			return self
		else:
			print("Cannot add son!")
			exit(-1)

	def getValue(self):
		# 叶子节点
		if self.lson==None and self.rson==None:
			if self.token.tokenType==TokenType.CONST_ID:
				return self.token.value
			elif self.token.tokenType==TokenType.T:
				return T_value
			else:
				print("Expression Error")
				exit(-1)

		# 只有左子树	函数节点	or +5 or -5
		elif self.rson==None:
			if self.token.tokenType==TokenType.PLUS:
				return self.lson.getValue()
			elif self.token.tokenType==TokenType.MINUS:
				return -self.lson.getValue()
			elif self.token.tokenType==TokenType.FUNC:
				return self.token.funcPtr(self.lson.getValue())
			else:
				print("Expression Error")
				exit(-1)
		# 只有右子树
		# elif self.lson==None:
		# 	if self.token.tokenType==TokenType.PLUS:
		# 		return self.rson.getValue()
		# 	elif self.token.tokenType==TokenType.MINUS:
		# 		return -self.rson.getValue()
		# 	elif self.token.tokenType==TokenType.FUNC:
		# 		return self.token.funcptr(self.rson.getValue())
		# 	else:
		# 		print("Expression Error")
		else:
			if self.token.tokenType==TokenType.PLUS:
				return self.lson.getValue() + self.rson.getValue()
			elif self.token.tokenType==TokenType.MINUS:
				return self.lson.getValue() - self.rson.getValue()
			elif self.token.tokenType==TokenType.MUL:
				return self.lson.getValue() * self.rson.getValue()
			elif self.token.tokenType==TokenType.DIV:
				return self.lson.getValue() / self.rson.getValue()
			elif self.token.tokenType==TokenType.POWER:
				return self.lson.getValue() ** self.rson.getValue()
			else:
				print("Expression Error")
				exit(-1)

	def dfs(self, depth=0):
		if self.lson!=None:
			self.lson.dfs(depth+1)
		if self.rson!=None:
			self.rson.dfs(depth+1)

		print("Depth %d" % depth)
		self.token.show()


tokenIter = None
tokenNow = Token(TokenType.NONTOKEN, '')

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
	else:
		print("Excepted ", tokenType, "received ", tokenNow.tokenType)
		print("error!")
		exit(-1)

def Parser(string):
	global tokenIter			# 必须要 global
	tokenList = Lexer(string)
	tokenIter = iter(tokenList)
	FetchToken()
	exp = Expression()
	print("--------------------")

	# exp.token.show()
	# print(exp.lson)
	# print(exp.rson)
	exp.dfs()
	print(exp.getValue())

def Msg(op, str):
	if op==0:
		print("Enter %s" % str)
	else:
		print("Exit %s" % str)

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


# Parser("1+2-3")
# exp = "sin(sqrt(sqrt(sqrt(sqrt(pi**2**3))))**2/2)"  => 1.0
# exp = "sin((2+5)-3**(5)-100*cos(3)-2)"
# exp = "-152.143134+3.2**(5.0)+(1.3-34)*2/2-1*2**5*245-1+2-3*4/5-(6)*7-(((232)))*((2**5)-5)**1.4"
# 不支持 a**-N
# exp = "2**(-1)"
# 

Parser(exp)
print(eval(exp))