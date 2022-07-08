import logging
import time

from aiohttp.abc import Application
from aiohttp.web_request import Request
from typing import Dict, Any

from aiohttp.web_response import Response

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
        app: Application = web.Application()
        app.add_routes(
            [
                web.get("/", self.process_request),
            ]
        )

        return app

    def run_server(self):
        """
        Spin up the server

        :return:
        """
        if self.app:
            web.run_app(self.app, port=self.port)
        else:
            logging.log(level=40, msg="Web app is not properly initiated")

    async def process_request(self, request: Request) -> Response:
        """
        Extract data from the request and call the method that calculates number of combinations.

        :param request: request passed from the client
        :return:
        """
        data: Dict[str, Any] = await request.json()
        self.validate_data(data)

        json: Dict[str, Any] = self.calculate_possible_solutions(size=data["n"], piece=self.create_piece(name=data["chessPiece"]))

        return web.json_response(json)

    @staticmethod
    def create_piece(name) -> Piece:
        """
        Helper method that instantiates a piece based on the string passed in the request.

        :param name:
        :return:
        """
        name_lower: str = name.lower()
        class_dict: Dict[str, Any] = {"queen": Queen, "rook": Rook, "bishop": Bishop, "knight": Knight}
        return class_dict[name_lower]()

    @staticmethod
    def validate_data(data: dict) -> None:
        """
        Check that the data passed in the request can be used to calculate

        :param data: Dictionary containing data that needs to be checked
        :return:
        """
        if not 1 <= int(data["n"]) <= 8:
            raise ValueError(f"Board size must be in range: 0-8. Got {data['n']}")
        if not data["chessPiece"].lower() in ["queen", "rook", "bishop", "knight"]:
            raise ValueError(f"chessPiece must be one of: [queen, rook, bishop, knight]. Got {data['chessPiece']}")

    @staticmethod
    def calculate_possible_solutions(size: int, piece: Piece):
        """
        Instantiate a chess board, and call an algorithm that calculates number of possible combinations

        :param size: size of the board
        :param piece: Chess piece to place on the board
        :return: Number of solutions
        """
        b: Board = Board(
            size=int(size),
            piece=piece
        )

        start: float = time.time()
        tree: Tree = Tree(b.solve())
        stop: float = time.time()

        soulutions_count: int = tree.get_total()
        print(f"Request for piece: {piece.name}, and a board size of {size} executed in: {stop - start}")

        return {"solutionsCount": f"{soulutions_count}"}


def main():
    server = Server(8088)


if __name__ == "__main__":
    main()
