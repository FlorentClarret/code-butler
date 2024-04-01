from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from code_butler.rules.rule import Rule

if TYPE_CHECKING:
    from typing import Iterable

    from git import Repo

    from code_butler.rules.issue import Issue


class RuleGroup(Rule, ABC):
    def __init__(self, repository: Repo, rules: Iterable[Rule]):
        super().__init__(repository)
        self.rules = list(rules)

    def detect(self) -> Iterable[Issue]:
        for rule in self.rules:
            yield from rule.detect()

    def fix(self, issue: Issue) -> None:
        issue.fix()

    @abstractmethod
    def commit_message(self) -> str:
        pass

    @abstractmethod
    def pr_body(self) -> str:
        pass
