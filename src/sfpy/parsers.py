from .programs import Program
from .tokens import Token


class Parser:
    def parse(self, text: str) -> Program | None:
        result = Program(map(Token, text.replace("(", " ( ").replace(")", " ) ").split()))
        return result if result.valid() else None
