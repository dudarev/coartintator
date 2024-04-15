"""
Create temporary repo
Create a post
Update the post
Check that the post was updated
"""

from coartintator.entities import Post
from coartintator.repo import FileBasedRepository
from coartintator.services.post_updater import PostUpdater


def test_post_updater(random_vault):
    post = Post(
        name="Test Post",
        url="https://example.com",
        content="Existing content",
    )
    assert post.status == "new"
    repo = FileBasedRepository(random_vault)
    post_updater = PostUpdater(repo)
    post_updater.update_post(post)
    with open(repo.posts_path / post.name + ".md") as f:
        file_content = f.read().strip()
        assert file_content == post.to_markdown().strip()


def test_post_updater_no_updated(random_vault):
    post = Post(
        name="Test Post",
        url="https://example.com",
        content="Existing content",
    )
    assert post.status == "new"
    repo = FileBasedRepository(random_vault)

    # Create a post with the same name but different content
    with open(repo.posts_path / "Test Post.md", "w") as f:
        f.write("Existing content")

    post_updater = PostUpdater(repo)
    post_updater.update_post(post)
    with open(repo.posts_path / post.name + ".md") as f:
        file_content = f.read().strip()
        assert file_content == "Existing content"
