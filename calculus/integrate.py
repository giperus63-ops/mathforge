import random
from ..core.scalar import EPS

def simpson(f, a, b, n=1000):
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n, 2):
        s += 4 * f(a + i * h)
    for i in range(2, n, 2):
        s += 2 * f(a + i * h)
    return s * h / 3

def gauss_legendre(f, a, b, n=5):
    nodes, weights = _gauss_nodes(n)
    c = (b - a) / 2
    d = (b + a) / 2
    return c * sum(w * f(c * x + d) for x, w in zip(nodes, weights))

def _gauss_nodes(n):
    table = {
        1: ([(0.0)], [2.0]),
        2: ([-0.5773502691896257, 0.5773502691896257], [1.0, 1.0]),
        3: ([-0.7745966692414834, 0.0, 0.7745966692414834], [0.5555555555555556, 0.8888888888888888, 0.5555555555555556]),
        4: ([-0.8611363115940526, -0.3399810435848563, 0.3399810435848563, 0.8611363115940526],
            [0.3478548451374538, 0.6521451548625461, 0.6521451548625461, 0.3478548451374538]),
        5: ([-0.9061798459386640, -0.5384693101056831, 0.0, 0.5384693101056831, 0.9061798459386640],
            [0.2369268850561891, 0.4786286704993665, 0.5688888888888889, 0.4786286704993665, 0.2369268850561891]),
    }
    if n not in table:
        raise ValueError(f"unsupported n={n}")
    return table[n]

def monte_carlo(f, a, b, n=100000):
    total = 0.0
    for _ in range(n):
        x = a + (b - a) * random.random()
        total += f(x)
    return (b - a) * total / n