import string

DIGITS = '0123456789'
LETTERS = string.ascii_letters + "_"
LETTERS_DIGITS = LETTERS + DIGITS

TT_INT, TT_FLOAT, TT_STRING = 'INT', 'FLOAT', 'STRING'
TT_IDENTIFIER, TT_KEYWORD = 'IDENTIFIER', 'KEYWORD'
TT_PLUS, TT_MINUS, TT_MUL, TT_DIV = 'PLUS', 'MINUS', 'MUL', 'DIV'
TT_EQ, TT_PLUS_EQ, TT_MINUS_EQ, TT_MUL_EQ = 'EQ', 'PLUS_EQ', 'MINUS_EQ', 'MUL_EQ'
TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE = 'EE', 'NE', 'LT', 'GT', 'LTE', 'GTE'
TT_AND, TT_OR, TT_NOT = 'AND', 'OR', 'NOT'
TT_LPAREN, TT_RPAREN = 'LPAREN', 'RPAREN'
TT_LBRACE, TT_RBRACE = 'LBRACE', 'RBRACE'
TT_LBRACKET, TT_RBRACKET = 'LBRACKET', 'RBRACKET'
TT_COMMA, TT_DOT, TT_SEMICOLON = 'COMMA', 'DOT', 'SEMICOLON'
TT_NEWLINE, TT_EOF = 'NEWLINE', 'EOF'

class Token:
    def __init__(self, t, v=None):
        self.type = t
        self.value = v

    def __repr__(self):
        return f'{self.type}:{self.value}' if self.value is not None else f'{self.type}'

# keywords
KEYWORDS = [
    'var', 'array', 'stack', 'if', 'then', 
    'else', 'while', 'for', 'and', 'or', 
    'not', 'true', 'false'
]