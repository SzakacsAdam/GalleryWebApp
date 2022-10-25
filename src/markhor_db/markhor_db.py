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
