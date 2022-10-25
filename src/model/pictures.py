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
    def __init__(self, pictures: List[Picture] = []) -> None:
        self.pictures: List[Picture] = pictures

    def add_picture(self, picture: Picture) -> None:
        self.pictures.append(picture)

    def rem_picture(self, picture: Picture) -> None:
        self.pictures.remove(picture)

    def update_picture(self, name: str, alt: str) -> None:
        for picture in self.pictures:
            if (
                    picture.name == name or
                    picture.alt == alt
            ):
                picture.name = name
                picture.alt = alt
                break

    def to_dict(self) -> Dict[str, List[Dict[str, str]]]:
        key: str = self.__class__.__name__
        val: List[Dict[str, str]] = [
            picture.to_dict()
            for picture in self.pictures
        ]
        return {key: val}
