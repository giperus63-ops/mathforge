from ..core.errors import ParseError
from .node import Num, Var, BinOp, UnaryOp, Func

def tokenize(s):
    tokens = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c.isspace():
            i += 1
            continue
        if c.isdigit() or c == '.':
            j = i
            while j < n and (s[j].isdigit() or s[j] == '.'):
                j += 1
            tokens.append(("NUM", float(s[i:j])))
            i = j
            continue
        if c.isalpha() or c == '_':
            j = i
            while j < n and (s[j].isalnum() or s[j] == '_'):
                j += 1
            tokens.append(("ID", s[i:j]))
            i = j
            continue
        if c in "+-*/^(),":
            tokens.append((c, c))
            i += 1
            continue
        raise ParseError(f"unexpected char {c!r}")
    tokens.append(("EOF", None))
    return tokens

class _P:
    def __init__(self, tokens):
        self.toks = tokens
        self.pos = 0
    def peek(self):
        return self.toks[self.pos]
    def next(self):
        t = self.toks[self.pos]
        self.pos += 1
        return t
    def expect(self, kind):
        t = self.next()
        if t[0] != kind:
            raise ParseError(f"expected {kind}, got {t}")
        return t
    def parse_expr(self):
        node = self.parse_term()
        while self.peek()[0] in ("+", "-"):
            op = self.next()[0]
            node = BinOp(op, node, self.parse_term())
        return node
    def parse_term(self):
        node = self.parse_power()
        while self.peek()[0] in ("*", "/"):
            op = self.next()[0]
            node = BinOp(op, node, self.parse_power())
        return node
    def parse_power(self):
        node = self.parse_unary()
        if self.peek()[0] == "^":
            self.next()
            node = BinOp("^", node, self.parse_power())
        return node
    def parse_unary(self):
        if self.peek()[0] == "-":
            self.next()
            return UnaryOp("-", self.parse_unary())
        return self.parse_atom()
    def parse_atom(self):
        t = self.peek()
        if t[0] == "NUM":
            self.next()
            return Num(t[1])
        if t[0] == "ID":
            name = t[1]
            self.next()
            if self.peek()[0] == "(":
                self.next()
                arg = self.parse_expr()
                self.expect(")")
                return Func(name, arg)
            return Var(name)
        if t[0] == "(":
            self.next()
            node = self.parse_expr()
            self.expect(")")
            return node
        raise ParseError(f"unexpected token {t}")

def parse(s):
    p = _P(tokenize(s))
    node = p.parse_expr()
    p.expect("EOF")
    return node