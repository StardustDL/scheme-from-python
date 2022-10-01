from functools import wraps, reduce
from typing import Callable

from .evaluators import Evaluator
from .programs import Program
from .functions import Function, function
from .values import Int, Value, Symbol
from .tokens import LEFT

builtins = {}


def builtin(name: str):
    def decorator(func: Function | Callable):
        if not isinstance(func, Function):
            func = function(func)
        builtins[name] = func
        return func
    return decorator


@builtin("def")
@builtin("define")
def define(name: Program, value: Program, *, eval: Evaluator):
    assert len(name) == 1, "The symbol name must be a single string."

    symbol = Symbol(name[0])
    assert symbol.valid(), "The symbol name is not valid."

    eval.symbol(symbol, eval.evaluate(value))

    return symbol


@builtin("if")
def branch(predicate: Program, exprTrue: Program, exprFalse: Program, *, eval: Evaluator):
    return eval.evaluate(exprTrue if eval.evaluate(predicate) else exprFalse)


@builtin("lam")
@builtin("lambda")
def lambdafunc(parameters: Program, body: Program, *, eval: Evaluator):
    assert len(parameters) > 0 and parameters.valid(
    ) and parameters[0] == LEFT, f"Parameter list {parameters} is invalid."

    parameters = parameters.split()
    assert all(
        len(p) == 1 for p in parameters), f"Parameter list {parameters} is invalid."
    assert len(set(p[0] for p in parameters)) == len(
        parameters), "Parameter names contain conflicts."

    parameters: list[Symbol] = [Symbol(p[0]) for p in parameters]
    assert all(s.valid()
               for s in parameters), f"Parameter list {parameters} is invalid."

    @function
    def raw(*args):
        return eval.sub({str(parameter): argument for parameter, argument in zip(parameters, args)}).evaluate(body)

    raw.repr = f"( lambda ( {' '.join(p.raw for p in parameters)} ) {' '.join(body)} )"
    raw.signature.parameters = [None] * len(parameters)

    return raw


@builtin("+")
def add(v1: int, v2: int, *args: int):
    return sum([v1, v2, *args])


@builtin("-")
def subtract(v1: int, v2: int):
    return v1 - v2


@builtin("*")
def multiply(v1: int, v2: int, *args: int):
    return reduce(lambda x, y: x * y, [v1, v2, *args])


@builtin("/")
def divide(v1: int, v2: int):
    assert v2 != 0, "The divisor cannot be zero."
    return v1 // v2


@builtin("^")
def power(v1: int, v2: int):
    return v1 ** v2


@builtin("<")
def less(v1: int, v2: int):
    return v1 < v2


@builtin("<=")
def lessEq(v1: int, v2: int):
    return v1 <= v2


@builtin(">")
def greater(v1: int, v2: int):
    return v1 > v2


@builtin(">=")
def greaterEq(v1: int, v2: int):
    return v1 >= v2


@builtin("=")
def equal(v1: Value, v2: Value):
    return v1 == v2


@builtin("!=")
def notEq(v1: Value, v2: Value):
    return v1 != v2


@builtin("not")
def boolNot(b: bool):
    return not b


@builtin("and")
def boolAnd(b1: bool, b2: bool, *args: bool):
    return all([b1, b2, *args])


@builtin("or")
def boolOr(b1: bool, b2: bool, *args: bool):
    return any([b1, b2, *args])
