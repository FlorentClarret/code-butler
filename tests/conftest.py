import tempfile
from pathlib import Path

import pytest
import tomli_w

from code_butler.config.file import ConfigFile


@pytest.fixture
def config_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        file = Path(temp_dir) / "config.toml"
        file.write_text(tomli_w.dumps({"github": {"token": "my-token"}}))
        yield ConfigFile(file)
