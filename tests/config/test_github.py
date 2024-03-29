import os
from unittest import mock
from code_butler.config.github import Github


@mock.patch.dict(os.environ, {"CODE_BUTLER_GITHUB_TOKEN": "my-token"})
def test_read_token_from_env_variable():
    assert Github().token == "my-token"


@mock.patch.dict(os.environ, {})
def test_no_token():
    assert Github().token == ""
