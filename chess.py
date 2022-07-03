from typing import List, Optional, Tuple


class Piece:
    def __init__(self, direction):
        self.name: str
        self.aliases: Optional[List[str]]
        self.direction: List[Tuple] = direction

    def scope(self, square: Tuple) -> List[Tuple]:
        """
        A list of squares (tuple) that this piece is attacking

        :return: returns a list of valid board positions that this piece can move to in one move
        """

        scope = []
        for dx, dy in self.direction:
            x, y = square
            while (0 <= x + dx <= 7) and (0 <= y + dy <= 7):
                scope.append((x + dx, y + dy))
                x += dx
                y += dy
        return scope


class Queen(Piece):
    def __init__(self):
        self.name = "Queen"
        self.aliases = ["q"]
        direction = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        super().__init__(direction)


class Bishop(Piece):
    def __init__(self):
        self.name = "bishop"
        self.aliases = ["b", "laufer"]
        direction = [(1, 1), (-1, 1), (-1, -1), (1, -1)]

        super().__init__(direction)


class Knight(Piece):
    def __init__(self):
        self.name = "knight"
        self.aliases = ["k", "horse"]
        direction = [(2, 1), (2, -1), (-1, 2), (1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2)]

        super().__init__(direction)

    def scope(self, square: Tuple) -> List[Tuple]:
        """

        :param square:
        :return:
        """
        scope = []
        x, y = square

        for dx, dy in self.direction:
            if (0 <= x + dx <= 7) and (0 <= y + dy <= 7):
                scope.append((x + dx, y + dy))
        return scope


class Rook(Piece):
    def __init__(self):
        self.name = "rook"
        self.aliases = ["r", "tower"]
        direction = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        super().__init__(direction)


def main():
    q = Queen()
    print(q.scope((3, 3)))

    b = Bishop()
    print(b.scope((3, 3)))

    r = Rook()
    print(r.scope((3, 3)))

    k = Knight()
    print(k.scope((3, 3)))

if __name__ == "__main__":
    main()