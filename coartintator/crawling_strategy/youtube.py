import types
from pathlib import Path

import orjson
import scrapetube

from coartintator.entities import Feed, Post, PostsSet

from . import AbstractCrawlingStrategy


def default_serializer(obj):
    if isinstance(obj, types.GeneratorType):
        return list(obj)
    raise TypeError


def youtube_video_to_post(video: dict) -> Post:
    return Post(
        name=video["title"]["runs"][0]["text"],
        title=video["title"]["runs"][0]["text"],
        url=f"https://www.youtube.com/watch?v={video['videoId']}",
    )


def youtube_videos_to_posts(videos: list[dict]) -> PostsSet:
    return PostsSet([youtube_video_to_post(video) for video in videos])


class YouTubeCrawlingStrategy(AbstractCrawlingStrategy):

    def get_videos(self, feed: Feed) -> list[dict]:
        print(f"Getting videos from YouTube feed {feed.name}")
        return scrapetube.get_channel(channel_url=feed.url)

    def crawl(self, feed: Feed) -> PostsSet:
        print(f"Crawling YouTube feed {feed.name}")
        videos = self.get_videos(feed)
        return youtube_videos_to_posts(videos)


class FakeYouTubeCrawlingStrategy(YouTubeCrawlingStrategy):
    DEFAULT_FAKE_DATA_PATH = (
        Path(__file__).parent.parent.parent
        / "tests/assets/test_feed_crawler/fakes_data/youtube_videos_feed_1.json"
    )

    def __init__(self, fake_data_path: Path = DEFAULT_FAKE_DATA_PATH) -> None:
        self.fake_data_path = fake_data_path

    def get_videos(self, feed):
        print(f"Getting fake videos from YouTube feed {feed.name}")
        with open(self.fake_data_path) as f:
            videos = orjson.loads(f.read())
        return videos
