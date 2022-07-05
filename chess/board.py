from typing import List, Tuple, Optional

from chess.pieces import Piece, Bishop


class Board:
    def __init__(self, size: int, position: List[List[str]] = None):
        self.size: int = size
        if position:
            self.position = position
        else:
            self.position = [["." for _ in range(size)] for _ in range(size)]

    def __repr__(self):
        s: str = "\n".join([str(row) for row in self.position])
        return "\n" + s + "\n"

    def next_available_square(self) -> Optional[Tuple[int, int]]:
        """

        :return:
        """
        for x in range(len(self.position)):
            for y in range(len(self.position[0])):
                if self.get_square_available((x, y)):
                    return x, y
        return None

    def get_square_available(self, square: Tuple):
        """

        :param square:
        :return:
        """
        x, y = square
        if self.position[x][y] == ".":
            return True
        else:
            return False

    def add_piece(self, piece: Piece, square: Tuple):
        """

        :param piece:
        :param square:
        :return:
        """
        if self.get_square_available(square):
            x, y = square
            self.position[x][y] = piece.marker
            for square in piece.scope(square, self.size):
                x, y = square
                self.position[x][y] = "X"

    def solve(self):
        """
        TODO: Probably some kind of tree structure, gotta see if its fast enough

        :return:
        """
        pass


def main():
    b = Board(
        size=4
    )

    while b.next_available_square():
        b.add_piece(Bishop(), b.next_available_square())
        print(b)


if __name__ == "__main__":
    main()
