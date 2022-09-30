from functools import wraps
from typing import Callable

from sfpy.tokens import LEFT

from .programs import Program
from .values import Symbol, Value


class Function(Value):
    __rawType__ = Callable

    def __init__(self, raw, count: int | None = None, lazy: bool = False, repr: str | None = None) -> None:
        super().__init__(raw)
        self.count = count
        self.lazy = lazy
        self.repr = repr

    def __call__(self, *args):
        if self.count is not None:
            assert len(
                args) == self.count, f"The number of operands must be {self.count}."
        return Value.ensure(self.raw(*args))

    def __repr__(self) -> str:
        return self.repr if self.repr is not None else super().__repr__()


def function(count: int | None = None, lazy: bool = False, repr: str | None = None):
    def decorator(func: Callable):
        return Function(func, count=count, lazy=lazy, repr=repr)
    return decorator
