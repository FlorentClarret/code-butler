from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from git import Repo
    from typing import Iterable


class Rule(ABC):
    def __init__(self, repository: "Repo"):
        self.repository = repository

    @property
    def id(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def detect(self) -> "Iterable[str]":
        # TODO yield
        pass

    @abstractmethod
    def fix(self, file: str) -> None:
        pass

    @abstractmethod
    def commit_message(self) -> str:
        pass

    def pr_title(self) -> str:
        return self.commit_message()

    @abstractmethod
    def pr_body(self) -> str:
        pass
