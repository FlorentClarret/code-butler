from __future__ import annotations

from pathlib import Path

import pytest
from code_butler.rules.common.search_replace_rule import SearchAndReplaceRule
from code_butler.rules.issue import Issue
from git import Repo


class DummyRule(SearchAndReplaceRule):
    def __init__(self, repository: Repo):
        super().__init__(repository, search="123", pattern="\\d+", replace="REPLACE")

    def commit_message(self) -> str:
        pass

    def pr_body(self) -> str:
        pass


@pytest.fixture
def repository(repository):
    file = Path(repository.working_dir) / "file.txt"
    file.write_text("one two 123 four five")
    repository.index.add(["file.txt"])
    repository.index.commit("Commit")

    return repository


def test_fix(
    repository,
):
    rule = DummyRule(repository)
    issue = Issue(rule, repository, "file.txt")
    rule.fix(issue)

    assert (
        Path(repository.working_dir) / "file.txt"
    ).read_text() == "one two REPLACE four five"


def test_detect(repository):
    rule = DummyRule(repository)
    issues = list(rule.detect())

    assert len(issues) == 1
    assert issues[0].file_path == "file.txt"
    assert issues[0].rule == rule


def test_detect_not_found(repository):
    rule = DummyRule(repository)
    rule.search = "not found"
    assert not list(rule.detect())
