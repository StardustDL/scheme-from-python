from sfpy.functions import Function
from .programs import Program
from .tokens import TRUE as TOKEN_TRUE, FALSE as TOKEN_FALSE, LEFT, RIGHT
from .values import Int, Symbol, Value, EMPTY, TRUE as VALUE_TRUE, FALSE as VALUE_FALSE


class Evaluator:
    def __init__(self, parent: "Evaluator | None" = None) -> None:
        self.parent = parent
        self.symbols: dict[str, Value] = {}

        if self.parent is None:
            from .builtins import builtins
            self.symbols.update(builtins)

    def sub(self, symbols: dict[str, Value] | None = None) -> "Evaluator":
        sub = Evaluator(self)
        if symbols:
            sub.symbols.update(symbols)
        return sub

    def evaluate(self, program: Program) -> Value:
        if not program:
            return EMPTY
        if program.combination():
            return self.combination(program)
        elif program.atomic():
            return self.atomic(program)
        else:
            return self.sequence(program)

    def symbol(self, symbol: str | Symbol, value=None) -> Value:
        symbol = str(symbol)
        if value == None:
            if self.parent == None:
                assert symbol in self.symbols, f"Undefined symbol: '{symbol}'"
            elif symbol not in self.symbols:
                return self.parent.symbol(symbol)
            return self.symbols[symbol]
        else:
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

        return operator(*[o if operator.signature.lazy else self.evaluate(o) for o in operands], eval=self)

    def sequence(self, program: Program) -> Value:
        result = EMPTY
        for sub in program.split():
            result = self.evaluate(sub)
        return result
