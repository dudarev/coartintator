from abc import ABC, abstractmethod

from coartintator.entities import Post


class AbstractDownloadingStrategy(ABC):
    @abstractmethod
    def download(self, post: Post) -> Post:
        pass

    def __str__(self):
        return self.__class__.__name__


class AbstractDownloadingStrategyFactory(ABC):
    @abstractmethod
    def get_strategy(self, post: Post) -> AbstractDownloadingStrategy:
        pass
