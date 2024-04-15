from coartintator.downloading_strategy import AbstractDownloadingStrategyFactory
from coartintator.entities import Post


class PostDownloader:
    def __init__(
        self, downloading_strategy_factory: AbstractDownloadingStrategyFactory
    ):
        self.downloading_strategy_factory = downloading_strategy_factory

    def download(self, post: Post) -> Post:
        strategy = self.downloading_strategy_factory.get_strategy(post)
        print(f"Downloading post: {post.name} with strategy: {strategy}")
        post = strategy.download(post)
        post.status = "read"
        return post
