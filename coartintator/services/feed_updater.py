from coartintator.entities import Feed, PostsSet
from coartintator.repo import AbstractRepository


class FeedUpdater:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def update_feed(self, feed: Feed, posts: PostsSet, dry_run: bool = False) -> Feed:
        feed.update_content(posts)
        if not dry_run:
            self.repository.update_feed(feed)
