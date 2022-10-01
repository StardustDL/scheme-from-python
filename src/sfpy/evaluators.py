from sfpy.functions import Function
from .programs import Program
from .tokens import TRUE as TOKEN_TRUE, FALSE as TOKEN_FALSE, LEFT, RIGHT
from .values import Int, Symbol, Value, EMPTY, TRUE as VALUE_TRUE, FALSE as VALUE_FALSE
from .builtins import builtins


CORE_DEFINE = {"define", "def"}
CORE_LAMBDA = {"lambda", "lam"}
CORE_BRANCH = {"if"}

CORE_SYMBOLS = CORE_DEFINE | CORE_LAMBDA | CORE_BRANCH


class Evaluator:
    def __init__(self, parent: "Evaluator | None" = None) -> None:
        self.parent = parent
        self.symbols: dict[str, Value] = {}

        if self.parent is None:
            self.symbols.update(builtins)

        from .core import define, branch, lambdafunc
        cdefine = define(self)
        cbranch = branch(self)
        clambda = lambdafunc(self)
        self.symbols.update({
            **builtins,
            **{name: cdefine for name in CORE_DEFINE},
            **{name: cbranch for name in CORE_BRANCH},
            **{name: clambda for name in CORE_LAMBDA},
        })

    def sub(self, symbols: dict[str, Value] | None = None) -> "Evaluator":
        sub = Evaluator(self)
        from .core import lambdafunc
        clambda = lambdafunc(sub)
        sub.symbols.update({
            **(symbols or {}),
            **{name: clambda for name in CORE_LAMBDA},
        })
        return sub

    def evaluate(self, program: Program) -> Value:
        if not program:
            return EMPTY
        if program[0] == LEFT:
            return self.combination(program[1:-1])
        else:
            return self.atomic(program)

    def symbol(self, symbol: str | Symbol, value=None) -> Value:
        symbol = str(symbol)
        if value == None:
            if self.parent == None:
                assert symbol in self.symbols, f"Undefined symbol: '{symbol}'"
            elif symbol not in self.symbols:
                return self.parent.symbol(symbol)
            return self.symbols[symbol]
        else:
            assert symbol not in CORE_SYMBOLS, f"Core symbol '{symbol}' cannot be changed."
            self.symbols[symbol] = value

    def atomic(self, program: Program) -> Value:
        assert len(
            program) == 1, f"Cannot directly evaluate a non-single program: {program}"

        token = program[0]
        assert token not in {LEFT, RIGHT}, "Cannot evaluate a parenthese."

        if token == TOKEN_TRUE:
            return VALUE_TRUE
        if token == TOKEN_FALSE:
            return VALUE_FALSE

        try:
            intval = int(token)
            return Int(intval)
        except:
            pass

        return self.symbol(token)

    def combination(self, program: Program) -> Value:
        subprograms = program.split()
        operator, operands = subprograms[0], subprograms[1:]

        operator = self.evaluate(operator)
        if isinstance(operator, Symbol):
            operator = self.symbol(operator)
        assert isinstance(
            operator, Function), f"Operator must be a function: {operator}"

        return operator(*[o if operator.signature.lazy else self.evaluate(o) for o in operands])
