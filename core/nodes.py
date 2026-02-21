# Nodes code

class NumberNode:
    def __init__(self, token): self.token = token
    def __repr__(self): return f'{self.token}'

class StringNode:
    def __init__(self, token): self.token = token
    def __repr__(self): return f'{self.token}'

class VarAccessNode:
    def __init__(self, name_tok): self.name_tok = name_tok
    def __repr__(self): return f'{self.name_tok}'

class VarAssignNode:
    def __init__(self, v_type, v_name, value_expr):
        self.type_tok = v_type
        self.var_name_tok = v_name
        self.value_node = value_expr
    def __repr__(self): 
        return f'(set {self.type_tok} {self.var_name_tok} = {self.value_node})'
class BinOpNode:
    def __init__(self, left, op, right):
        self.left_node, self.op_tok, self.right_node = left, op, right
    def __repr__(self): return f'({self.left_node}, {self.op_tok}, {self.right_node})'
class UnaryOpNode:
    def __init__(self, op, operand):
        self.op_tok, self.node = op, operand
    def __repr__(self): return f'({self.op_tok}, {self.node})'

class IfNode:
    def __init__(self, branch_cases, fallback):
        self.cases, self.else_case = branch_cases, fallback
    def __repr__(self): return f'(if {self.cases} else {self.else_case})'

class WhileNode:
    def __init__(self, cond, body):
        self.condition_node, self.body_node = cond, body
    def __repr__(self): return f'(while {self.condition_node} do {self.body_node})'

class ForNode:
    def __init__(self, setup, cond, step, body):
        self.var_assign_node = setup
        self.condition_node = cond
        self.iterate_node = step
        self.body_node = body
    def __repr__(self):
        return f'(for {self.var_assign_node}; {self.condition_node}; {self.iterate_node} do {self.body_node})'

class CallNode:
    def __init__(self, target, params):
        self.node_to_call, self.args = target, params
    def __repr__(self): return f'{self.node_to_call}({self.args})'

class ListNode:
    def __init__(self, nodes):
        self.element_nodes = nodes
    def __repr__(self): return f'List{self.element_nodes}'
class ArrayNode:
    def __init__(self, items):
        self.elements = items
    def __repr__(self): return f'ArrayNode{self.elements}'
class IndexNode:
    def __init__(self, source, pos):
        self.left, self.index = source, pos
    def __repr__(self): return f'({self.left}[{self.index}])'
class MemberAccessNode:
    def __init__(self, obj, member):
        self.left = obj
        self.member_name = member
    def __repr__(self): return f'({self.left}.{self.member_name})'