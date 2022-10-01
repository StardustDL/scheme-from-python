from .tokens import Token, LEFT, RIGHT


class Program(list[Token]):
    def __getitem__(self, key):
        if isinstance(key, int):
            return super().__getitem__(key)
        if isinstance(key, slice):
            return Program(super().__getitem__(key))
        else:
            raise TypeError

    def missingRight(self) -> int | None:
        cnt = 0
        for token in self:
            if token == LEFT:
                cnt += 1
            elif token == RIGHT:
                if cnt <= 0:
                    return None
                cnt -= 1
        return cnt

    def valid(self):
        return self.missingRight() == 0

    def combination(self):
        return len(self) > 1 and self[0] == LEFT and self[-1] == RIGHT

    def atomic(self):
        return len(self) == 1

    def split(self) -> list["Program"]:
        target = self[1:-1] if self.combination() else self
        result, st = [], []

        for i, token in enumerate(target):
            if token == LEFT:
                st.append(i)
            elif token == RIGHT:
                bg = st.pop()
                if not st:
                    result.append(target[bg:i+1])
            elif not st:
                result.append(target[i:i+1])

        return result
