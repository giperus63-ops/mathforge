import cmath
import random
from .polynomial import Polynomial

def durand_kerner(poly, iters=500, tol=1e-12):
    n = poly.degree
    if n < 1:
        return []
    c = poly.coeffs
    lead = c[-1]
    coeffs = [x / lead for x in c]
    roots = [complex(0.4 + 0.9 * random.random(), 0.4 + 0.9 * random.random()) ** i for i in range(n)]
    for _ in range(iters):
        max_delta = 0.0
        new_roots = []
        for i in range(n):
            num = _eval(coeffs, roots[i])
            den = 1.0
            for j in range(n):
                if i != j:
                    den *= (roots[i] - roots[j])
            delta = num / den
            new_roots.append(roots[i] - delta)
            max_delta = max(max_delta, abs(delta))
        roots = new_roots
        if max_delta < tol:
            break
    return roots

def _eval(coeffs, z):
    out = 0j
    for a in reversed(coeffs):
        out = out * z + a
    return out

def newton_roots(poly, x0, iters=100, tol=1e-12):
    dpoly = poly.derivative()
    x = x0
    for _ in range(iters):
        fx = poly(x)
        if abs(fx) < tol:
            break
        dfx = dpoly(x)
        if abs(dfx) < 1e-15:
            break
        x = x - fx / dfx
    return x