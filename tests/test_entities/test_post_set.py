import textwrap

from coartintator.entities import Post, PostsSet

CONTENT_WITH_POSTS = """
## Read
- [[Post 7]]
- [[Post 8]]

## New

- [Post 1](https://www.youtube.com/watch?v=post-1)
- [Post 2](https://www.youtube.com/watch?v=post-2)

## Download

- [Post 3](https://www.youtube.com/watch?v=post-3)
- [Post 4](https://www.youtube.com/watch?v=post-4)

## Archived

- [Post 5](https://www.youtube.com/watch?v=post-5)
- [Post 6](https://www.youtube.com/watch?v=post-6)
"""


def test_post_set_from_markdown():
    post_set = PostsSet.from_markdown(CONTENT_WITH_POSTS)

    assert len(post_set.posts) == 8
    assert len(post_set.name_set) == 8

    # filter new posts
    new_posts = post_set.filter_by_status("new")
    assert len(new_posts) == 2

    # filter download posts
    download_posts = post_set.filter_by_status("download")
    assert len(download_posts) == 2

    # filter archived posts
    archived_posts = post_set.filter_by_status("archived")
    assert len(archived_posts) == 2

    # filter read posts
    read_posts = post_set.filter_by_status("read")
    assert len(read_posts) == 2


def test_adding_existing_name():
    content_before = textwrap.dedent(
        """
        ## Read
        - [[Post 7]]

        ## Download
        - [Post 1](https://www.youtube.com/watch?v=post-1)
        """
    ).strip()
    expected_content = textwrap.dedent(
        """
        ## Read
        - [[Post 7]]
        - [[Post 1]]
        """
    ).strip()

    post_set = PostsSet.from_markdown(content_before)

    post = Post(
        name="Post 1", url="https://example.com", content="content", status="read"
    )
    post_set = post_set.add_post_set(PostsSet([post]))

    assert len(post_set.posts) == 2
    assert len(post_set.name_set) == 2
    print(post_set.to_markdown())
    print(expected_content)
    assert post_set.to_markdown() == expected_content


def test_to_markdown_with_multiple_statuses():
    post1 = Post(
        name="Test Entity 1",
        url="https://example.com/1",
        status="read",
    )
    post2 = Post(
        name="Test Entity 2",
        url="https://example.com/2",
        status="new",
    )
    post3 = Post(
        name="Test Entity 3",
        url="https://example.com/3",
        status="archived",
    )
    entity_set = PostsSet([post1, post2, post3])

    expected = "## Read\n- [[Test Entity 1]]\n\n## New\n- [Test Entity 2](https://example.com/2)\n\n## Archived\n- [Test Entity 3](https://example.com/3)"
    assert entity_set.to_markdown() == expected


def test_add_posts_sets():
    post1 = Post(
        name="Test Entity 1",
        url="https://example.com/1",
        status="read",
    )
    post2 = Post(
        name="Test Entity 2",
        url="https://example.com/2",
        status="new",
    )
    post3 = Post(
        name="Test Entity 3",
        url="https://example.com/3",
        status="archived",
    )
    posts_set1 = PostsSet([post1, post2])
    posts_set2 = PostsSet([post3])
    assert (posts_set1.add_post_set(posts_set2)).posts == [post1, post2, post3]

    posts_set1 = PostsSet([post1, post2])
    posts_set2 = PostsSet([post3])
    assert (posts_set2.add_post_set(posts_set1)).posts == [post3, post1, post2]

    posts_set1 = PostsSet([post1, post2])
    posts_set1.add_post_set(posts_set1)
    assert posts_set1.posts == [post2, post1]
