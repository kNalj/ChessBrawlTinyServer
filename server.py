import logging
import time
from chess.board import Board, Tree
from chess.pieces import Piece, Knight, Bishop, Rook, Queen

from aiohttp import web


class Server:
    def __init__(self, port: int = 8088):
        """
        Constructor for the server class

        :param port: On which port will the server be accessible.
        """
        self.port: int = port
        self.app: web.Application = self.init_app()

        self.run_server()

    def init_app(self) -> web.Application:
        """
        Create web app and setup routes

        :return: created web app
        """
        app = web.Application()
        app.add_routes(
            [
                web.get("/", self.parse_request),
            ]
        )

        return app

    def run_server(self):
        """

        :return:
        """
        if self.app:
            web.run_app(self.app, port=self.port)
        else:
            logging.log(level=40, msg="Web app is not properly initiated")

    async def parse_request(self, request):
        """

        :param request:
        :return:
        """
        data = await request.json()
        self.validate_data(data)

        json = self.calculate_possible_solutions(size=data["n"], piece=self.create_piece(name=data["chessPiece"]))

        return web.json_response(json)

    @staticmethod
    def create_piece(name) -> Piece:
        name_lower: str = name.lower()
        if name_lower == "queen":
            return Queen()
        elif name_lower == "rook":
            return Rook()
        elif name_lower == "bishop":
            return Bishop()
        elif name_lower == "knight":
            return Knight()

    @staticmethod
    def validate_data(data):
        """

        :param data:
        :return:
        """
        if not 0 <= int(data["n"]) <= 9:
            raise ValueError(f"Board size must be in range: 0-8. Got {data['n']}")
        if not data["chessPiece"].lower() in ["queen", "rook", "bishop", "knight"]:
            raise ValueError(f"chessPiece must be one of: [queen, rook, bishop, knight]. Got {data['chessPiece']}")

    @staticmethod
    def calculate_possible_solutions(size: int, piece: Piece):
        """

        :param size:
        :param piece:
        :return:
        """
        b = Board(
            size=int(size),
            piece=piece
        )

        start = time.time()
        tree: Tree = Tree(b.solve())
        stop = time.time()

        soulutions_count: int = tree.get_total()
        print(f"Request for piece: {piece.name}, and a board size of {size} executed in: {stop - start}")

        return {"solutionsCount": f"{soulutions_count}"}


def main():
    server = Server(8088)


if __name__ == "__main__":
    main()
