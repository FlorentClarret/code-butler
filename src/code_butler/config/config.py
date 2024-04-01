from __future__ import annotations

from typing import TYPE_CHECKING

from code_butler.config.models.console import Console
from code_butler.config.models.github import Github

if TYPE_CHECKING:
    from typing import Any


class Config:
    def __init__(self, data: dict[str, Any]):
        self.__data = data

    @property
    def data(self) -> dict[str, Any]:
        return self.__data

    @property
    def github(self) -> Github:
        return Github(**self.__data.get("github", {}))

    @property
    def console(self) -> Console:
        return Console(**self.__data.get("console", {}))

    def set_field(self, key: str, value: str) -> None:
        config = self.data
        fields = key.split(".")

        for f in fields[:-1]:
            if f not in config:
                config[f] = {}
            config = config[f]

        if value.lower() == "true":
            config[fields[-1]] = True
        elif value.lower() == "false":
            config[fields[-1]] = False
        else:
            config[fields[-1]] = value
