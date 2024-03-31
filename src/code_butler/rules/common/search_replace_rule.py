import re
from abc import ABC
from pathlib import Path
from typing import TYPE_CHECKING

from code_butler.rules.common.rule import Rule

if TYPE_CHECKING:
    from git import Repo
    from typing import Iterable


class SearchAndReplaceRule(Rule, ABC):
    def __init__(self, repository: "Repo", search: str, pattern: str, replace: str):
        super().__init__(repository)
        self.search = search
        self.pattern = pattern
        self.replace = replace

    def detect(self) -> "Iterable[str]":
        return self.repository.git.execute(
            ["git", "grep", "-l", self.search]
        ).splitlines()  # type: ignore

    def fix(self, file: str) -> None:
        path = Path(self.repository.working_dir) / file
        content = path.read_text()
        new_content = re.sub(
            self.pattern,
            self.replace,
            content,
        )
        path.write_text(new_content)
