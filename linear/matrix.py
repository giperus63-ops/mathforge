from .vector import Vector
from ..core.errors import DimensionError

class Matrix:
    def __init__(self, rows):
        if not rows:
            raise DimensionError("empty matrix")
        n = len(rows[0])
        for r in rows:
            if len(r) != n:
                raise DimensionError("ragged matrix")
        self._rows = [[float(x) for x in r] for r in rows]
    @property
    def shape(self):
        return (len(self._rows), len(self._rows[0]))
    def __getitem__(self, ij):
        i, j = ij
        return self._rows[i][j]
    def __setitem__(self, ij, v):
        i, j = ij
        self._rows[i][j] = float(v)
    def row(self, i):
        return Vector(self._rows[i])
    def col(self, j):
        return Vector([r[j] for r in self._rows])
    def __add__(self, other):
        self._check(other)
        return Matrix([[a + b for a, b in zip(ra, rb)] for ra, rb in zip(self._rows, other._rows)])
    def __sub__(self, other):
        self._check(other)
        return Matrix([[a - b for a, b in zip(ra, rb)] for ra, rb in zip(self._rows, other._rows)])
    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.matmul(other)
        return Matrix([[x * other for x in r] for r in self._rows])
    __rmul__ = __mul__
    def __matmul__(self, other):
        return self.matmul(other)
    def _check(self, other):
        if self.shape != other.shape:
            raise DimensionError(f"shape mismatch: {self.shape} vs {other.shape}")
    def matmul(self, other):
        r1, c1 = self.shape
        r2, c2 = other.shape
        if c1 != r2:
            raise DimensionError(f"matmul shape mismatch: {self.shape} @ {other.shape}")
        return Matrix([[sum(self._rows[i][k] * other._rows[k][j] for k in range(c1)) for j in range(c2)] for i in range(r1)])
    def transpose(self):
        r, c = self.shape
        return Matrix([[self._rows[i][j] for i in range(r)] for j in range(c)])
    T = property(transpose)
    def identity(n):
        return Matrix([[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)])
    def trace(self):
        r, c = self.shape
        if r != c:
            raise DimensionError("trace requires square matrix")
        return sum(self._rows[i][i] for i in range(r))
    def approx_equal(self, other, tol=1e-10):
        self._check(other)
        return all(abs(self._rows[i][j] - other._rows[i][j]) <= tol for i in range(self.shape[0]) for j in range(self.shape[1]))
    def __repr__(self):
        return f"Matrix({self._rows})"