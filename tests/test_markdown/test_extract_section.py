from coartintator.markdown import extract_section

TEXT = """# Title 1
## Title 2
### Title 3
Some content
## Title 4
More content
"""


def test_extract_section():
    assert extract_section(TEXT, "Title 1", 2) == ""
    assert extract_section(TEXT, "Title 1", 1) == "\n".join(TEXT.split("\n")[1:])
    assert extract_section(TEXT, "Title 2", 2) == "### Title 3\nSome content"
    assert extract_section(TEXT, "Title 4", 2) == "More content\n"
