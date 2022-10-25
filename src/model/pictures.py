from typing import Dict
from typing import List


class Picture:
    __slots__ = ("name", "alt")

    def __init__(self, name: str, alt: str) -> None:
        self.name: str = name
        self.alt: str = alt

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "alt": self.alt
        }


class Pictures:
    def __init__(self) -> None:
        self.pictures: List[Picture] = []
