from __future__ import annotations

from typing import Any

from code_butler.config.github import Github


class Config:
    def __init__(self, data: dict[str, Any]):
        self.__data = data

    @property
    def github(self) -> Github:
        return Github(**self.__data["github"])
