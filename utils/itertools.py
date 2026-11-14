def combinations(xs, k):
    xs = list(xs)
    n = len(xs)
    if k < 0 or k > n:
        return
    if k == 0:
        yield []
        return
    for i in range(n - k + 1):
        for tail in combinations(xs[i + 1:], k - 1):
            yield [xs[i]] + tail

def chunks(xs, n):
    xs = list(xs)
    for i in range(0, len(xs), n):
        yield xs[i:i + n]