from __future__ import annotations

from pathlib import Path
from typing import cast

import tomli
import tomli_w

from code_butler.config.config import Config
from code_butler.config.models.console import Console
from code_butler.config.models.github import Github


class ConfigFile:
    def __init__(self, path: Path | None = None):
        self.path = path or self.get_default_location()
        self.config = cast(Config, None)

    def load(self) -> None:
        self.config = Config(tomli.loads(self.read()))

    def read(self) -> str:
        return self.path.read_text()

    def save(self, content: str | None = None) -> None:
        if content is None:
            content = tomli_w.dumps(self.config.data)

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(content, encoding="utf-8")

    def restore(self) -> None:
        self.save(
            tomli_w.dumps(
                {
                    "github": Github().model_dump(),
                    "console": Console().model_dump(),
                }
            )
        )

    @classmethod
    def get_default_location(cls) -> Path:
        from platformdirs import user_data_dir

        return Path(user_data_dir("code-butler", appauthor=False)) / "config.toml"
