# Lexer codeZ

from core.constants import *

class Lexer:
    def __init__(self, input_text):
        self.text = input_text
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        toks = []
        while self.current_char is not None:
            char = self.current_char
            
            if char in ' \t': self.advance()
            elif char == '\n':
                toks.append(Token(TT_NEWLINE))
                self.advance()
            elif char == ';':
                toks.append(Token(TT_SEMICOLON))
                self.advance()
            elif char == '/':
                out = self.make_slash_or_comment()
                if out: toks.append(out)
            elif char == '"':
                toks.append(self.make_string())
            elif char in DIGITS:
                toks.append(self.make_number())
            elif char in LETTERS: toks.append(self.make_identifier())
            elif char == '+': toks.append(self.make_plus())
            elif char == '-': toks.append(self.make_minus())
            elif char == '*': toks.append(self.make_mul())
            elif char == '.':
                toks.append(Token(TT_DOT))
                self.advance()
            elif char == '(':
                toks.append(Token(TT_LPAREN))
                self.advance()
            elif char == ')':
                toks.append(Token(TT_RPAREN))
                self.advance()
            elif char == '{':
                toks.append(Token(TT_LBRACE))
                self.advance()
            elif char == '}':
                toks.append(Token(TT_RBRACE))
                self.advance()
            elif char == '[':
                toks.append(Token(TT_LBRACKET))
                self.advance()
            elif char == ']':
                toks.append(Token(TT_RBRACKET))
                self.advance()
            elif char == ',':
                toks.append(Token(TT_COMMA))
                self.advance()
            elif char == '=':
                toks.append(self.make_equals())
            elif char == '!':
                toks.append(self.make_not())
            elif char == '&':
                toks.append(self.make_and())
            elif char == '|':
                toks.append(self.make_or())
            elif char == '<':
                toks.append(self.make_less_than())
            elif char == '>':
                toks.append(self.make_greater_than())
            else:
                bad_char = self.current_char
                self.advance()
                return [], f"Illegal char: {bad_char}"
        
        toks.append(Token(TT_EOF))
        return toks, None

    def make_slash_or_comment(self):
        self.advance()
        if self.current_char == '/':
            while self.current_char and self.current_char != '\n':
                self.advance()
            return None
        return Token(TT_DIV)

    def make_plus(self):
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(TT_PLUS_EQ)
        return Token(TT_PLUS)

    def make_minus(self):
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(TT_MINUS_EQ)
        return Token(TT_MINUS)

    def make_mul(self):
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(TT_MUL_EQ)
        return Token(TT_MUL)

    def make_equals(self):
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(TT_EE)
        return Token(TT_EQ)

    def make_not(self):
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(TT_NE)
        return Token(TT_NOT)

    def make_and(self):
        self.advance()
        if self.current_char == '&':
            self.advance()
            return Token(TT_AND)
        return Token(TT_KEYWORD, 'and')

    def make_or(self):
        self.advance()
        if self.current_char == '|':
            self.advance()
            return Token(TT_OR)
        return Token(TT_KEYWORD, 'or')

    def make_string(self):
        content = ''
        self.advance()
        while self.current_char and self.current_char != '"':
            content += self.current_char
            self.advance()
        self.advance()
        return Token(TT_STRING, content)

    def make_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char and self.current_char in DIGITS + '.':
            if self.current_char == '.': dot_count += 1
            num_str += self.current_char
            self.advance()
        
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        return Token(TT_FLOAT, float(num_str))

    def make_identifier(self):
        id_str = ''
        while self.current_char and self.current_char in LETTERS + DIGITS + '_':
            id_str += self.current_char
            self.advance()
        
        type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(type, id_str)

    def make_less_than(self):
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(TT_LTE)
        return Token(TT_LT)

    def make_greater_than(self):
        self.advance()
        if self.current_char == '=':
            self.advance()
            return Token(TT_GTE)
        return Token(TT_GT)