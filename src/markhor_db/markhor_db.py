from json import dumps as json_dumps
from json import loads as json_loads
from typing import Any
from typing import Dict
from typing import Union

from aiofiles import open as aio_open


class _FileHandling:
    __slots__ = "_src"

    def __init__(self, src: str) -> None:
        self._src: str = src

    async def load_file(self) -> str:
        async with aio_open(self._src, mode='r', encoding="UTF-8") as f:
            return await f.read()

    async def save_file(self, data: str) -> None:
        async with aio_open(self._src, mode='w+', encoding="UTF-8") as f:
            await f.write(data)

    async def load_json(self) -> Dict[str, Any]:
        content: str = await self.load_file()
        return json_loads(content)

    async def save_dict(self, data: Dict[str, Any]) -> None:
        json_data: str = json_dumps(data, ensure_ascii=True, indent=4,
                                    sort_keys=True, encoding="UTF-8")
        await self.save_file(json_data)


class _CRUDOperations:
    __slots__ = ("_file_handler", "_auto_save", "_storage")

    def __init__(self, src: str, auto_save: bool = True) -> None:
        self._file_handler: _FileHandling = _FileHandling(src)
        self._auto_save: bool = auto_save
        self._storage: Dict[str, Any] = {}

    def __getitem__(self, key: str) -> Union[Any, None]:
        return self._storage.get(key, None)

    def get(self, key: str) -> Union[Any, None]:
        return self.__getitem__(key)

    async def load(self) -> None:
        self._storage = await self._file_handler.load_file()

    async def save(self) -> None:
        await self._file_handler.save_dict(self._storage)

    async def auto_save(self) -> None:
        if self._auto_save is True:
            await self.save()
