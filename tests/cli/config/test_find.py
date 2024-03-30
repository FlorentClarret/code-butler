def test(code_butler, config_file):
    result = code_butler("config", "find")

    assert result.exit_code == 0, result.output
    assert result.output == str(config_file.path) + "\n"
