import os
import tempfile
from pathlib import Path

import pytest
import tomli_w
from click.testing import CliRunner

from code_butler.config.file import ConfigFile


@pytest.fixture(autouse=True)
def config_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        file = Path(temp_dir) / "config.toml"
        file.write_text(tomli_w.dumps({"github": {"token": "my-token"}}))
        os.environ["CODE_BUTLER_CONFIG"] = str(file)
        yield ConfigFile(file)


class BoundCliRunner(CliRunner):
    def __init__(self, command):
        super().__init__()
        self.__command = command

    def __call__(self, *args, **kwargs):
        kwargs.setdefault("catch_exceptions", False)
        return self.invoke(self.__command, args, **kwargs)


@pytest.fixture(scope="session")
def code_butler():
    from code_butler import cli

    return BoundCliRunner(cli.code_butler)