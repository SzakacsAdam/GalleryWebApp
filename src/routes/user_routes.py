from typing import Dict, Tuple

from falcon import Request
from falcon import Response

from src.utils import parse_dict_to_json_bytes


class Ping:
    DEFAULT_CONTENT_TYPE: str = "application/json"
    __slots__ = "parsed_message"

    def __init__(self) -> None:
        message: Dict[str, str] = {"Ping": "Hi from AssetCacheProxy v1"}
        self.parsed_message: Tuple[bytes, int] = parse_dict_to_json_bytes(
            message
        )

    def on_get(self, req: Request, resp: Response) -> None:
        resp.data, resp.content_length = self.parsed_message
        resp.content_type = self.DEFAULT_CONTENT_TYPE
