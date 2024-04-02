from unittest.mock import Mock

from code_butler.rules.rule import Rule
from git import Repo


class DummyRule(Rule):
    def detect(self):
        pass

    def fix(self, issue):
        pass

    def commit_message(self):
        return "commit_message"

    def pr_body(self):
        return "body"


def test_init():
    mock = Mock(Repo)
    rule = DummyRule(mock)
    assert rule.repository == mock


def test_id():
    rule = DummyRule(Mock())
    assert rule.id == "DummyRule"


def test_pr_title():
    rule = DummyRule(Mock())
    assert rule.pr_title() == "commit_message"
