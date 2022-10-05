import falcon

from src.routes import DHTMLFilesRoute
from src.routes import Ping
from src.storages import DHTMLStorage
from storages.dhtml_storage import DHTMLFolder


class GalleryWebAPP:

    def __init__(self) -> None:
        self._app: falcon.App = falcon.App(cors_enable=True)
        self.dhtml_files: DHTMLStorage = DHTMLStorage()
        self.dhtml_files.load_container()

    @property
    def app(self) -> falcon.App:
        return self._app

    def add_routes(self) -> None:
        ping: Ping = Ping()
        self._app.add_route("/ping", ping)
        for file_type in self.dhtml_files.dhtml_files:
            dhtml_files: DHTMLFolder = self.dhtml_files[file_type]
            dhtml_route_handler: DHTMLFilesRoute = DHTMLFilesRoute(dhtml_files)
            self._app.add_route("/%s" % dhtml_files.dir_name,
                                dhtml_route_handler)
            self._app.add_route("/%s/{name}" % dhtml_files.dir_name,
                                dhtml_route_handler, suffix="item")


if __name__ == '__main__':
    gallery: GalleryWebAPP = GalleryWebAPP()
    gallery.add_routes()
