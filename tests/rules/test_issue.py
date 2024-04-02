from unittest.mock import Mock

from code_butler.rules.issue import Issue
from code_butler.rules.rule import Rule
from git import Repo


def test_fix():
    rule = Mock(Rule)
    issue = Issue(rule, Mock(Repo), "file_path")
    issue.fix()
    rule.fix.assert_called_once_with(issue)
