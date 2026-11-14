from .node import Num, Var, BinOp, UnaryOp, Func

def simplify(node):
    if isinstance(node, (Num, Var)):
        return node
    if isinstance(node, UnaryOp):
        v = simplify(node.operand)
        if isinstance(v, Num):
            return Num(-v.value)
        return UnaryOp("-", v)
    if isinstance(node, BinOp):
        l = simplify(node.left)
        r = simplify(node.right)
        if isinstance(l, Num) and isinstance(r, Num):
            if node.op == "+":
                return Num(l.value + r.value)
            if node.op == "-":
                return Num(l.value - r.value)
            if node.op == "*":
                return Num(l.value * r.value)
            if node.op == "/":
                return Num(l.value / r.value)
            if node.op == "^":
                return Num(l.value ** r.value)
        if node.op == "+" and isinstance(r, Num) and r.value == 0:
            return l
        if node.op == "+" and isinstance(l, Num) and l.value == 0:
            return r
        if node.op == "-" and isinstance(r, Num) and r.value == 0:
            return l
        if node.op == "*" and isinstance(r, Num) and r.value == 1:
            return l
        if node.op == "*" and isinstance(l, Num) and l.value == 1:
            return r
        if node.op == "*" and isinstance(r, Num) and r.value == 0:
            return Num(0.0)
        if node.op == "*" and isinstance(l, Num) and l.value == 0:
            return Num(0.0)
        if node.op == "^" and isinstance(r, Num) and r.value == 1:
            return l
        if node.op == "^" and isinstance(r, Num) and r.value == 0:
            return Num(1.0)
        return BinOp(node.op, l, r)
    if isinstance(node, Func):
        return Func(node.name, simplify(node.arg))
    return node