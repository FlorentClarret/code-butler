from __future__ import annotations

from pathlib import Path

import pytest
from code_butler.rules.github.save_state import SaveStateRule
from code_butler.rules.issue import Issue


@pytest.fixture
def repository(repository):
    file = Path(repository.working_dir) / "file.txt"
    file.write_text('run: echo "::save-state name=state1::value1"')
    repository.index.add(["file.txt"])
    repository.index.commit("Commit")

    return repository


def test_fix(repository):
    rule = SaveStateRule(repository)
    issue = Issue(rule, repository, "file.txt")
    rule.fix(issue)

    assert (
        Path(repository.working_dir) / "file.txt"
    ).read_text() == 'run: echo "state1=value1" >> "$GITHUB_STATE"'


def test_detect(repository):
    rule = SaveStateRule(repository)
    issues = list(rule.detect())

    assert len(issues) == 1
    assert issues[0].file_path == "file.txt"
    assert issues[0].rule == rule


def test_detect_not_found(repository):
    rule = SaveStateRule(repository)
    (Path(repository.working_dir) / "file.txt").unlink()
    assert not list(rule.detect())
