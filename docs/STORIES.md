# Stories

- Feeds are located in the vault in `feeds/` directory
- Posts are located in the vault in `posts/` directory
- User can create a note that describes a feed.
  - Properties:
    - feed_url
    - tags
    - In the feed there are sections with Markdown level 2 headers
      - New
      - Download
      - Read
      - Archived
- User can run `c` to run commands in all the feeds
  - First crawls all feeds that were updated more than `UPDATE_INTERVAL` ago
  - Gets all posts from the feed
  - Updates those that are not present in the file
  - Then downloads all the posts from 'Download' section

## Later

- Implement `last_crawled_at` property for feeds
- Implement filter logic when determining which feeds to update
