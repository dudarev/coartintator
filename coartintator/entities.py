from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Literal

import frontmatter
import pathvalidate

from coartintator import markdown

PostStatusT = Literal["read", "download", "new", "archived"]
# we repeat the section names here to preserve the order
SECTION_NAMES = ["Read", "Download", "New", "Archived", "Archive"]


@dataclass(kw_only=True)
class Post:
    """
    Posts that are crawled have titles, name is derived by sanitization.
    Posts that are in content have names, title can be stored in metadata.
    """

    name: str = None
    title: str = None
    url: str = None
    content: str = None
    status: PostStatusT = "new"
    updated_at: datetime = None

    def __post_init__(self):
        if self.name is None and self.title is None:
            raise ValueError("At least one of name or title should be set for Post.")
        if self.name is None:
            self.name = self.title
        self.name = pathvalidate.sanitize_filename(self.name)
        self.updated_at = self.updated_at or datetime.now(tz=timezone.utc).isoformat()

    @staticmethod
    def from_dict(data: dict):
        return Post(
            name=data["name"],
            title=data.get("title"),
            url=data.get("post_url"),
            content=data.get("content"),
            status=data.get("status", "read"),
            updated_at=data.get("updated_at"),
        )

    def to_dict_without_content(self):
        return {
            "type": "post",
            "title": self.title,
            "post_url": self.url,
            "updated_at": self.updated_at,
        }

    def to_link(self):
        """
        Return a string representation of the post.
        """
        if self.status == "read":
            return f"- [[{self.name}]]"
        return f"- [{self.name}]({self.url})"

    def to_markdown(self) -> str:
        frontmatter_post = frontmatter.Post(
            content=self.content or "", **self.to_dict_without_content()
        )
        return frontmatter.dumps(frontmatter_post)


@dataclass(kw_only=True)
class PostSummary:
    post: Post
    summary: str

    @property
    def name(self):
        return f"Summary - {self.post.name}"

    def to_dict_without_content(self):
        return {
            "type": "summary",
            "post_url": self.post.url,
        }

    def to_link(self):
        """
        Return a link to the post summary.
        """
        return f"[[{self.name}]]"

    def to_markdown(self) -> str:
        frontmatter_post = frontmatter.Post(
            content=self.summary or "", **self.to_dict_without_content()
        )
        return frontmatter.dumps(frontmatter_post)


class PostsSet:
    """
    Post with a given name is unique in the set.
    """

    def __init__(self, posts: List[Post]):
        self.posts = posts
        self.name_set = {post.name for post in posts}

    def __contains__(self, post: Post) -> bool:
        pass

    def __len__(self) -> int:
        return len(self.posts)

    def pop(self) -> Post:
        post = self.posts.pop()
        self.name_set.remove(post.name)
        return post

    def add_post(self, post: Post):
        if post.name not in self.name_set:
            self.posts.append(post)
            self.name_set.add(post.name)
        if post.name in self.name_set:
            if post.status == "new":
                return
            self.posts = [p for p in self.posts if p.name != post.name]
            self.posts.append(post)

    def add_post_set(self, post_set: "PostsSet"):
        for post in post_set.posts:
            self.add_post(post)
        return self

    def filter_by_status(self, status: PostStatusT) -> List[Post]:
        return [post for post in self.posts if post.status == status]

    def to_markdown(self) -> str:
        """
        Return a markdown representation of the post set.

        Iterate over all possible PostStatusT and return sections with the posts.
        """
        res = ""
        for section_name in SECTION_NAMES:
            posts = self.filter_by_status(section_name.lower())
            if posts:
                section = f"## {section_name}\n"
                for post in posts:
                    section += post.to_link() + "\n"
                res += section + "\n"
        return res.strip()

    @staticmethod
    def from_markdown(text: str) -> "PostsSet":
        """
        Given a markdown content, extract posts and return a PostSet.

        For example, given the following markdown text:
        ## New
        [Post 1](https://www.youtube.com/watch?v=post-1)
        [Post 2](https://www.youtube.com/watch?v=post-2)
        ## Download
        [Post 3](https://www.youtube.com/watch?v=post-3)
        [Post 4](https://www.youtube.com/watch?v=post-4)
        ## Archived
        [Post 5](https://www.youtube.com/watch?v=post-5)
        [Post 6](https://www.youtube.com/watch?v=post-6)

        We should get a PostSet with 6 posts, 2 with each status.
        """
        res = PostsSet([])
        for section_name in SECTION_NAMES:
            status = section_name.lower()
            status_normalized = "archived" if status == "archive" else status
            section = markdown.extract_section(text, section_name, 2)
            links = markdown.get_links(section)
            for link in links:
                res.add_post(
                    Post(
                        name=link.title,
                        title=link.title,
                        url=link.url,
                        status=status_normalized,
                    )
                )
            wikilinks = markdown.get_wikilinks(section)
            for link in wikilinks:
                res.add_post(Post(name=link, status=status_normalized))
        return res


@dataclass
class Feed:
    name: str
    url: str
    content: str = None
    last_crawled_at: datetime = None

    @staticmethod
    def from_dict(data: dict):
        return Feed(
            name=data["name"],
            url=data["feed_url"],
            content=data["content"],
            last_crawled_at=data.get("last_crawled_at"),
        )

    def to_dict_without_content(self):
        return {
            "type": "feed",
            "name": self.name,
            "feed_url": self.url,
            "last_crawled_at": self.last_crawled_at,
        }

    def update_content(self, posts: PostsSet):
        content_before = markdown.remove_sections(self.content or "", SECTION_NAMES)
        content_after = (
            content_before
            + "\n\n"
            + (
                PostsSet.from_markdown(self.content or "").add_post_set(posts)
            ).to_markdown()
        )
        self.content = content_after

    def to_markdown(self) -> str:
        frontmatter_post = frontmatter.Post(
            content=self.content or "", **self.to_dict_without_content()
        )
        return frontmatter.dumps(frontmatter_post)

    def get_posts(self) -> PostsSet:
        return PostsSet.from_markdown(self.content or "")
