import re
from abc import ABC
from pathlib import Path
from typing import TYPE_CHECKING

from code_butler.rules.issue import Issue
from code_butler.rules.rule import Rule

if TYPE_CHECKING:
    from typing import Iterable

    from git import Repo


class SearchAndReplaceRule(Rule, ABC):
    def __init__(self, repository: "Repo", search: str, pattern: str, replace: str):
        super().__init__(repository)
        self.search = search
        self.pattern = pattern
        self.replace = replace

    def detect(self) -> "Iterable[Issue]":
        for line in self.repository.git.execute(
            ["git", "grep", "-l", self.search]
        ).splitlines():  # type: ignore
            yield Issue(self, self.repository, str(line))

    def fix(self, issue: "Issue") -> None:
        path = Path(self.repository.working_dir) / issue.file_path
        content = path.read_text()
        new_content = re.sub(
            self.pattern,
            self.replace,
            content,
        )
        path.write_text(new_content)
