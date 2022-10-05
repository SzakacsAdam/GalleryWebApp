import os
from typing import Tuple, List, Dict, Union

from src.utils import MimeTypes


class DHTMLFile:
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


class DHTMLFolder:
    __slots__ = ("dir_src", "dir_name", "mime_type", "dir_content")

    def __init__(self, dir_src: str, auto_load: bool = True) -> None:
        self.dir_src: str = dir_src
        self.dir_name: str = dir_src.split(os.sep)[-1]
        self.mime_type: str = MimeTypes[self.dir_name.upper()].value
        self.dir_content: Dict[str, DHTMLFile] = {}

        if auto_load:
            self.search_files()

    def search_files(self) -> None:
        for root, dirs, files in os.walk(self.dir_src, topdown=False):
            for file_name in files:
                if file_name.endswith(self.dir_name):
                    file_path: str = os.path.join(root, file_name)
                    self.dir_content[file_name] = DHTMLFile(file_path)

    def __getitem__(self, key: str) -> Union[DHTMLFile, None]:
        return self.dir_content.get(key, None)

    def __contains__(self, item: str) -> bool:
        return item in self.dir_content

    @property
    def items(self) -> List[str]:
        return list(self.dir_content.keys())

    @property
    def name(self) -> str:
        return self.dir_name


class DHTMLStorage:
    __DHTML_FILES: Tuple[str, ...] = ("html", "css", "js")
    _RESOURCE_DIR_NAME: str = "resources"
    __slots__ = ("resource_src", "_container")

    def __init__(self, resource_src: str = None) -> None:

        if resource_src is None:
            resource_src = os.path.join(os.getcwd(), self._RESOURCE_DIR_NAME)

        if not os.path.isdir(resource_src):
            resource_src = os.path.join(os.getcwd(), resource_src)
            if not os.path.isdir(resource_src):
                raise ValueError(f"Resource dir not found at: {resource_src}")

        src_content: List[str] = os.listdir(resource_src)
        if not src_content:
            raise ValueError(f"Resource dir is empty at: {resource_src}")

        if not set(self.__DHTML_FILES).issubset(set(src_content)):
            raise ValueError(
                f"Cannot find all DHTML file's folder: {self.__DHTML_FILES}"
            )
        self.resource_src: str = resource_src
        self._container: Dict[str, DHTMLFolder] = {}

    def load_container(self) -> None:
        self._container: Dict[str, DHTMLFolder] = {
            folder: DHTMLFolder(os.path.join(self.resource_src, folder))
            for folder in self.__DHTML_FILES
        }

    def __getitem__(self, key: str) -> Union[DHTMLFolder, None]:
        return self._container.get(key, None)

    @property
    def dhtml_files(self) -> Tuple[str, ...]:
        return self.__DHTML_FILES
