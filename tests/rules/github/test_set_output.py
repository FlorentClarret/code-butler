from __future__ import annotations

from pathlib import Path

import pytest
from code_butler.rules.github.set_output import SetOutputRule
from code_butler.rules.issue import Issue


@pytest.fixture
def repository(repository):
    file = Path(repository.working_dir) / "file.txt"
    file.write_text('run: echo "::set-output name=output1::value3"')
    repository.index.add(["file.txt"])
    repository.index.commit("Commit")

    return repository


def test_fix(repository):
    rule = SetOutputRule(repository)
    issue = Issue(rule, repository, "file.txt")
    rule.fix(issue)

    assert (
        Path(repository.working_dir) / "file.txt"
    ).read_text() == 'run: echo "output1=value3" >> "$GITHUB_OUTPUT"'


def test_detect(repository):
    rule = SetOutputRule(repository)
    issues = list(rule.detect())

    assert len(issues) == 1
    assert issues[0].file_path == "file.txt"
    assert issues[0].rule == rule


def test_detect_not_found(repository):
    rule = SetOutputRule(repository)
    (Path(repository.working_dir) / "file.txt").unlink()
    assert not list(rule.detect())
