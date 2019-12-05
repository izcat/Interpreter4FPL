# Program -> {Statement SEMICO}
# Statement -> OriginStatement | ScaleStatement | RotStatement | ForStatement
# OriginStatement -> ORIGIN IS L_BRACKET Expression COMMA Expression R_BRACKET
# ScaleStatement -> SCALE IS L_BRACKET Expression COMMA Expression R_BRACKET
# RotStatement -> ROT IS Expression
# ForStatement -> FOR T FROM Expression TO Expression STEP Expression
# 				DRAW L_BRACKET Expression COMMA Expression R_BRACKET

from lexer import *
import sys

tokenIter = None
tokenNow = Token(TokenType.NONTOKEN, '');

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
	Program()

def OriginStatement():
	MatchToken(TokenType.ORIGIN)
	MatchToken(TokenType.IS)
	MatchToken(TokenType.L_BRACKET)
	Origin_x = Expression().getValue()
	MatchToken(TokenType.COMMA)
	Origin_y = Expression().getValue()
	MatchToken(TokenType.R_BRACKET)

def	ScaleStatement():
	MatchToken(TokenType.SCALE)
	MatchToken(TokenType.IS)
	MatchToken(TokenType.L_BRACKET)
	Scale_x = Expression().getValue()
	MatchToken(TokenType.COMMA)
	Scale_y = Expression().getValue()
	MatchToken(TokenType.R_BRACKET)

def	RotStatement():
	MatchToken(TokenType.ROT)
	MatchToken(TokenType.IS)
	Rot_angle = Expression().getValue()

def	ForStatement():
	MatchToken(TokenType.FOR)
	MatchToken(TokenType.T)
	MatchToken(TokenType.FROM)
	T_start = Expression()
	MatchToken(TokenType.TO)
	T_end = Expression()
	MatchToken(TokenType.STEP)
	T_step = Expression()

	MatchToken(TokenType.DRAW)
	MatchToken(TokenType.L_BRACKET)
	Point_x = Expression()
	MatchToken(TokenType.COMMA)
	Point_y = Expression()
	MatchToken(TokenType.R_BRACKET)


# Statement -> OriginStatement | ScaleStatement | RotStatement | ForStatement
def Statement():
	if tokenNow.tokenType==TokenType.ORIGIN:
		OriginStatement()
	elif tokenNow.tokenType==TokenType.SCALE:
		ScaleStatement()
	elif tokenNow.tokenType==TokenType.ROT:
		RotStatement()
	elif tokenNow.tokenType==TokenType.FOR:
		ForStatement()
	else:
		print("error!")


def Program():
	while tokenNow.tokenType!=TokenType.NONTOKEN:
		Statement()
		matched = MatchToken(TokenType.SEMICO)
		if not matched:
			break


def test():
	Parser("--hello fad\n  //fadfjl\n ROT is (  1, 0*2) \n ROT is (sin(t), cos(tt));")

test()
