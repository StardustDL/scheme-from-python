from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, Type
from inspect import signature, Parameter

from sfpy.tokens import LEFT

from .programs import Program
from .values import Bool, Int, Symbol, Value


@dataclass
class Signature:
    parameters: list[tuple[Type[Value], bool] | None] | None = None
    variadic: tuple[Type[Value], bool] | None = None
    lazy: bool = False

    def adapt(self, *args: Value) -> list:
        if self.parameters is None:
            return

        parameters = self.parameters

        if self.lazy:
            parameters = [(Program, False) for _ in parameters]

        variadic = []

        if self.variadic is not None:
            assert len(args) >= len(
                parameters), f"Missing arguments, expected {len(parameters)}, but got {len(args)}."

            target, flat = self.variadic
            for arg in args[len(parameters):]:
                assert isinstance(
                    arg, target), f"The variadic {i}-th argument must of type {target}, but got {type(arg)}."
                variadic.append(arg.raw if flat else arg)

            args = args[:len(parameters)]
        else:
            assert len(args) == len(
                parameters), f"The number of operands must be {len(parameters)}, but got {len(args)}."

        result = []
        for i, (parameter, arg) in enumerate(zip(parameters, args)):
            if parameter is None:
                result.append(arg)
                continue
            target, flat = parameter
            assert isinstance(
                arg, target), f"The {i}-th argument must of type {target}, but got {type(arg)}."
            result.append(arg.raw if flat else arg)

        return result + variadic


class Function(Value):
    __rawType__ = Callable

    def __init__(self, raw, signature: Signature | None = None, repr: str | None = None) -> None:
        super().__init__(raw)
        self.signature = signature or Signature()
        self.repr = repr

    def __call__(self, *args):
        return Value.ensure(self.raw(*self.signature.adapt(*args)))

    def __repr__(self) -> str:
        return self.repr if self.repr is not None else super().__repr__()


def inferSignature(func: Callable) -> Signature:
    sign = signature(func)
    parameters = list(sign.parameters.values())

    assert all(p.kind in {
        Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD, Parameter.VAR_POSITIONAL} for p in parameters), "Functions with keyword parameters are not supported."

    result = Signature(parameters=[], lazy=all(
        p.annotation == Program for p in parameters))

    def infer(p: Parameter):
        assert result.lazy or p.annotation != Program, f"Parameter named '{p.name}' cannot be Program in a non-lazy function, use Program for all parameters."

        if p.annotation in {bool, Bool}:
            return (Bool, p.annotation != Bool)
        elif p.annotation in {int, Int}:
            return (Int, p.annotation != Int)
        elif p.annotation in {Callable, Function}:
            return (Function, p.annotation != Function)
        elif p.annotation == Program:
            return (Program, False)
        else:
            return None

    if len(parameters) > 0 and parameters[-1].kind == Parameter.VAR_POSITIONAL:
        result.variadic = infer(parameters[-1])

    for p in [p for p in parameters if p.kind in {
            Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD}]:
        result.parameters.append(infer(p))

    return result


def function(func: Callable):
    return Function(func, signature=inferSignature(func), repr=repr)
