from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from git import Repo

    from code_butler.rules.rule import Rule


class Issue:
    def __init__(
        self,
        rule: Rule,
        repository: Repo,
        file_path: str,
    ):
        self.rule = rule
        self.repository = repository
        self.file_path = file_path

    def fix(self) -> None:
        self.rule.fix(self)
