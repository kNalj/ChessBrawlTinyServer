import logging

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
                web.get("/", self.parse_request)
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

    def parse_request(self, request):
        """

        :param request:
        :return:
        """
        return web.Response(text="This is a place holder response")

    def validate_request(self, request):
        """

        :param request:
        :return:
        """
        pass

    def calculate_possible_solutions(self, request):
        """

        :param request:
        :return:
        """
        pass


def main():
    server = Server(8088)


if __name__ == "__main__":
    main()
