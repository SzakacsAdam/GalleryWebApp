from typing import Dict


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
