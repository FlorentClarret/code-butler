from typing import TYPE_CHECKING

from code_butler.rules.common.search_replace_rule import SearchAndReplaceRule

if TYPE_CHECKING:
    from git import Repo


class SetOutputRule(SearchAndReplaceRule):
    def __init__(self, repository: "Repo"):
        super().__init__(
            repository,
            "::set-output name=",
            r"::set-output name=([^:]*)::(.*)",
            r'\g<1>=\g<2> >> "$GITHUB_OUTPUT"',
        )

    def commit_message(self) -> str:
        return "chore(ci): replace deprecated set-output commands"

    def pr_body(self) -> str:
        return "See https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/"
