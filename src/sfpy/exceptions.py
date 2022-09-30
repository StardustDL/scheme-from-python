class InvalidInput(Exception):
    def __init__(self, input: str) -> None:
        super().__init__(f"Invalid input: '{input}'")
