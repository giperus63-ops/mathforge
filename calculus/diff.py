from .dual import Dual
from ..core.scalar import EPS

def derivative(f, x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)

def derivative_dual(f, x):
    return f(Dual(x, 1.0)).du

def gradient(f, point, h=1e-6):
    n = len(point)
    p = list(point)
    out = [0.0] * n
    for i in range(n):
        pi = p[:]
        mi = p[:]
        pi[i] += h
        mi[i] -= h
        out[i] = (f(*pi) - f(*mi)) / (2 * h)
    return out

def hessian(f, point, h=1e-4):
    n = len(point)
    p = list(point)
    H = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                pp = p[:]
                pm = p[:]
                pp[i] += h
                pm[i] -= h
                H[i][j] = (f(*pp) - 2 * f(*p) + f(*pm)) / (h * h)
            else:
                pp = p[:]
                pm = p[:]
                mp = p[:]
                mm = p[:]
                pp[i] += h
                pp[j] += h
                pm[i] += h
                pm[j] -= h
                mp[i] -= h
                mp[j] += h
                mm[i] -= h
                mm[j] -= h
                H[i][j] = (f(*pp) - f(*pm) - f(*mp) + f(*mm)) / (4 * h * h)
    return H

def newton(f, df, x0, iters=50, tol=EPS):
    x = x0
    for _ in range(iters):
        fx = f(x)
        if abs(fx) < tol:
            break
        x = x - fx / df(x)
    return x