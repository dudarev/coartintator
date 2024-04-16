This is a simple Command File Interface (CFI) demo for managing and working with feeds in Markdown files.

## Current Features

- Crawl feeds and update their posts
- Download posts from feeds when placed into `Download` section
- Create summaries of posts with `SUM` command

See [User Stories](STORIES.md) for more details.

## Current Implementation

- Feeds - YouTube channels
- `SUM` command with Anthropic's Haiku model to create summaries

See [Future Plans](PLAN.md).

## Usage

Place feeds files in `feeds/` directory. Specify feed URL in the front matter of the file, for example:

```markdown
---
feed_url: https://www.youtube.com/@anthropic-ai
type: feed
---
```

Use `c` command to crawl the feeds.

Move posts you want to download to `Download` section. Run `c` command again. Posts are created in `posts/` directory.

Use `SUM` command in a post to create a summary. Run `c` command again. Find the summaries in `summaries/` directory.
