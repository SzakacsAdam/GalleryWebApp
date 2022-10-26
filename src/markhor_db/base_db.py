from json import dumps as json_dumps
from json import loads as json_loads
from sys import getsizeof
from typing import Any
from typing import Dict
from typing import Tuple
from typing import Union
from os import stat as os_stat

from aiofiles import open as aio_open


class _FileHandling:
    __slots__ = "_src"

    def __init__(self, src: str) -> None:
        self._src: str = src

    @property
    def size(self) -> int:
        return os_stat(self._src).st_size

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
                                    sort_keys=True)
        await self.save_file(json_data)


class _CRUDOperations:
    __slots__ = ("_file_handler", "_auto_save", "_storage")

    def __init__(self, src: str, auto_save: bool = True) -> None:
        self._file_handler: _FileHandling = _FileHandling(src)
        self._auto_save: bool = auto_save
        self._storage: Dict[str, Any] = {}

    @property
    def size(self) -> int:
        return getsizeof(self._storage)

    def __getitem__(self, key: str) -> Union[Any, None]:
        return self._storage.get(key, None)

    def get(self, key: str) -> Union[Any, None]:
        return self.__getitem__(key)

    def keys(self) -> Tuple[str, ...]:
        return tuple(self._storage.keys())

    def has_key(self, key: str) -> bool:
        return key in self._storage

    async def set(self, key: str, value: Any) -> None:
        self._storage[key] = value
        await self.auto_save()

    async def update(self, content: Dict[str, Any]) -> None:
        self._storage.update(content)
        await self.auto_save()

    async def rem(self, key: str) -> Any:
        content: Any = self._storage.pop(key)
        await self.auto_save()
        return content

    async def rem_last_inserted(self) -> Dict[str, Any]:
        content: Dict[str, Any] = dict(self._storage.popitem())
        await self.auto_save()
        return content

    async def clear(self) -> None:
        self._storage.clear()
        await self.auto_save()

    async def load(self) -> None:
        self._storage = await self._file_handler.load_json()

    async def save(self) -> None:
        await self._file_handler.save_dict(self._storage)

    async def auto_save(self) -> None:
        if self._auto_save is True:
            await self.save()
