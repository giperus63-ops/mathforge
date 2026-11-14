from dataclasses import dataclass

@dataclass(frozen=True)
class Num:
    value: float

@dataclass(frozen=True)
class Var:
    name: str

@dataclass(frozen=True)
class BinOp:
    op: str
    left: object
    right: object

@dataclass(frozen=True)
class UnaryOp:
    op: str
    operand: object

@dataclass(frozen=True)
class Func:
    name: str
    arg: object