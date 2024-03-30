def test_call(code_butler):
    result = code_butler("config", "set", "github.token", "new-token")

    assert result.exit_code == 0, result.output
    assert not result.output

    result = code_butler("config", "show")

    assert result.exit_code == 0, result.output
    assert (
        result.output
        == """[github]
token = "new-token"
"""
    )
