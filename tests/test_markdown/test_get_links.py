from coartintator.markdown import Link, get_links


def test_empty_text():
    text = ""
    expected = []
    assert get_links(text) == expected


def test_no_links():
    text = "This is a sample text without any links."
    expected = []
    assert get_links(text) == expected


def test_single_link():
    text = "This is a [link](https://example.com)."
    expected = [Link("link", "https://example.com")]
    assert get_links(text) == expected


def test_multiple_links():
    text = "These are some [links](https://example.com) and [more links](https://example.org)."
    expected = [
        Link("links", "https://example.com"),
        Link("more links", "https://example.org"),
    ]
    assert get_links(text) == expected


def test_nested_links():
    text = "This is a [nested [link]](https://example.com)."
    expected = [Link("nested [link]", "https://example.com")]
    assert get_links(text) == expected
