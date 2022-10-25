from json import dumps as json_dumps
from json import loads as json_loads
from typing import Any
from typing import Dict

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
