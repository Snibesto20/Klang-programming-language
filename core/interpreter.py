import re
from core.constants import *
from core.values import Value, Array, Stack

class Interpreter:
    def visit(self, node, ctx):
        if node is None: return 0
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, ctx)

    def no_visit_method(self, node, ctx):
        print(f"No visit_{type(node).__name__} method defined")
        return 0

    def visit_ListNode(self, node, ctx):
        res = None
        for element in node.element_nodes:
            res = self.visit(element, ctx)
        return res

    def visit_NumberNode(self, node, ctx): 
        return node.token.value

    def visit_StringNode(self, node, ctx):
        raw_text = node.token.value
        def replace_var(match):
            v_name = match.group(1)
            val = ctx.get(v_name, f"{{{v_name}}}")
            return str(val)
        return re.sub(r'\{(\w+)\}', replace_var, raw_text)

    def visit_ArrayNode(self, node, ctx): 
        elements = [self.visit(el, ctx) for el in node.elements]
        return Array(elements)

    def visit_VarAccessNode(self, node, ctx): 
        return ctx.get(node.name_tok.value, 0)

    def visit_VarAssignNode(self, node, ctx):
        val = self.visit(node.value_node, ctx)
        var_type = getattr(node, 'type_tok', None)
        var_type_val = var_type.value if var_type else 'var'
        
        if var_type_val == 'array':
            final_val = val if isinstance(val, Array) else Array(val if isinstance(val, list) else [val])
        elif var_type_val == 'stack':
            final_val = val if isinstance(val, Stack) else Stack(val if isinstance(val, list) else [val])
        else:
            final_val = val
            
        # Updated to match Node.var_name_tok
        ctx[node.var_name_tok.value] = final_val
        return final_val

    def visit_IndexNode(self, node, ctx):
        left = self.visit(node.left, ctx)
        index = self.visit(node.index, ctx)
        if hasattr(left, 'value') and isinstance(left.value, list):
            try:
                return left.value[int(index)]
            except:
                return 0
        return 0

    def visit_BinOpNode(self, node, ctx):
        l = self.visit(node.left_node, ctx)
        r = self.visit(node.right_node, ctx)
        op = node.op_tok.type
        
        if op == TT_PLUS: return l + r
        if op == TT_MINUS: return l - r
        if op == TT_MUL: return l * r
        if op == TT_DIV: return l / r if r != 0 else 0
        if op == TT_EE: return int(l == r)
        if op == TT_NE: return int(l != r)
        if op == TT_LT: return int(l < r)
        if op == TT_GT: return int(l > r)
        if op == TT_LTE: return int(l <= r)
        if op == TT_GTE: return int(l >= r)
        if op == TT_AND: return int(bool(l) and bool(r))
        if op == TT_OR: return int(bool(l) or bool(r))
        return 0

    def visit_UnaryOpNode(self, node, ctx):
        val = self.visit(node.node, ctx)
        if node.op_tok.type == TT_MINUS: val = -val
        if node.op_tok.type == TT_NOT: val = int(not val)
        return val

    def visit_IfNode(self, node, ctx):
        for cond, expr in node.cases:
            if self.visit(cond, ctx) != 0: 
                return self.visit(expr, ctx)
        if node.else_case: 
            return self.visit(node.else_case, ctx)
        return None

    def visit_WhileNode(self, node, ctx):
        res = None
        while self.visit(node.condition_node, ctx) != 0: 
            res = self.visit(node.body_node, ctx)
        return res

    def visit_ForNode(self, node, ctx):
        self.visit(node.var_assign_node, ctx)
        res = None
        while self.visit(node.condition_node, ctx) != 0:
            res = self.visit(node.body_node, ctx)
            self.visit(node.iterate_node, ctx)
        return res

    def visit_MemberAccessNode(self, node, ctx):
        obj = self.visit(node.left, ctx)
        return (obj, node.member_name.value)

    def visit_CallNode(self, node, ctx):
        args = [self.visit(arg, ctx) for arg in node.args]
        call_target = self.visit(node.node_to_call, ctx)
        
        if isinstance(call_target, tuple):
            obj, method_name = call_target
            if hasattr(obj, 'methods') and method_name in obj.methods:
                return obj.methods[method_name](args)
            return None

        if hasattr(node.node_to_call, 'name_tok'):
            fn_name = node.node_to_call.name_tok.value
            
            if fn_name == "print":
                print(*(str(a) for a in args))
                return None
            
            if fn_name == "input":
                prompt = str(args[0]) if len(args) > 0 else ""
                text = input(prompt)
                try:
                    if "." in text: return float(text)
                    return int(text)
                except ValueError:
                    return text
                    
        return None