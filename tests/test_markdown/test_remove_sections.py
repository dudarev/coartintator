import pytest

from coartintator.markdown import remove_sections


@pytest.mark.parametrize(
    "text, titles, expected",
    [
        pytest.param(
            "# Title 1\nSome content\n## Title 2\nMore content\n## Title 3\nEven more content",
            ["Title 2", "Title 3"],
            "# Title 1\nSome content",
            id="Remove multiple sections",
        ),
        pytest.param(
            "# Title 1\nSome content\n## Title 2\nMore content\n## Title 3\nEven more content",
            ["Title 1", "Title 2", "Title 3"],
            "",
            id="Remove all sections",
        ),
        pytest.param(
            "# Title 1\nSome content\n## Title 2\nMore content\n## Title 3\nEven more content",
            ["Title 4"],
            "# Title 1\nSome content\n## Title 2\nMore content\n## Title 3\nEven more content",
            id="Remove non-existing section",
        ),
        pytest.param(
            "",
            ["Title 1", "Title 2", "Title 3"],
            "",
            id="Remove sections from empty text",
        ),
        pytest.param(
            "",
            ["Title 1"],
            "",
            id="Remove non-existing section from empty text",
        ),
    ],
)
def test_remove_sections(text, titles, expected):
    assert remove_sections(text, titles) == expected
