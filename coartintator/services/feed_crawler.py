from coartintator.crawling_strategy.factory import AbstractCrawlingStrategyFactory
from coartintator.entities import Feed, PostsSet


class FeedCrawler:
    def __init__(self, strategy_factory: AbstractCrawlingStrategyFactory):
        self.strategy_factory = strategy_factory

    def crawl_feed(self, feed: Feed) -> PostsSet:
        strategy = self.strategy_factory.get_strategy(feed)
        return strategy.crawl(feed)
