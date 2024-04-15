from coartintator.entities import Post


def test_to_markdown_with_read_status():
    post = Post(
        name="Test Entity",
        url="https://example.com",
        status="read",
    )
    expected = "- [[Test Entity]]"
    assert post.to_link() == expected


def test_to_markdown_with_unread_status():
    post = Post(
        name="Test Entity",
        url="https://example.com",
    )
    expected = "- [Test Entity](https://example.com)"
    assert post.to_link() == expected


def test_post_init_with_name():
    post = Post(name="Test Post")
    assert post.name == "Test Post"


def test_post_init_with_title():
    post = Post(title="Test Title")
    assert post.name == "Test Title"


def test_post_init_with_invalid_name():
    post = Post(name="Test/Post")
    assert post.name == "TestPost"
