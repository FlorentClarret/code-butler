import os
from unittest import mock

from code_butler.config.models.console import Console


@mock.patch.dict(os.environ, {"CODE_BUTLER_CONSOLE_COLOR": "false"})
def test_read_color_from_env_variable():
    assert Console().color is False


@mock.patch.dict(os.environ, {})
def test_no_color():
    assert Console().color is True
