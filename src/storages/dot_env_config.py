from os import getcwd
from os.path import isfile, join
from typing import Dict, Union

from dotenv import dotenv_values


class DotEnvConfig:
    __slots__ = "_conf"

    def __init__(self, env_path: str = None) -> None:
        self._conf: Dict[str, str] = {}
        if env_path is None:
            env_path: str = join(getcwd(), '.env')
        if not isfile(env_path):
            raise FileNotFoundError(f"Cannot find .env at: {env_path}")
        self._conf = dotenv_values(env_path)

    def add_dot_env_load(self, env_path: str = None):
        self._conf = dotenv_values(env_path)

    def __getitem__(self, key: str) -> Union[str, None]:
        return self._conf.get(key, None)

    def __repr__(self) -> str:
        conf_content: str = ', '.join([f'{key}={val}' for key, val
                                       in self._conf.items()])
        return f"{self.__class__.__name__}({conf_content})"

    def __str__(self) -> str:
        conf_keys: str = ', '.join(self._conf.keys())
        return f"{self.__class__.__name__}({conf_keys})"
