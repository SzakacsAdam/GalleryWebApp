import os
from typing import Tuple, List, Dict, Union

from src.utils import MimeTypes


class _DHTMLFile:
    __slots__ = ("file_path", "file_bytes", "file_bytes_len")

    def __init__(self, file_path: str, auto_load: bool = True) -> None:
        self.file_path: str = file_path
        self.file_bytes: bytes = b''
        self.file_bytes_len = len(self.file_bytes)

        if auto_load:
            self.read_file()
            self.calc_file_len()

    def read_file(self) -> None:
        with open(self.file_path, "rb") as f:
            self.file_bytes = f.read()

    def calc_file_len(self) -> None:
        self.file_bytes_len = len(self.file_bytes)


class _DHTMLFolder:
    __slots__ = ("dir_src", "dir_name", "mime_type", "dir_content")

    def __init__(self, dir_src: str, auto_load: bool = True) -> None:
        self.dir_src: str = dir_src
        self.dir_name: str = dir_src.split(os.sep)[-1]
        self.mime_type: str = MimeTypes[self.dir_name.upper()].value
        self.dir_content: Dict[str, _DHTMLFile] = {}

        if auto_load:
            self.search_files()

    def search_files(self) -> None:
        for root, dirs, files in os.walk(resources_src, topdown=False):
            for file_name in files:
                if file_name.endswith(self.dir_name):
                    file_path: str = os.path.join(root, file_name)
                    self.dir_content[file_name] = _DHTMLFile(file_path)


class DHTMLStorage:
    DHTML_FILES: Tuple[str, ...] = ("html", "css", "js", "ico")
    __slots__ = ("resource_src", "_container")

    def __init__(self, resource_src: str = None) -> None:
        self.resource_src: str = resource_src
        if not os.path.isdir(resource_src):
            resource_src = os.path.join(os.getcwd(), resource_src)
            if not os.path.isdir(resource_src):
                raise ValueError(f"Resource dir not found at: {resource_src}")

        src_content: List[str] = os.listdir(resource_src)
        if not src_content:
            raise ValueError(f"Resource dir is empty at: {resource_src}")

        if not set(self.DHTML_FILES).issubset(set(src_content)):
            raise ValueError(
                f"Cannot find all DHTML file's folder: {self.DHTML_FILES}"
            )
        self._container: Dict[str, _DHTMLFolder] = {}

    def load_container(self) -> None:
        self._container: Dict[str, _DHTMLFolder] = {
            folder: _DHTMLFolder(os.path.join(self.resource_src, folder))
            for folder in self.DHTML_FILES
        }

    def __getitem__(self, key: str) -> Union[_DHTMLFolder, None]:
        return self._container.get(key, None)


if __name__ == '__main__':
    resources_src: str = "/mnt/f/GalleryWebApp/resources"

    storage: DHTMLStorage = DHTMLStorage(resources_src)
