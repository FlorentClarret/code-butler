from __future__ import annotations

from pathlib import Path

from code_butler.config.file import ConfigFile


class Application:
    def __init__(self, token: str | None, config_file: Path | None = None):
        self.__config_file = ConfigFile(config_file)
        self.__token = token

    @property
    def config_file(self) -> ConfigFile:
        self.__config_file.load()
        return self.__config_file

    @property
    def token(self) -> str | None:
        if self.__token is None:
            return self.config_file.config.github.token
        return self.__token
