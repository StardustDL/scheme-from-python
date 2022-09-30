from typing import Callable
from .values import Value


class Function(Value):
    __rawType__ = Callable

    def __init__(self, raw, lazy: bool = False) -> None:
        super().__init__(raw)
        self.lazy = lazy

    def __call__(self, *args, **kwds):
        return Value.ensure(self.raw(*args, **kwds))


def function(func: Callable):
    return Function(func)


def lazyFunction(func: Callable):
    return Function(func, True)
