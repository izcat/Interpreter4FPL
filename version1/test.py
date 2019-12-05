from enum import Enum

class TokenType(Enum):
    ORIGIN = "ORIGIN"
    SCALE = "SCALE"
    ROT = "ROT"
    IS = "IS"
    TO = "TO"
    STEP = "STEP"
    DRAW = "DRAW"
    FOR = "FOR"
    FROM = "FROM"
    T = "T"
    SEMICO = ';'
    L_BRACKET = '('
    R_BRACKET = ')'
    COMMA = ','
    PLUS = '+'
    MINUS = '-'
    MUL = '*'
    DIV = '/'
    POWER = '**'
    FUNC = "FUNCTION"
    CONST_ID = "CONST_ID"
    NONTOKEN = 22
    ERRTOKEN = 23

print(TokenType)