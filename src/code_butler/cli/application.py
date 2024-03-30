from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from code_butler.config.file import ConfigFile

if TYPE_CHECKING:
    from pathlib import Path


class Application:
    def __init__(self, config_file: Path | None = None):
        self.__config_file = ConfigFile(config_file)

    @cached_property
    def config_file(self) -> ConfigFile:
        self.__config_file.load()
        return self.__config_file
