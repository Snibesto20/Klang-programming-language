from core.lexer import Lexer
from core.parser import Parser
from core.interpreter import Interpreter

symbol_table = {}

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()
    if error: return None, error
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    interpreter = Interpreter()
    return interpreter.visit(ast, symbol_table), None