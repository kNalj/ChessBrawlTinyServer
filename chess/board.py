import copy
import time
from typing import List, Tuple, Optional

from chess.pieces import Piece, Bishop, Knight, Queen


class Board:
    def __init__(self, size: int, piece: Piece, position: List[List[str]] = None) -> None:
        """
        Constructor for board class. There are two versions:
            - when position is not passed
                Constructrs an empty board of size NxN
            - when position is passed
                Constructs a board based on passed position

        :param size: size of the board, both in x and y directions
        :param piece: which piece will be placed on this board
        :param position: initial state of the board
        """
        self.size: int = size
        self.piece: Piece = piece
        self.position: List[List[str]]
        if position:
            self.position = position
        else:
            self.position = [["." for _ in range(size)] for _ in range(size)]

    def __repr__(self) -> str:
        """
        Just a readable version of the position. List of lists where each inner list is printed in a new row.

        :return: string representation of the position
        """
        s: str = "\n".join([str(row) for row in self.position])
        return "\n" + s + "\n"

    def get_number_of_filled_squares(self) -> int:
        """
        Squares filled by pieces. This is useful because its equal to the depth of the tree.

        :return: Depth of the tree at which this position is
        """
        depth: int = 0
        for x in range(len(self.position)):
            for y in range(len(self.position[0])):
                if self.position[x][y] == self.piece.marker:
                    depth += 1

        return depth

    def get_number_of_available_squares_from_last_filled_square(self) -> int:
        """
        This is number of not visited combinations that are available from this position

        :return: number of unique combinations that can be made from this position
        """
        combinations: int = 0
        for x in range(len(self.position) - 1, -1, -1):
            for y in range(len(self.position[0]) - 1, -1, -1):
                if self.position[x][y] == ".":
                    combinations += 1
                if self.position[x][y] == self.piece.marker:
                    return combinations

        return combinations

    def get_all_available_squares(self, starting_square: Tuple[int, int] = (0, 0)) -> List[Tuple[int, int]]:
        """
        Returns a list of squares where pieces can be placed without being attacked or attacking any other pieces.

        :param starting_square: From which square to start searching
        :return:
        """
        start_x, start_y = starting_square
        squares: List[Tuple[int, int]] = []
        for x in range(start_x, len(self.position)):
            if x != start_x:
                start_y = 0
            for y in range(start_y, len(self.position[0])):
                if self.is_square_available((x, y)):
                    squares.append((x, y))

        return squares

    def is_square_available(self, square: Tuple) -> bool:
        """
        Check if the square is attacked by any pieces.

        :param square: tuple representing the square
        :return: True if not attacked, else False
        """
        x, y = square
        if self.position[x][y] == ".":
            return True
        else:
            return False

    def add_piece(self, piece: Piece, square: Tuple) -> None:
        """
        Adds a piece to the board, and marks all the fields that this piece is attacking

        :param piece: Which piece to add to the board
        :param square: To which square to add the piece
        :return:
        """
        if self.is_square_available(square):
            x, y = square
            self.position[x][y] = piece.marker
            for square in piece.scope(square, self.size):
                x, y = square
                self.position[x][y] = "X"

    def get_number_of_combinations(self) -> int:
        """
        Method that calculates number of combinations from current position. Only needs to count the number of available
        squares from the last piece placed on the board (bcs pieces are placed on the board in order)

        :return:
        """
        if self.get_number_of_filled_squares() == self.size - 1:
            return self.get_number_of_available_squares_from_last_filled_square()
        else:
            return 0

    def solve(self,  starting_square: Tuple = (0, 0)) -> 'Node':
        """
        Recursively solve position.

        :param starting_square: From which square to start searching. Cuts down execution time.
        :return: Node that holds board and all subsequent boards that can be made from that one.
        """

        node = Node(self)
        available_squares = self.get_all_available_squares(starting_square=starting_square)
        solved = self.get_number_of_filled_squares() == self.size - 1

        if available_squares and not solved:
            for square in available_squares:
                pos = copy.deepcopy(self.position)
                b = Board(size=self.size, piece=self.piece, position=pos)
                b.add_piece(self.piece, square)
                node.children.append(b.solve(starting_square=square))

        return node


class Node:
    def __init__(self, board: Board):
        self.board: Board = board
        self.children: List[Node] = []

    def __repr__(self, depth=0):
        ret = "\t" * depth + repr(self.board) + "\n"
        for child in self.children:
            ret += child.__repr__(depth+1)

        return ret

    def get_combinations(self):
        sum = 0
        for child in self.children:
            sum += child.get_combinations()

        return self.board.get_number_of_combinations() + sum


class Tree:
    def __init__(self, root: Node):
        self.root = root

    def __repr__(self):
        print(self.root)

    def get_total(self):
        return self.root.get_combinations()


def main():
    b = Board(
        size=6,
        piece=Bishop()
    )

    start = time.time()
    tree: Tree = Tree(b.solve())
    stop = time.time()

    print("################")
    print(tree.root)
    print("################")
    print("Execution time: ", stop - start)

    print(tree.get_total())


if __name__ == "__main__":
    main()
