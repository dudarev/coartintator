from coartintator.entities import Post
from coartintator.repo import AbstractRepository


class PostUpdater:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository

    def update_post(self, post: Post, dry_run: bool = False):
        print(f"Updating post {post.name}")
        if not dry_run:
            self.repository.update_post(post)
