import json
from enum import Enum
from typing import Tuple


def convert_str_to_camelcase(string: str) -> str:
    if len(string) < 2:
        return string.lower()
    out: str = ''.join(char for char in string.title() if char.isalnum())
    return f"{out[0].lower()}{out[1:]}"


def parse_dict_to_json_bytes(dictionary: dict) -> Tuple[bytes, int]:
    byte_json: bytes = bytes(
        json.dumps(dictionary, ensure_ascii=True, indent=4),
        encoding="utf-8"
    )
    return byte_json, len(byte_json)


class MimeTypes(Enum):
    # Dynamic HTML files
    JS = "text/javascript; charset=UTF-8"
    HTML = "text/html; charset=UTF-8"
    CSS = "text/css; charset=UTF-8"
    ICO = "image/vnd.microsoft.icon"

    JSON = "application/json"

    # image formats
    AVIF = "image/avif"
    GIF = "image/gif"
    JPG = JPEG = "image/jpeg"
    PNG = "image/png"
    SVG = "image/svg+xml"
    TIFF = "image/tiff"
    WEBP = "image/webp"
