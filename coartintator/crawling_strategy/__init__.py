from abc import ABC, abstractmethod


class AbstractCrawlingStrategy(ABC):
    @abstractmethod
    def crawl(self, feed):
        pass


class AbstractCrawlingStrategyFactory(ABC):
    @abstractmethod
    def get_strategy(self, url: str) -> AbstractCrawlingStrategy:
        pass
