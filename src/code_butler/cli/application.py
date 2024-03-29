from __future__ import annotations

from pathlib import Path

from code_butler.config.file import ConfigFile


class Application:
    def __init__(self, config_file: Path | None = None):
        self.__config_file = ConfigFile(config_file)

    @property
    def config_file(self) -> ConfigFile:
        self.__config_file.load()
        return self.__config_file
