import pytest

from code_butler.config.config import Config


@pytest.fixture
def config():
    return Config({"github": {"token": "my-token"}})


def test_github(config):
    assert config.github.token == "my-token"
