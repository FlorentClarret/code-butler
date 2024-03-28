import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import tomli_w

from code_butler.config.file import ConfigFile


@pytest.fixture
def config_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        file = Path(temp_dir) / "config.toml"
        file.write_text(tomli_w.dumps({"github": {"token": "my-token"}}))
        yield ConfigFile(file)


def test_read(config_file):
    assert config_file.read() == '[github]\ntoken = "my-token"\n'


def test_load(config_file):
    assert config_file.config is None
    config_file.load()
    assert config_file.config.github.token == "my-token"


def test_get_default_location():
    with patch("platformdirs.user_data_dir") as user_data_dir:
        user_data_dir.return_value = Path("/tmp")
        assert ConfigFile.get_default_location() == Path("/tmp/config.toml")


def test_save(config_file):
    config_file.save("content")
    assert config_file.path.read_text() == "content"


def test_restore(config_file):
    config_file.restore()
    assert config_file.path.read_text() == '[github]\ntoken = ""\n'
