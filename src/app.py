import falcon

from src.routes import Ping


class GalleryWebAPP:

    def __init__(self) -> None:
        self._app: falcon.App = falcon.App(cors_enable=True)

        self.ping: Ping = Ping()

    @property
    def app(self) -> falcon.App:
        return self._app

    def add_routes(self) -> None:
        self._app.add_route("/ping", self.ping)
