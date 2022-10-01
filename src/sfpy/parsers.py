from .programs import Program
from .tokens import Token


class Parser:
    def nocheck(self, text: str) -> Program:
        return Program(map(Token, text.replace("(", " ( ").replace(")", " ) ").split()))

    def parse(self, text: str) -> Program | None:
        result = self.nocheck(text)
        return result if result.valid() else None
