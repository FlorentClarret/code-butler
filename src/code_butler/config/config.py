from __future__ import annotations

from typing import Any

from code_butler.config.github import Github


class Config:
    def __init__(self, data: dict[str, Any]):
        self.__data = data

    @property
    def data(self) -> dict[str, Any]:
        return self.__data

    @property
    def github(self) -> Github:
        return Github(**self.__data.get("github", {}))

    def set_field(self, key: str, value: str):
        config = self.data
        fields = key.split(".")

        for f in fields[:-1]:
            if f not in config:
                config[f] = {}
            config = config[f]

        config[fields[-1]] = value
