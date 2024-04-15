from coartintator.crawling_strategy import (
    AbstractCrawlingStrategy,
    AbstractCrawlingStrategyFactory,
)
from coartintator.crawling_strategy.twitter import TwitterCrawlingStrategy
from coartintator.crawling_strategy.youtube import (
    YouTubeCrawlingStrategy,
)
from coartintator.entities import Feed


class CrawlingStrategyFactory(AbstractCrawlingStrategyFactory):
    @staticmethod
    def get_strategy(feed: Feed) -> AbstractCrawlingStrategy:
        if "youtube.com" in feed.url:
            return YouTubeCrawlingStrategy()
        elif "twitter.com" in feed.url:
            return TwitterCrawlingStrategy()
        else:
            raise ValueError("Unsupported URL")
