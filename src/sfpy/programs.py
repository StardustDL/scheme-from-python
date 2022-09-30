from .tokens import Token, LEFT, RIGHT


class Program(list[Token]):
    def valid(self):
        if len(self) > 1:
            if self[0] != LEFT or self[-1] != RIGHT:
                return False
        return self.validParenthese()

    def validParenthese(self):
        cnt = 0
        for token in self:
            if token == LEFT:
                cnt += 1
            elif token == RIGHT:
                if cnt <= 0:
                    return False
                cnt -= 1
        return cnt == 0

    def __getitem__(self, key):
        if isinstance(key, int):
            return super().__getitem__(key)
        if isinstance(key, slice):
            return Program(super().__getitem__(key))
        else:
            raise TypeError

    def split(self) -> list["Program"]:
        assert self.validParenthese(), f"The sub-program is not valid: {self}"

        result = []

        st = []
        for i, token in enumerate(self):
            if token == LEFT:
                st.append(i)
            elif token == RIGHT:
                bg = st.pop()
                if not st:
                    result.append(self[bg:i+1])
            elif not st:
                result.append(self[i:i+1])

        return result
