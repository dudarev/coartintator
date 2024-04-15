import textwrap

from coartintator.entities import Feed, Post, PostsSet


def test_feed_from_dict_with_posts():
    feed = Feed.from_dict(
        {
            "name": "feed_1.md",
            "feed_url": "https://www.youtube.com/@EveryInc",
            "content": "",
        }
    )
    assert feed.name == "feed_1.md"
    assert feed.content == ""


def test_update_content():
    # Create a Feed instance
    feed = Feed(
        name="Test Feed",
        url="https://example.com/feed",
        content="Existing content",
    )

    # Create some Post instances
    post1 = Post(
        name="Test Entity 1",
        url="https://example.com/1",
        status="read",
    )
    posts = PostsSet(
        [
            post1,
        ]
    )

    # Call the update_content method
    feed.update_content(posts)

    # Check if the content has been updated correctly
    expected_content = textwrap.dedent(
        """
        Existing content

        ## Read
        - [[Test Entity 1]]
    """
    ).strip()
    assert feed.content == expected_content


def test_update_existing_content_with_sections():
    # Create a Feed instance
    feed = Feed(
        name="Test Feed",
        url="https://example.com/feed",
        content=textwrap.dedent(
            """
            Existing content

            ## Read
            - [[Test Entity 1]]
            - [[Test Entity 2]]

            ## New
            - [Test Entity 3](https://example.com/3)
            - [Test Entity 4](https://example.com/4)

            ## Archived
            - [Test Entity 5](https://example.com/5)
            - [Test Entity 6](https://example.com/6)
        """
        ).strip(),
    )

    # Create some Post instances
    post1 = Post(
        name="Test Entity 7",
        url="https://example.com/7",
        status="read",
    )
    post2 = Post(
        name="Test Entity 8",
        url="https://example.com/8",
        status="new",
    )
    post3 = Post(
        name="Test Entity 9",
        url="https://example.com/9",
        status="archived",
    )
    posts = PostsSet(
        [
            post1,
            post2,
            post3,
        ]
    )

    # Call the update_content method
    feed.update_content(posts)

    expected_content = textwrap.dedent(
        """
        Existing content

        ## Read
        - [[Test Entity 1]]
        - [[Test Entity 2]]
        - [[Test Entity 7]]

        ## New
        - [Test Entity 3](https://example.com/3)
        - [Test Entity 4](https://example.com/4)
        - [Test Entity 8](https://example.com/8)

        ## Archived
        - [Test Entity 5](https://example.com/5)
        - [Test Entity 6](https://example.com/6)
        - [Test Entity 9](https://example.com/9)
    """
    ).strip()
    assert feed.content == expected_content


def test_to_markdown_with_content():
    feed = Feed(
        name="Test Feed",
        url="https://example.com/feed",
        content="Existing content",
    )
    expected = textwrap.dedent(
        """
        ---
        feed_url: https://example.com/feed
        last_crawled_at: null
        name: Test Feed
        type: feed
        ---

        Existing content
    """
    ).strip()
    assert feed.to_markdown() == expected


def test_to_markdown_without_content():
    feed = Feed(
        name="Test Feed",
        url="https://example.com/feed",
    )
    expected = textwrap.dedent(
        """
        ---
        feed_url: https://example.com/feed
        last_crawled_at: null
        name: Test Feed
        type: feed
        ---
        """
    ).strip()
    assert feed.to_markdown() == expected
