from functools import wraps, reduce
from pathlib import Path
from typing import Callable

from .exceptions import InvalidInput

from .evaluators import Evaluator
from .programs import Program
from .functions import Function, function
from .values import EMPTY, Int, Number, Value, String
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

    symbol = String(name[0])
    assert symbol.isSymbol(), "The symbol name is not valid."

    value = eval.evaluate(value)
    eval.symbol(symbol, value)

    return value


@builtin("if")
def branch(predicate: Program, exprTrue: Program, exprFalse: Program, *, eval: Evaluator):
    return eval.evaluate(exprTrue if eval.evaluate(predicate) else exprFalse)


def getParameterList(parameters: Program) -> list[String]:
    assert len(parameters) > 0 and parameters.valid(
    ) and parameters[0] == LEFT, f"Parameter list {parameters} is invalid."

    parameters = parameters.split()
    assert all(
        len(p) == 1 for p in parameters), f"Parameter list {parameters} is invalid."
    assert len(set(p[0] for p in parameters)) == len(
        parameters), "Parameter names contain conflicts."

    parameters: list[String] = [String(p[0]) for p in parameters]
    assert all(s.isSymbol()
               for s in parameters), f"Parameter list {parameters} is invalid."

    return parameters


@builtin("lam")
@builtin("lambda")
def lambdafunc(parameters: Program, body: Program, *, eval: Evaluator):
    parameters = getParameterList(parameters)

    @function
    def raw(*args):
        return eval.sub({str(parameter): argument for parameter, argument in zip(parameters, args)}).evaluate(body)

    raw.repr = f"( lambda ( {' '.join(p.raw for p in parameters)} ) {' '.join(body)} )"
    raw.signature.parameters = [(Value, False)] * len(parameters)

    return raw


@builtin("mac")
@builtin("macro")
def macro(parameters: Program, body: Program):  # do not capture macro creation environment
    parameters = getParameterList(parameters)

    @function
    def raw(*args: Program, eval: Evaluator):
        mp = {str(parameter): argument for parameter,
              argument in zip(parameters, args)}
        return eval.evaluate(Program(sum((mp.get(str(token), [token]) for token in body), [])))

    raw.repr = f"( macro ( {' '.join(p.raw for p in parameters)} ) {' '.join(body)} )"
    raw.signature.parameters = [(Program, False)] * len(parameters)

    return raw


@builtin("from")
def fromFile(file: Program, *, eval: Evaluator):
    assert len(file) == 1, "Only one file can be provided."
    file: Path = Path(file[0])
    assert file.exists() and file.is_file(), f"File '{file}' not found."
    assert eval.interpreter is not None, "No interpreter found."
    text = file.read_text()
    program = eval.interpreter.parser.parse(text)
    assert program is not None, InvalidInput(text)
    return eval.evaluate(program)


@builtin("syms")
@builtin("symbols")
def symbols(*, eval: Evaluator):
    return eval.symbols


@builtin("+")
def add(v1: Number, v2: Number, *args: Number):
    return sum(v.raw for v in [v1, v2, *args])


@builtin("-")
def subtract(v1: Number, v2: Number):
    return v1.raw - v2.raw


@builtin("*")
def multiply(v1: Number, v2: Number, *args: Number):
    return reduce(lambda x, y: x * y, (v.raw for v in [v1, v2, *args]))


@builtin("//")
def divideInt(v1: Number, v2: Number):
    assert v2.raw != 0, "The divisor cannot be zero."
    return v1.raw // v2.raw


@builtin("%")
def divideInt(v1: Number, v2: Number):
    assert v2.raw != 0, "The divisor cannot be zero."
    return v1.raw % v2.raw


@builtin("/")
def divide(v1: Number, v2: Number):
    assert v2.raw != 0, "The divisor cannot be zero."
    return v1.raw / v2.raw


@builtin("^")
def power(v1: Number, v2: Number):
    return v1.raw ** v2.raw


@builtin("max")
def maxNum(v1: Number, v2: Number, *args: Number):
    return max(v.raw for v in [v1, v2, *args])


@builtin("min")
def minNum(v1: Number, v2: Number, *args: Number):
    return min(v.raw for v in [v1, v2, *args])


@builtin("<")
def less(v1: Number, v2: Number):
    return v1.raw < v2.raw


@builtin("<=")
def lessEq(v1: Number, v2: Number):
    return v1.raw <= v2.raw


@builtin(">")
def greater(v1: Number, v2: Number):
    return v1.raw > v2.raw


@builtin(">=")
def greaterEq(v1: Number, v2: Number):
    return v1.raw >= v2.raw


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


@builtin("print")
def printFunc(v: Value):
    print(v)
    return EMPTY
