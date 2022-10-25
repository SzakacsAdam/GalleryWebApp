from typing import Dict
from typing import List


class Picture:
    __slots__ = ("name", "alt")

    def __init__(self, name: str, alt: str) -> None:
        self.name: str = name
        self.alt: str = alt

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Picture):
            if self.name == other.name and self.alt == other.alt:
                return True
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.to_dict())

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "alt": self.alt
        }


class Pictures:
    def __init__(self) -> None:
        self.pictures: List[Picture] = []

    def add_picture(self, picture: Picture) -> None:
        self.pictures.append(picture)
