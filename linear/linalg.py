import math
from .matrix import Matrix
from .vector import Vector
from ..core.errors import DimensionError, SingularMatrixError
from ..core.scalar import EPS

def det(m):
    n, c = m.shape
    if n != c:
        raise DimensionError("det requires square matrix")
    a = [[m[i, j] for j in range(n)] for i in range(n)]
    sign = 1.0
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(a[r][col]))
        if abs(a[pivot][col]) < EPS:
            return 0.0
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            sign = -sign
        for r in range(col + 1, n):
            f = a[r][col] / a[col][col]
            for k in range(col, n):
                a[r][k] -= f * a[col][k]
    d = sign
    for i in range(n):
        d *= a[i][i]
    return d

def lu(m):
    n, c = m.shape
    if n != c:
        raise DimensionError("lu requires square matrix")
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]
    for i in range(n):
        L[i][i] = 1.0
        for j in range(i, n):
            s = m[i, j] - sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = s
        if abs(U[i][i]) < EPS:
            raise SingularMatrixError("zero pivot in LU")
        for j in range(i + 1, n):
            s = m[j, i] - sum(L[j][k] * U[k][i] for k in range(i))
            L[j][i] = s / U[i][i]
    return Matrix(L), Matrix(U)

def inverse(m):
    n, c = m.shape
    if n != c:
        raise DimensionError("inverse requires square matrix")
    aug = [[m[i, j] for j in range(n)] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < EPS:
            raise SingularMatrixError("singular matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        pv = aug[col][col]
        aug[col] = [x / pv for x in aug[col]]
        for r in range(n):
            if r != col and abs(aug[r][col]) > 0:
                f = aug[r][col]
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[col])]
    return Matrix([row[n:] for row in aug])

def solve(a, b):
    n, c = a.shape
    if n != c:
        raise DimensionError("solve requires square matrix")
    inv = inverse(a)
    return Vector([sum(inv[i, j] * b[j] for j in range(n)) for i in range(n)])

def qr(m):
    r, c = m.shape
    cols = [[m[i, j] for i in range(r)] for j in range(c)]
    q_cols = []
    rmat = [[0.0] * c for _ in range(c)]
    for j in range(c):
        v = cols[j][:]
        for k in range(len(q_cols)):
            rmat[k][j] = sum(q_cols[k][i] * v[i] for i in range(r))
            v = [v[i] - rmat[k][j] * q_cols[k][i] for i in range(r)]
        norm = math.sqrt(sum(x * x for x in v))
        if norm < EPS:
            raise SingularMatrixError("linearly dependent columns")
        rmat[j][j] = norm
        q_cols.append([x / norm for x in v])
    Q = Matrix([[q_cols[j][i] for j in range(c)] for i in range(r)])
    return Q, Matrix(rmat)

def power_iteration(m, iters=200, tol=1e-12):
    n, c = m.shape
    if n != c:
        raise DimensionError("requires square matrix")
    v = [1.0] * n
    lam = 0.0
    for _ in range(iters):
        w = [sum(m[i, j] * v[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x * x for x in w))
        v = [x / norm for x in w]
        new_lam = sum(v[i] * sum(m[i, j] * v[j] for j in range(n)) for i in range(n))
        if abs(new_lam - lam) < tol:
            lam = new_lam
            break
        lam = new_lam
    return lam, Vector(v)