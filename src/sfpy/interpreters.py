from sfpy.evaluators import Evaluator
from sfpy.exceptions import InvalidInput
from sfpy.values import EMPTY, Value
from .parsers import Parser
from . import __version__


class Interpreter:
    def __init__(self) -> None:
        self.parser = Parser()
        self.evaluator = Evaluator()

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
                if result != EMPTY:
                    print(result)
            except Exception as ex:
                import traceback
                traceback.print_exception(ex)
