from abc import ABC
from types import NoneType
from typing import Callable


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

    @classmethod
    def ensure(cls, raw) -> "Value":
        if isinstance(raw, Value):
            return raw
        if isinstance(raw, bool):
            return Bool(raw)
        if isinstance(raw, int):
            return Int(raw)
        if isinstance(raw, Callable):
            from .functions import Function
            return Function(raw)
        if raw == None:
            return Empty(raw)
        raise Exception(f"Unsupport value type: {type(raw)}.")


class Bool(Value):
    __rawType__ = bool

    def __repr__(self) -> str:
        from .tokens import TRUE, FALSE
        return TRUE if self.raw else FALSE

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Bool) and other.raw == self.raw


class Int(Value):
    __rawType__ = int

    def __repr__(self) -> str:
        return repr(self.raw)


class Empty(Value):
    __rawType__ = NoneType

    def __repr__(self) -> str:
        return "<empty>"


class Symbol(Value):
    __rawType__ = str

    def __repr__(self) -> str:
        return self.raw

    def valid(self):
        return len(self.raw) > 0 and any(not c.isdigit() for c in self.raw)


TRUE = Bool(True)
FALSE = Bool(False)
EMPTY = Empty(None)
