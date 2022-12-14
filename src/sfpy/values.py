from abc import ABC
import inspect
from types import NoneType
from typing import Callable


def allValues():
    from .functions import Function
    return [v for v in globals().values() if inspect.isclass(v) and issubclass(v, Value)] + [Function]

def allConcreteValues():
    return [v for v in allValues() if not inspect.isabstract(v) and not ABC in v.__bases__]


class Value(ABC):
    __rawType__ = object

    def __init__(self, raw) -> None:
        if not isinstance(raw, self.__rawType__):
            raise Exception(
                f"Not a compatible type of the value, expected {self.__rawType__}, but got {type(raw)}.")
        self.raw = raw

    def __bool__(self):
        return not (isinstance(self, Bool) and self.raw == False)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, type(self)) and other.raw == self.raw

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}({repr(self.raw)})"

    @classmethod
    def ensure(cls, raw) -> "Value":
        if isinstance(raw, Value):
            return raw
        for item in allConcreteValues():
            if isinstance(raw, item.__rawType__):
                return item(raw)
        return Object(raw)


class Bool(Value):
    __rawType__ = bool

    def __repr__(self) -> str:
        from .tokens import TRUE, FALSE
        return TRUE if self.raw else FALSE

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Bool) and other.raw == self.raw


class Number(Value, ABC):
    def __repr__(self) -> str:
        return repr(self.raw)


class Int(Number):
    __rawType__ = int


class Float(Number):
    __rawType__ = float


class Complex(Number):
    __rawType__ = complex


class Empty(Value):
    __rawType__ = NoneType

    def __repr__(self) -> str:
        return "<empty>"


class String(Value):
    __rawType__ = str

    def __repr__(self) -> str:
        return self.raw

    def isSymbol(self):
        return len(self.raw) > 0 and any(not c.isdigit() for c in self.raw)


class Object(Value, ABC):
    """Wrapper for unsupported Python values."""
    pass


TRUE = Bool(True)
FALSE = Bool(False)
EMPTY = Empty(None)
