from code_butler.cli import Application


def test_token_from_cli(config_file):
    assert Application("the-token", config_file.path).token == "the-token"


def test_token_from_file(config_file):
    assert Application(None, config_file.path).token == "my-token"
