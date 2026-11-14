from ..core.scalar import is_close

def approx_equal(a, b, tol=1e-10):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            return False
        return all(approx_equal(x, y, tol) for x, y in zip(a, b))
    return is_close(a, b, tol)