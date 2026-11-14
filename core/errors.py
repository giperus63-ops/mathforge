class MathForgeError(Exception):
    pass

class DimensionError(MathForgeError):
    pass

class SingularMatrixError(MathForgeError):
    pass

class ParseError(MathForgeError):
    pass