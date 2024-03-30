import pytest

from code_butler.config.config import Config


@pytest.fixture
def config():
    return Config({"foo": "bar", "baz": {"key": "value"}})


def test_github():
    assert Config({"github": {"token": "my-token"}}).github.token == "my-token"


@pytest.mark.parametrize(
    "key, value, expected_dict",
    [
        (
            "new_key",
            "new_value",
            {"foo": "bar", "new_key": "new_value", "baz": {"key": "value"}},
        ),
        (
            "foo",
            "new_value",
            {"foo": "new_value", "baz": {"key": "value"}},
        ),
        (
            "new.key",
            "new_value",
            {"foo": "bar", "baz": {"key": "value"}, "new": {"key": "new_value"}},
        ),
        (
            "baz.key",
            "new_value",
            {
                "foo": "bar",
                "baz": {"key": "new_value"},
            },
        ),
    ],
)
def test_set_field(config, key, value, expected_dict):
    config.set_field(key, value)
    assert config.data == expected_dict
