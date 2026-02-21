from core.constants import *
from core.nodes import *

class Parser:
    def __init__(self, token_list):
        self.tokens = token_list
        self.cursor = -1
        self.advance()

    def advance(self):
        self.cursor += 1
        self.current_tok = self.tokens[self.cursor] if self.cursor < len(self.tokens) else None
        return self.current_tok

    def parse(self):
        return self.statements()

    def statements(self):
        nodes = []
        while self.current_tok and self.current_tok.type == TT_NEWLINE:
            self.advance()
        
        while True:
            stmt = self.expr()
            if not stmt: break
            nodes.append(stmt)
            
            while self.current_tok and self.current_tok.type == TT_NEWLINE:
                self.advance()
            
            # stop if we hit a closing brace or end of file
            if self.current_tok and self.current_tok.type in (TT_RBRACE, TT_EOF):
                break
                
        return ListNode(nodes)

    def atom(self):
        tok = self.current_tok
        if not tok: return None
        
        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(tok)
            
        if tok.type == TT_STRING:
            self.advance()
            return StringNode(tok)

        if tok.type == TT_KEYWORD and tok.value in ('true', 'false'):
            self.advance()
            bool_val = 1 if tok.value == 'true' else 0
            return NumberNode(Token(TT_INT, bool_val))
            
        if tok.type == TT_IDENTIFIER:
            self.advance()
            return VarAccessNode(tok)
            
        if tok.type == TT_LBRACKET:
            self.advance()
            items = []
            if self.current_tok and self.current_tok.type != TT_RBRACKET:
                items.append(self.expr())
                while self.current_tok and self.current_tok.type == TT_COMMA:
                    self.advance()
                    items.append(self.expr())
            if self.current_tok and self.current_tok.type == TT_RBRACKET:
                self.advance()
            return ArrayNode(items)
            
        if tok.type == TT_LPAREN:
            self.advance()
            inner_expr = self.expr()
            if self.current_tok and self.current_tok.type == TT_RPAREN:
                self.advance()
            return inner_expr
        return None

    def call(self):
        node = self.atom()
        while True:
            if not self.current_tok: break
            
            if self.current_tok.type == TT_LPAREN:
                self.advance()
                args_list = []
                if self.current_tok.type != TT_RPAREN:
                    args_list.append(self.expr())
                    while self.current_tok and self.current_tok.type == TT_COMMA:
                        self.advance()
                        args_list.append(self.expr())
                if self.current_tok and self.current_tok.type == TT_RPAREN:
                    self.advance()
                node = CallNode(node, args_list)
                
            elif self.current_tok.type == TT_LBRACKET:
                self.advance()
                idx_val = self.expr()
                if self.current_tok and self.current_tok.type == TT_RBRACKET:
                    self.advance()
                node = IndexNode(node, idx_val)
                
            elif self.current_tok.type == TT_DOT:
                self.advance()
                attr_name = self.current_tok
                self.advance()
                node = MemberAccessNode(node, attr_name)
            else:
                break
        return node

    def factor(self):
        tok = self.current_tok
        if tok and tok.type in (TT_PLUS, TT_MINUS, TT_NOT):
            self.advance()
            return UnaryOpNode(tok, self.factor())
        return self.call()

    def term(self): return self.bin_op(self.factor, (TT_MUL, TT_DIV))
    def arith_expr(self): return self.bin_op(self.term, (TT_PLUS, TT_MINUS))
    def comp_expr(self): return self.bin_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE))
    def and_expr(self): return self.bin_op(self.comp_expr, (TT_KEYWORD, 'and'))
    def or_expr(self): return self.bin_op(self.and_expr, (TT_KEYWORD, 'or'))

    def expr(self):
        if self.current_tok and self.current_tok.type == TT_KEYWORD and self.current_tok.value in ['var', 'array', 'stack']:
            v_type = self.current_tok
            self.advance()
            v_name = self.current_tok
            self.advance()
            if self.current_tok and self.current_tok.type == TT_EQ:
                self.advance()
                return VarAssignNode(v_type, v_name, self.expr())
        if self.current_tok and self.current_tok.type == TT_IDENTIFIER:
            if self.cursor + 1 < len(self.tokens):
                lookahead = self.tokens[self.cursor + 1]
                if lookahead.type in (TT_EQ, TT_PLUS_EQ, TT_MINUS_EQ):
                    var_name = self.current_tok
                    self.advance()
                    op_tok = self.current_tok
                    self.advance()
                    rhs = self.expr()
                    
                    if op_tok.type == TT_PLUS_EQ:
                        rhs = BinOpNode(VarAccessNode(var_name), Token(TT_PLUS), rhs)
                    elif op_tok.type == TT_MINUS_EQ:
                        rhs = BinOpNode(VarAccessNode(var_name), Token(TT_MINUS), rhs)
                    return VarAssignNode(Token(TT_KEYWORD, 'var'), var_name, rhs)
        if self.current_tok and self.current_tok.type == TT_KEYWORD:
            kw = self.current_tok.value
            if kw == 'if': return self.if_expr()
            if kw == 'while': return self.while_expr()
            if kw == 'for': return self.for_expr()
            
        return self.or_expr()

    def if_expr(self):
        self.advance()
        if self.current_tok.type == TT_LPAREN:
            self.advance()
            cond = self.expr()
            if self.current_tok.type == TT_RPAREN: self.advance()
        else:
            cond = self.expr()

        if self.current_tok and self.current_tok.type == TT_LBRACE:
            self.advance()
            body_block = self.statements()
            if self.current_tok and self.current_tok.type == TT_RBRACE: self.advance()
        else:
            body_block = self.expr()

        fallback = None
        if self.current_tok and self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'else':
            self.advance()
            if self.current_tok and self.current_tok.type == TT_LBRACE:
                self.advance()
                fallback = self.statements()
                if self.current_tok and self.current_tok.type == TT_RBRACE: self.advance()
            else:
                fallback = self.expr()
        
        return IfNode([(cond, body_block)], fallback)

    def while_expr(self):
        self.advance()
        if self.current_tok.type == TT_LPAREN:
            self.advance()
            cond = self.expr()
            if self.current_tok.type == TT_RPAREN: self.advance()
        else:
            cond = self.expr()

        if self.current_tok and self.current_tok.type == TT_LBRACE:
            self.advance()
            loop_body = self.statements()
            if self.current_tok and self.current_tok.type == TT_RBRACE: self.advance()
        else:
            loop_body = self.expr()
        return WhileNode(cond, loop_body)

    def for_expr(self):
        self.advance() 
        if self.current_tok.type == TT_LPAREN: self.advance()
        
        start_node = self.expr()
        if self.current_tok and self.current_tok.type == TT_SEMICOLON: self.advance()
        
        end_cond = self.expr()
        if self.current_tok and self.current_tok.type == TT_SEMICOLON: self.advance()
        
        step_node = self.expr()
        
        if self.current_tok and self.current_tok.type == TT_RPAREN: self.advance()

        if self.current_tok and self.current_tok.type == TT_LBRACE:
            self.advance()
            main_body = self.statements()
            if self.current_tok and self.current_tok.type == TT_RBRACE: self.advance()
        else:
            main_body = self.expr()
            
        return ForNode(start_node, end_cond, step_node, main_body)

    def bin_op(self, parse_func, operators):
        left_node = parse_func()
        while self.current_tok and (self.current_tok.type in operators or (self.current_tok.type, self.current_tok.value) in operators):
            operator = self.current_tok
            self.advance()
            right_node = parse_func()
            left_node = BinOpNode(left_node, operator, right_node)
        return left_node