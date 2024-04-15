import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Link:
    title: str
    url: str


def get_links(text: str) -> list[Link]:
    """
    Given a markdown text, extract Markdown links and return a list of Link objects.
    """
    # https://regex101.com/library/BOkFPx
    link_pattern = r"(?:\[(?P<text>.*?)\])\((?P<link>.*?)\)"
    links = re.findall(link_pattern, text)
    link_objects = [Link(title, url) for title, url in links]
    return link_objects


def get_wikilinks(text: str) -> list[str]:
    """
    Given a markdown text, extract wikilinks and return a list of link names.
    Wikilink looks like: [[link|label]]
    """
    link_pattern = r"\[\[(?P<text>.*?)(?:\|(?P<label>.*?))?\]\]"
    links = re.findall(link_pattern, text)
    return [link for link, _ in links]


def _get_title_and_level(line: str) -> tuple[str, int]:
    """
    Given a markdown line, return the title.
    """
    if not line:
        return "", 0
    level = 0
    while line[level] == "#":
        level += 1
    if level == 0:
        return "", 0
    return line[level + 1 :].strip(), level


def remove_sections(text: str, titles: list[str]) -> str:
    """
    Remove sections from a markdown text.

    For example, given the following markdown text:

    # Title 1
    Some content
    ## Title 2
    More content
    ## Title 3
    Even more content

    If we call `remove_sections(text, ["Title 2", "Title 3"])`, we should get:

    # Title 1
    Some content
    """
    lines = text.split("\n")
    res = []
    skip = False
    level_to_skip = 0
    for line in lines:
        title, level = _get_title_and_level(line)
        if skip and level > 0 and level <= level_to_skip:
            skip = False
            level_to_skip = 0
        if level == 0 and skip:
            continue
        if level > 0 and title in titles:
            skip = True
            level_to_skip = level
        if not skip:
            res.append(line)
    return "\n".join(res).strip()


def extract_section(text: str, title: str, level: int) -> str:
    """
    Extract a section from a markdown text.

    For example, given the following markdown text:

    # Title 1
    ## Title 2
    ### Title 3
    Some content
    ## Title 4
    More content

    If we call `extract_section(text, "Title 2", 2)`, we should get:
    ### Title 3
    Some content
    """
    lines = text.split("\n")
    start = None
    end = None
    for i, line in enumerate(lines):
        if line.startswith("#" * level + " " + title):
            start = i
            continue
        if start is not None and line.startswith("#" * level + " "):
            end = i
            break
    if start is None:
        return ""
    if end is None:
        return "\n".join(lines[start + 1 :])
    return "\n".join(lines[start + 1 : end])
