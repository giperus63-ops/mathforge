import math
from .node import Num, Var, BinOp, UnaryOp, Func

_FUNCS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "exp": math.exp, "log": math.log, "sqrt": math.sqrt,
    "abs": abs,
}

def evaluate(node, env=None):
    env = env or {}
    if isinstance(node, Num):
        return node.value
    if isinstance(node, Var):
        if node.name not in env:
            raise KeyError(f"undefined variable {node.name}")
        return env[node.name]
    if isinstance(node, UnaryOp):
        v = evaluate(node.operand, env)
        return -v if node.op == "-" else v
    if isinstance(node, BinOp):
        a = evaluate(node.left, env)
        b = evaluate(node.right, env)
        if node.op == "+":
            return a + b
        if node.op == "-":
            return a - b
        if node.op == "*":
            return a * b
        if node.op == "/":
            return a / b
        if node.op == "^":
            return a ** b
    if isinstance(node, Func):
        if node.name not in _FUNCS:
            raise KeyError(f"unknown function {node.name}")
        return _FUNCS[node.name](evaluate(node.arg, env))
    raise TypeError(f"unknown node {node}")