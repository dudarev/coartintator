import shutil
from pathlib import Path

import pytest

from coartintator.entities import Post, PostsSet
from coartintator.repo import FileBasedRepository
from coartintator.services.feed_updater import FeedUpdater
from coartintator.entities import PostSummary

REPO_PATH = Path(__file__).parent / "assets" / "test_file_based_repo"
REPO_FILE = "feed_1.md"
REPO_FILE_PATH = REPO_PATH / "feeds" / REPO_FILE


class FakePostFactory:
    def create_post(index: int) -> Post:
        return Post(
            name=f"Post {index}",
            title=f"Post {index}",
            url=f"https://www.youtube.com/watch?v=post-{index}",
        )

    @classmethod
    def create_posts(cls, n: int) -> PostsSet:
        return PostsSet([cls.create_post(index) for index in range(1, n + 1)])


def test_file_based_repository():
    repo = FileBasedRepository(REPO_PATH)
    feeds = repo.get_feeds_to_crawl()
    assert len(feeds) == 1
    feed = feeds[0]

    assert feed.name == "feed_1"
    assert feed.url == "https://www.youtube.com/@EveryInc"

    file_content = REPO_FILE_PATH.read_text().split("---")[-1].strip()
    assert feed.content == file_content


@pytest.fixture
def random_vault(tmpdir):
    shutil.copytree(REPO_PATH, tmpdir, dirs_exist_ok=True)
    return tmpdir


def test_file_based_repository_save(random_vault):
    repo = FileBasedRepository(random_vault)
    feeds = repo.get_feeds_to_crawl()
    assert len(feeds) == 1
    FeedUpdater(repo).update_feed(feeds[0], FakePostFactory.create_posts(7))

    # re-read the feed
    feeds = repo.get_feeds_to_crawl()
    assert len(feeds) == 1
    feed = feeds[0]
    assert len(PostsSet.from_markdown(feed.content).posts) == 7


def test_get_posts_to_summarize(random_vault):
    repo = FileBasedRepository(random_vault)
    posts = repo.get_posts_to_summarize()

    assert len(posts) == 1
    assert posts[0].name == "post_1"


def test_file_based_repository_save_post_summary(random_vault):
    repo = FileBasedRepository(random_vault)
    posts = repo.get_posts_to_summarize()
    summary = PostSummary(post=posts[0], summary="This is a summary.")
    repo.save_post_summary(summary)

    # Verify that the summary file is created
    file_path = repo.summaries_path / "Summary - post_1.md"
    assert file_path.exists()

    # Verify the content of the summary file
    with open(file_path, "r") as f:
        assert "This is a summary." in f.read()
