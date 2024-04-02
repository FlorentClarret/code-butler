from unittest.mock import Mock

from code_butler.rules.github.deprecated_commands import DeprecatedCommands
from code_butler.rules.github.save_state import SaveStateRule
from code_butler.rules.github.set_output import SetOutputRule
from git import Repo


def test_init():
    rule = DeprecatedCommands(Mock(Repo))

    assert len(rule.rules) == 2
    assert isinstance(rule.rules[0], SetOutputRule)
    assert isinstance(rule.rules[1], SaveStateRule)
