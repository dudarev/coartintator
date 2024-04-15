import abc
import os
from pathlib import Path
from typing import List

import frontmatter

from coartintator.entities import Feed, Post


def file_name_to_name(file_name: str) -> str:
    return file_name.split(".")[0]


def name_to_file_name(name: str) -> str:
    return name + ".md"


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get_feed(self, feed_name: str) -> str:
        pass

    @abc.abstractmethod
    def get_feeds_to_crawl(self) -> List[Feed]:
        pass

    @abc.abstractmethod
    def update_feed(self, feed: Feed):
        pass

    @abc.abstractmethod
    def update_post(self, post: Post):
        pass


class FileBasedRepository(AbstractRepository):
    def __init__(self, path: Path):
        self.path = path
        self.feeds_path = path / "feeds"
        self.posts_path = path / "posts"
        self._check_path()

    def _check_path(self):
        if not self.path.exists():
            print(f"Path `{self.path}` does not exist")
            exit(1)
        if not self.feeds_path.exists():
            print(f"Feeds path `{self.feeds_path}` does not exist")
            exit(1)
        if not self.posts_path.exists():
            self.posts_path.mkdir()

    @staticmethod
    def _is_feed(path: Path) -> bool:
        with open(path) as f:
            post = frontmatter.load(f)
            if "type" in post.metadata and post.metadata["type"] == "feed":
                return True
            else:
                return False

    def get_feed(self, feed_name: str) -> Feed:
        file_path = self.feeds_path / name_to_file_name(feed_name)
        with open(file_path) as f:
            raw_post = frontmatter.load(f)
            data = raw_post.metadata
            data["content"] = raw_post.content
            data["name"] = feed_name
            return Feed.from_dict(data)

    def get_feeds_to_crawl(self) -> List[Feed]:
        return [
            self.get_feed(file_name_to_name(file_name))
            for file_name in os.listdir(self.feeds_path)
            if self._is_feed(self.feeds_path / file_name)
        ]

    def update_feed(self, feed: Feed):
        file_path = self.feeds_path / name_to_file_name(feed.name)
        with open(file_path, "w") as f:
            f.write(feed.to_markdown())

    def update_post(self, post: Post):
        file_path = self.posts_path / name_to_file_name(post.name)
        if file_path.exists():
            print("No update - post already exists")
        else:
            with open(file_path, "w") as f:
                f.write(post.to_markdown())
