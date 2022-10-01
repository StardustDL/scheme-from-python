from functools import wraps, reduce
from typing import Callable
from .functions import Function, function
from .values import Int, Value


class BuiltinSymbols(dict):
    def name(self, name: str):
        def decorator(func: Function):
            self[name] = func
            return func
        return decorator


builtins = BuiltinSymbols()


@builtins.name("+")
@function
def add(v1: int, v2: int, *args: int):
    return sum([v1, v2, *args])


@builtins.name("-")
@function
def subtract(v1: int, v2: int):
    return v1 - v2


@builtins.name("*")
@function
def multiply(v1: int, v2: int, *args: int):
    return reduce(lambda x, y: x * y, [v1, v2, *args])


@builtins.name("/")
@function
def divide(v1: int, v2: int):
    assert v2 != 0, "The divisor cannot be zero."
    return v1 // v2


@builtins.name("^")
@function
def power(v1: int, v2: int):
    return v1 ** v2


@builtins.name("<")
@function
def less(v1: int, v2: int):
    return v1 < v2


@builtins.name("<=")
@function
def lessEq(v1: int, v2: int):
    return v1 <= v2


@builtins.name(">")
@function
def greater(v1: int, v2: int):
    return v1 > v2


@builtins.name(">=")
@function
def greaterEq(v1: int, v2: int):
    return v1 >= v2


@builtins.name("=")
@function
def equal(v1: Value, v2: Value):
    return v1 == v2


@builtins.name("!=")
@function
def notEq(v1: Value, v2: Value):
    return v1 != v2


@builtins.name("not")
@function
def boolNot(b: bool):
    return not b


@builtins.name("and")
@function
def boolAnd(b1: bool, b2: bool, *args: bool):
    return all([b1, b2, *args])


@builtins.name("or")
@function
def boolOr(b1: bool, b2: bool, *args: bool):
    return any([b1, b2, *args])
