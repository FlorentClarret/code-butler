from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable

    from git import Repo

    from code_butler.rules.issue import Issue


class Rule(ABC):
    def __init__(self, repository: "Repo"):
        self.repository = repository

    @property
    def id(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def detect(self) -> "Iterable[Issue]":
        pass

    @abstractmethod
    def fix(self, issue: "Issue") -> None:
        pass

    @abstractmethod
    def commit_message(self) -> str:
        pass

    def pr_title(self) -> str:
        return self.commit_message()

    @abstractmethod
    def pr_body(self) -> str:
        pass
