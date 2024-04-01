from __future__ import annotations

from typing import TYPE_CHECKING

from code_butler.rules.common.search_replace_rule import SearchAndReplaceRule

if TYPE_CHECKING:
    from git import Repo


class SaveStateRule(SearchAndReplaceRule):
    def __init__(self, repository: Repo):
        super().__init__(
            repository,
            "::save-state name=",
            r"::save-state name=([^:]*)::(.*)",
            r'\g<1>=\g<2> >> "$GITHUB_STATE"',
        )

    def commit_message(self) -> str:
        return "chore(ci): replace deprecated save-output commands"

    def pr_body(self) -> str:
        return "See https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/"
