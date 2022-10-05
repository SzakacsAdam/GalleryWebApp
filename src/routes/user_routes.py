from typing import Dict, Tuple

from falcon import Request
from falcon import Response

from src.utils import parse_dict_to_json_bytes, MimeTypes
from storages.dhtml_storage import DHTMLFolder


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


class DHTMLFilesRoute:
    def __init__(self, dhtml_component: DHTMLFolder) -> None:
        self.component: DHTMLFolder = dhtml_component

    def on_get(self, req: Request, resp: Response) -> None:
        message: Dict[str, str] = {self.component.name: self.component.items}
        parsed_message: Tuple[bytes, int] = parse_dict_to_json_bytes(
            message
        )
        resp.data, resp.content_length = parsed_message
        resp.content_type = MimeTypes.JSON.value
