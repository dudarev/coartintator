from coartintator.downloading_strategy import (
    AbstractDownloadingStrategy,
    AbstractDownloadingStrategyFactory,
)
from coartintator.downloading_strategy.youtube import YouTubeDownloadingStrategy
from coartintator.entities import Post


class DownloadingStrategyFactory(AbstractDownloadingStrategyFactory):
    @staticmethod
    def is_youtube(url: str) -> bool:
        youtube_domains = ["youtube.com", "youtu.be"]
        if any(domain in url for domain in youtube_domains):
            return True
        return False

    def get_strategy(self, post: Post) -> AbstractDownloadingStrategy:
        if self.is_youtube(post.url):
            return YouTubeDownloadingStrategy()
        else:
            raise ValueError("Unsupported URL")
