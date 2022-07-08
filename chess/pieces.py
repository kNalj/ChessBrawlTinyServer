from typing import List, Tuple


class Piece:
    def __init__(self, name: str, marker: str, direction: List[Tuple[int, int]]):
        self.name: str = name
        self.marker: str = marker
        self.direction: List[Tuple[int, int]] = direction

    def scope(self, square: Tuple, boardsize: int) -> List[Tuple]:
        """
        A list of squares (tuple) that this piece is attacking

        :return: returns a list of valid board positions that this piece can move to in one move
        """

        scope = []
        for dx, dy in self.direction:
            x, y = square
            while (0 <= x + dx <= boardsize - 1) and (0 <= y + dy <= boardsize - 1):
                scope.append((x + dx, y + dy))
                x += dx
                y += dy
        return scope


class Queen(Piece):
    def __init__(self):
        name = "queen"
        marker = "Q"
        direction = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        super().__init__(name, marker, direction)


class Bishop(Piece):
    def __init__(self):
        name = "bishop"
        marker = "B"
        direction = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

        super().__init__(name, marker, direction)


class Knight(Piece):
    def __init__(self):
        name = "knight"
        marker = "N"
        direction = [(2, 1), (2, -1), (-1, 2), (1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2)]

        super().__init__(name, marker, direction)

    def scope(self, square: Tuple, boardsize: int) -> List[Tuple]:
        """

        :param square:
        :param boardsize:
        :return:
        """
        scope = []
        x, y = square

        for dx, dy in self.direction:
            if (0 <= x + dx <= boardsize - 1) and (0 <= y + dy <= boardsize - 1):
                scope.append((x + dx, y + dy))
        return scope


class Rook(Piece):
    def __init__(self):
        name = "rook"
        marker = "R"
        direction = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        super().__init__(name, marker, direction)


def main():
    q = Queen()
    print(q.scope((3, 3), 5))

    b = Bishop()
    print(b.scope((3, 3), 4))

    r = Rook()
    print(r.scope((3, 3), 7))

    k = Knight()
    print(k.scope((3, 3), 6))


if __name__ == "__main__":
    main()
