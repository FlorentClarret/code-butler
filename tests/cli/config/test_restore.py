def test_standard(code_butler, config_file):
    result = code_butler("config", "restore")

    assert result.exit_code == 0, result.output
    assert result.output == "Settings were successfully restored.\n"

    config_file.load()
    assert config_file.config.github.token == ""


def test_allow_invalid_config(code_butler, config_file):
    config_file.save("""repo = [""]""")
    result = code_butler("config", "restore")

    assert result.exit_code == 0, result.output
    assert result.output == "Settings were successfully restored.\n"
