from typing import TYPE_CHECKING

from code_butler.rules.github.save_state import SaveStateRule
from code_butler.rules.github.set_output import SetOutputRule
from code_butler.rules.rule_group import RuleGroup

if TYPE_CHECKING:
    from git import Repo


class DeprecatedCommands(RuleGroup):
    def __init__(self, repository: "Repo"):
        super().__init__(
            repository, [SetOutputRule(repository), SaveStateRule(repository)]
        )

    def commit_message(self) -> str:
        return "chore(ci): replace deprecated commands"

    def pr_body(self) -> str:
        return "See https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/"
