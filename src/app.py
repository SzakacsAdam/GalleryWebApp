import falcon


class GalleryWebAPP:

    def __init__(self) -> None:
        self._app: falcon.App = falcon.App(cors_enable=True)

    @property
    def app(self) -> falcon.App:
        return self._app

    def add_routes(self) -> None:
        pass
