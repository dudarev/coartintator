from coartintator.crawling_strategy.youtube import (
    FakeYouTubeCrawlingStrategy,
    youtube_videos_to_posts,
)
from coartintator.entities import Feed, Post

FAKE_YOUTUBE_FEED = Feed(name="fake", url="https://www.youtube.com/channel/fake")


def test_youtube_videos_to_posts():
    strategy = FakeYouTubeCrawlingStrategy()
    videos = strategy.get_videos(FAKE_YOUTUBE_FEED)
    assert len(videos) > 0
    posts = youtube_videos_to_posts(videos)
    assert len(posts) == len(videos)
    assert type(posts.pop()) == Post
