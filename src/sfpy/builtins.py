from functools import wraps, reduce
from typing import Callable
from .functions import function
from .values import Int, Value


def arithmetic(func: Callable):
    @wraps(func)
    def wrapper(*args: Value):
        assert all(isinstance(v, Int)
                   for v in args), "All operands must be integer."
        return func(*[v.raw for v in args])

    return wrapper


@function()
@arithmetic
def add(*args: int):
    assert len(args) >= 2, "The length of operands must be larger than 2."
    return sum(args)


@function(count=2)
@arithmetic
def subtract(*args: int):
    return args[0] - args[1]


@function()
@arithmetic
def multiply(*args: int):
    assert len(args) >= 2, "The length of operands must be larger than 2."
    return reduce(lambda x, y: x * y, args)


@function(count=2)
@arithmetic
def divide(*args: int):
    assert len(args) == 2, "The length of operands must be 2."
    assert args[1] != 0, "The divisor cannot be zero."
    return args[0] // args[1]


@function(count=2)
@arithmetic
def power(*args: int):
    assert len(args) == 2, "The length of operands must be 2."
    return int(args[0] ** args[1])


builtinSymbols = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
    "^": power,
}
