from ..calculus.dual import Dual

class Polynomial:
    def __init__(self, coeffs):
        c = [float(x) for x in coeffs]
        while len(c) > 1 and abs(c[-1]) < 1e-15:
            c.pop()
        self._c = c
    @property
    def degree(self):
        return len(self._c) - 1
    @property
    def coeffs(self):
        return list(self._c)
    def __len__(self):
        return len(self._c)
    def __getitem__(self, i):
        return self._c[i] if i < len(self._c) else 0.0
    def __add__(self, other):
        n = max(len(self), len(other))
        return Polynomial([self[i] + other[i] for i in range(n)])
    def __sub__(self, other):
        n = max(len(self), len(other))
        return Polynomial([self[i] - other[i] for i in range(n)])
    def __mul__(self, other):
        if isinstance(other, Polynomial):
            res = [0.0] * (len(self) + len(other) - 1)
            for i, a in enumerate(self._c):
                for j, b in enumerate(other._c):
                    res[i + j] += a * b
            return Polynomial(res)
        return Polynomial([x * other for x in self._c])
    __rmul__ = __mul__
    def __truediv__(self, k):
        return Polynomial([x / k for x in self._c])
    def derivative(self):
        if self.degree == 0:
            return Polynomial([0.0])
        return Polynomial([self._c[i] * i for i in range(1, len(self._c))])
    def integrate(self, c=0.0):
        return Polynomial([c] + [self._c[i] / (i + 1) for i in range(len(self._c))])
    def evaluate(self, x):
        out = 0.0
        for a in reversed(self._c):
            out = out * x + a
        return out
    def evaluate_dual(self, x):
        d = Dual(x, 1.0)
        out = Dual(0.0, 0.0)
        for a in reversed(self._c):
            out = out * d + Dual(a, 0.0)
        return out
    def __call__(self, x):
        return self.evaluate(x)
    def __repr__(self):
        return f"Polynomial({self._c})"