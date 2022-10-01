from dataclasses import dataclass, field
from functools import wraps
from typing import Callable, Type, TYPE_CHECKING
from inspect import signature, Parameter

from .tokens import LEFT

from .programs import Program
from .values import Bool, Int, Object, String, Value, allValues

if TYPE_CHECKING:
    from .evaluators import Evaluator


EVAL_PARAMETER = "eval"


@dataclass
class Signature:
    parameters: list[tuple[Type[Value], bool]] | None = None
    variadic: tuple[Type[Value], bool] | None = None
    lazy: bool = False
    eval: bool = False

    def adapt(self, *args: Value) -> list:
        if self.parameters is None:
            return [v.raw if isinstance(v, Object) else v for v in args]

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
                variadic.append(arg.raw if flat or isinstance(arg, Object) else arg)

            args = args[:len(parameters)]
        else:
            assert len(args) == len(
                parameters), f"The number of operands must be {len(parameters)}, but got {len(args)}."

        result = []
        for i, (parameter, arg) in enumerate(zip(parameters, args)):
            target, flat = parameter
            assert isinstance(
                arg, target), f"The {i}-th argument must of type {target}, but got {type(arg)}."
            result.append(arg.raw if flat or isinstance(arg, Object) else arg)

        return result + variadic

    def __repr__(self) -> str:
        result = ""

        if self.parameters is None:
            result += "any"
        else:
            items = [t[0].__qualname__ if t else "?" for t in self.parameters]
            if self.variadic:
                items.append(f"{self.variadic[0].__qualname__}...")
            result += ", ".join(items)

        if self.lazy:
            result += "*"

        return result


class Function(Value):
    __rawType__ = Callable

    def __init__(self, raw, signature: Signature | None = None, repr: str | None = None) -> None:
        super().__init__(raw)
        self.signature = signature or inferSignature(raw)
        self.repr = repr

    def __call__(self, *args, eval: "Evaluator"):
        return Value.ensure(
            self.raw(*self.signature.adapt(*args),
                     **({EVAL_PARAMETER: eval} if self.signature.lazy and self.signature.eval else {})))

    def __repr__(self) -> str:
        return self.repr if self.repr is not None else f"(lambda ({repr(self.signature)}) (...))"


def inferSignature(func: Callable) -> Signature:
    try:
        sign = signature(func)
    except:
        return Signature()

    parameters = [p for p in sign.parameters.values() if p.kind in {
        Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD, Parameter.VAR_POSITIONAL} and p.default == Parameter.empty]

    result = Signature(parameters=[],
                       lazy=all(p.annotation == Program for p in parameters) and len(
                           parameters) > 0,
                       eval=any(p.name == EVAL_PARAMETER for p in sign.parameters.values() if p.kind == Parameter.KEYWORD_ONLY))

    def infer(p: Parameter):
        assert result.lazy or p.annotation != Program, f"Parameter named '{p.name}' cannot be Program in a non-lazy function, use Program for all parameters."

        for item in allValues():
            if p.annotation in {item, item.__rawType__}:
                return (item, p.annotation == item.__rawType__)

        if p.annotation == Program:
            return (Program, False)
        else:
            return (Value, False)

    if len(parameters) > 0 and parameters[-1].kind == Parameter.VAR_POSITIONAL:
        result.variadic = infer(parameters[-1])

    for p in [p for p in parameters if p.kind in {
            Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD}]:
        result.parameters.append(infer(p))

    return result


def function(func: Callable):
    return Function(func)
