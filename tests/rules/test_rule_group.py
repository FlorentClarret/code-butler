import collections
from unittest.mock import Mock

from code_butler.rules.issue import Issue
from code_butler.rules.rule import Rule
from code_butler.rules.rule_group import RuleGroup
from git import Repo


class DummyRuleGroup(RuleGroup):
    def __init__(self, repository):
        m1, m2 = Mock(Rule), Mock(Rule)
        m1.detect.return_value = []
        m2.detect.return_value = []
        super().__init__(repository, [m1, m2])

    def commit_message(self):
        return "commit_message"

    def pr_body(self):
        return "body"


def test_detect():
    repo = Mock(Repo)
    rule_group = DummyRuleGroup(repo)
    collections.deque(rule_group.detect(), maxlen=0)

    rule_group.rules[0].detect.assert_called_once()
    rule_group.rules[1].detect.assert_called_once()


def test_fix():
    rule_group = DummyRuleGroup(Mock(Repo))
    issue = Mock(Issue)
    rule_group.fix(issue)

    issue.fix.assert_called_once()


def test_commit_message():
    rule_group = DummyRuleGroup(Mock(Repo))
    assert rule_group.commit_message() == "commit_message"


def test_pr_body():
    rule_group = DummyRuleGroup(Mock(Repo))
    assert rule_group.pr_body() == "body"
