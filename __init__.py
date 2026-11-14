from .core.scalar import EPS, PI, E
from .linear.vector import Vector
from .linear.matrix import Matrix
from .poly.polynomial import Polynomial
from .calculus.dual import Dual
from .expr.parser import parse
from .expr.eval import evaluate
__all__ = ["EPS", "PI", "E", "Vector", "Matrix", "Polynomial", "Dual", "parse", "evaluate"]
