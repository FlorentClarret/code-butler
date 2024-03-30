def test_call(code_butler, config_file, mocker):
    mock = mocker.patch("click.launch")
    result = code_butler("config", "explore")

    assert result.exit_code == 0, result.output
    mock.assert_called_once_with(str(config_file.path), locate=True)
