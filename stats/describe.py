import math

def mean(xs):
    xs = list(xs)
    if not xs:
        raise ValueError("empty sequence")
    return sum(xs) / len(xs)

def variance(xs, sample=True):
    xs = list(xs)
    n = len(xs)
    if n < 2:
        raise ValueError("need at least 2 elements")
    m = mean(xs)
    s = sum((x - m) ** 2 for x in xs)
    return s / (n - 1 if sample else n)

def std(xs, sample=True):
    return math.sqrt(variance(xs, sample))

def median(xs):
    s = sorted(xs)
    n = len(s)
    if n == 0:
        raise ValueError("empty")
    if n % 2 == 1:
        return s[n // 2]
    return (s[n // 2 - 1] + s[n // 2]) / 2

def quantile(xs, q):
    if not 0.0 <= q <= 1.0:
        raise ValueError("q must be in [0,1]")
    s = sorted(xs)
    n = len(s)
    if n == 0:
        raise ValueError("empty")
    pos = (n - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return s[lo]
    return s[lo] + (pos - lo) * (s[hi] - s[lo])

def covariance(xs, ys, sample=True):
    xs = list(xs)
    ys = list(ys)
    if len(xs) != len(ys):
        raise ValueError("length mismatch")
    n = len(xs)
    if n < 2:
        raise ValueError("need at least 2")
    mx = mean(xs)
    my = mean(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (n - 1 if sample else n)