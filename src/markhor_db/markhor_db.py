from os import getcwd
from os.path import isfile
from os.path import join
from typing import Any
from typing import Dict
from typing import List

from base_db import _CRUDOperations
from src.model import Picture
from src.model import Pictures


class MarkhorDB:
    _DB_EXT: str = "json"
    __slots__ = ("_db",)

    def __init__(self, src_db: str = None, auto_save: bool = True) -> None:
        if (
                src_db is None
                or not isfile(src_db)
                or not src_db.lower().endswith(self._DB_EXT)
        ):
            db_file_name: str = f"{self.__class__.__name__}.{self._DB_EXT}"
            src_db = join(getcwd(), db_file_name)
        self._db: _CRUDOperations = _CRUDOperations(src_db, auto_save)

    async def load_db(self) -> None:
        await self._db.load()

    async def save_db(self) -> None:
        await self._db.save()

    async def save_pictures(self, pictures: Pictures) -> None:
        content: Dict[str, Any] = pictures.to_dict()
        await self._db.update(content)

    def get_pictures(self) -> Pictures:
        pictures: List[Picture] = [
            Picture(**picture)
            for picture in self._db.get("Pictures")
        ]
        return Pictures(pictures)
