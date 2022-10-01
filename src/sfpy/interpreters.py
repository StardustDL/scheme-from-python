from .exceptions import InvalidInput
from .values import EMPTY, Value
from . import __version__


class Interpreter:
    def __init__(self) -> None:
        from .parsers import Parser
        from .evaluators import Evaluator
        self.parser = Parser()
        self.evaluator = Evaluator(interpreter=self)

    def interprete(self, text: str) -> Value:
        program = self.parser.parse(text)
        assert program is not None, InvalidInput(text)
        result = self.evaluator.evaluate(program)
        assert isinstance(
            result, Value), f"Unexpected evaluated value: {result}"
        return result

    def interact(self):
        print(f"scheme-from-python (sfpy) {__version__}")
        while True:
            try:
                text = input("> ")
                while True:
                    program = self.parser.nocheck(text)
                    if program.valid():
                        break

                    right = program.missingRight()
                    line = input(". " + "  " * (right or 0))

                    if not line:
                        # auto fix right parentheses
                        text += ")" * (right or 0)
                        break

                    text += f" {line}"

                result = self.interprete(text)
                self.evaluator.symbol("_", result)
                if result != EMPTY:
                    print(result)
            except Exception as ex:
                import traceback
                traceback.print_exception(ex)
