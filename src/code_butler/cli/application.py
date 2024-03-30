from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from code_butler.cli.console import Console
from code_butler.config.file import ConfigFile

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Callable


class Application:
    def __init__(self, exit_function: Callable, config_file: Path | None = None):
        self.__config_file = ConfigFile(config_file)
        self.__exit_function = exit_function
        self.__console = Console(
            color=self.config_file.config.console.color,
        )

    @cached_property
    def config_file(self) -> ConfigFile:
        self.__config_file.load()
        return self.__config_file

    @property
    def console(self) -> Console:
        return self.__console

    def abort(self, text: str | None = None, code: int = 1):
        if text:
            self.console.print(text)
        self.__exit_function(code)
