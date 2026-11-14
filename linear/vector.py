import math
from ..core.errors import DimensionError
from ..core.scalar import EPS, is_close

class Vector:
    def __init__(self, data):
        self._data = [float(x) for x in data]
    @property
    def data(self):
        return list(self._data)
    def __len__(self):
        return len(self._data)
    def __getitem__(self, i):
        return self._data[i]
    def __setitem__(self, i, v):
        self._data[i] = float(v)
    def __add__(self, other):
        self._check(other)
        return Vector([a + b for a, b in zip(self._data, other._data)])
    def __sub__(self, other):
        self._check(other)
        return Vector([a - b for a, b in zip(self._data, other._data)])
    def __mul__(self, k):
        return Vector([a * k for a in self._data])
    __rmul__ = __mul__
    def __truediv__(self, k):
        return Vector([a / k for a in self._data])
    def __neg__(self):
        return Vector([-a for a in self._data])
    def _check(self, other):
        if len(self) != len(other):
            raise DimensionError(f"vector length mismatch: {len(self)} vs {len(other)}")
    def dot(self, other):
        self._check(other)
        return sum(a * b for a, b in zip(self._data, other._data))
    def norm(self):
        return math.sqrt(self.dot(self))
    def normalize(self):
        n = self.norm()
        return Vector([x / n for x in self._data])
    def cross(self, other):
        if len(self) != 3 or len(other) != 3:
            raise DimensionError("cross product requires 3D vectors")
        a = self._data
        b = other._data
        return Vector([a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]])
    def approx_equal(self, other, tol=EPS):
        self._check(other)
        return all(is_close(a, b, tol) for a, b in zip(self._data, other._data))
    def __repr__(self):
        return f"Vector({self._data})"