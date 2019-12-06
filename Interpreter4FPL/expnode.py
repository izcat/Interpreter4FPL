#-*- coding:utf-8 -*-
# @Time     : 2019/12/6 12:50
# @Author   : izcat
# @Site     : $ cnblogs.com/izcat
# @File     : expnode.py
# @Software : PyCharm
# @Desc     : 表达式节点定义

from mylexer import Token
from mylexer import TokenType

class ExpNode:
	T_value = 0.0

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
				return ExpNode.T_value
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
		ret = '  '*depth + self.token.lexeme + '\n'
		if self.lson!=None:
			ret += self.lson.dfs(depth+1)
		if self.rson!=None:
			ret += self.rson.dfs(depth+1)

		return ret
		# print("Depth %d" % depth)
		# self.token.show()