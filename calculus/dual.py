import math

class Dual:
    def __init__(self, re, du=0.0):
        self.re = float(re)
        self.du = float(du)
    def __add__(self, o):
        o = _wrap(o)
        return Dual(self.re + o.re, self.du + o.du)
    __radd__ = __add__
    def __sub__(self, o):
        o = _wrap(o)
        return Dual(self.re - o.re, self.du - o.du)
    def __rsub__(self, o):
        o = _wrap(o)
        return o - self
    def __mul__(self, o):
        o = _wrap(o)
        return Dual(self.re * o.re, self.du * o.re + self.re * o.du)
    __rmul__ = __mul__
    def __truediv__(self, o):
        o = _wrap(o)
        return Dual(self.re / o.re, (self.du * o.re - self.re * o.du) / (o.re * o.re))
    def __rtruediv__(self, o):
        return _wrap(o) / self
    def __pow__(self, o):
        o = _wrap(o)
        if o.du != 0.0:
            base = self.re
            return Dual(base ** o.re, base ** o.re * (o.du * math.log(abs(base)) + o.re * self.du / base))
        n = o.re
        return Dual(self.re ** n, n * self.re ** (n - 1) * self.du)
    def __neg__(self):
        return Dual(-self.re, -self.du)
    def __repr__(self):
        return f"Dual({self.re}, {self.du})"

def _wrap(x):
    return x if isinstance(x, Dual) else Dual(x, 0.0)

def sin(x):
    x = _wrap(x)
    return Dual(math.sin(x.re), math.cos(x.re) * x.du)

def cos(x):
    x = _wrap(x)
    return Dual(math.cos(x.re), -math.sin(x.re) * x.du)

def tan(x):
    x = _wrap(x)
    c = math.cos(x.re)
    return Dual(math.tan(x.re), x.du / (c * c))

def exp(x):
    x = _wrap(x)
    v = math.exp(x.re)
    return Dual(v, v * x.du)

def log(x):
    x = _wrap(x)
    return Dual(math.log(x.re), x.du / x.re)

def sqrt(x):
    x = _wrap(x)
    v = math.sqrt(x.re)
    return Dual(v, x.du / (2 * v))