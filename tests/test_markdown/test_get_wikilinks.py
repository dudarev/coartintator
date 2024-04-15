import pytest

from coartintator.markdown import get_wikilinks


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", []),
        ("This is a sample text without any wikilinks.", []),
        ("This is a [[wikilink]].", ["wikilink"]),
        (
            "These are some [[wikilinks]] and [[more wikilinks]].",
            ["wikilinks", "more wikilinks"],
        ),
        ("This is a [[wikilink|label]].", ["wikilink"]),
        (
            "These are some [[wikilinks|link1]] and [[more wikilinks|link2]].",
            ["wikilinks", "more wikilinks"],
        ),
    ],
)
def test_get_wikilinks(text, expected):
    assert get_wikilinks(text) == expected
