from sfpy.functions import Function
from .programs import Program
from .tokens import TRUE as TOKEN_TRUE, FALSE as TOKEN_FALSE, LEFT, RIGHT
from .values import Int, Symbol, Value, EMPTY, TRUE as VALUE_TRUE, FALSE as VALUE_FALSE
from .builtins import builtinSymbols


class Evaluator:
    def __init__(self) -> None:
        self.symbols: dict[str, Value] = {**builtinSymbols}

    def evaluate(self, program: Program) -> Value:
        if not program:
            return EMPTY
        if program[0] == LEFT:
            return self.combination(program[1:-1])
        else:
            return self.atomic(program)

    def symbol(self, symbol: str | Symbol) -> Value:
        symbol = str(symbol)
        assert symbol in self.symbols, f"Undefined symbol: '{symbol}'"
        return self.symbols[symbol]

    def atomic(self, program: Program) -> Value:
        assert len(program) == 1, f"Cannot directly evaluate a non-single program: {program}"

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
        assert isinstance(
            operator, Function), f"Operator must be a function: {operator}"

        return operator(*[o if operator.lazy else self.evaluate(o) for o in operands])
