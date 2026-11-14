import math

EPS = 1e-10
PI = math.pi
E = math.e

def is_close(a, b, tol = EPS):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))

def clamp(x, lo, hi):
    return max(lo, min(hi, x))