import os
from unittest import mock


@mock.patch.dict(os.environ, {"CODE_BUTLER_CONSOLE_COLOR": "false"})
def test_call(code_butler, config_file):
    result = code_butler("config", "show")

    assert result.exit_code == 0, result.output
    assert (
        result.output
        == """[github]
token = "my-token"
"""
    )
