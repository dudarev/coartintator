import argparse
from pathlib import Path

from coartintator.crawling_strategy.factory import CrawlingStrategyFactory
from coartintator.downloading_strategy.factory import DownloadingStrategyFactory
from coartintator.entities import PostsSet
from coartintator.repo import AbstractRepository, FileBasedRepository
from coartintator.services import FeedCrawler
from coartintator.services.feed_updater import FeedUpdater
from coartintator.services.post_downloader import PostDownloader
from coartintator.services.post_summarizer import (
    AbstractPostSummarizer,
    ClaudeHaikuSummarizer,
)
from coartintator.services.post_updater import PostUpdater


class Coartintator:
    def __init__(
        self,
        repository: AbstractRepository,
        feed_crawler: FeedCrawler,
        feed_updater: FeedUpdater,
        post_downloader: PostDownloader,
        post_updater: PostUpdater,
        post_summarizer: AbstractPostSummarizer,
    ):
        self.repository = repository
        self.feed_crawler = feed_crawler
        self.feed_updater = feed_updater
        self.post_downloader = post_downloader
        self.post_updater = post_updater
        self.post_summarizer = post_summarizer

    def run(self, dry_run: bool = False):
        feeds_to_crawl = self.repository.get_feeds_to_crawl()
        print("Feeds to crawl:")

        for f in feeds_to_crawl:
            print(f.name)

        for f in feeds_to_crawl:
            posts = self.feed_crawler.crawl_feed(f)
            self.feed_updater.update_feed(f, posts, dry_run=dry_run)
            posts_set = f.get_posts()
            posts_to_download = PostsSet(posts_set.filter_by_status("download"))
            posts_downloaded = PostsSet([])
            for p in posts_to_download.posts:
                new_post = self.post_downloader.download(p)
                self.post_updater.update_post(new_post, dry_run=dry_run)
                posts_downloaded.add_post(new_post)
            self.feed_updater.update_feed(f, posts_downloaded, dry_run=dry_run)

        for p in self.repository.get_posts_to_summarize():
            print(f"Summarizing post {p.name}")
            summary = self.post_summarizer.summarize(p)
            if not dry_run:
                self.repository.save_post_summary(summary)
                self.repository.add_summary_link(summary)


def add_arguments(parser):
    parser.add_argument(
        "--dry-run", action="store_true", help="Run without making any changes"
    )
    parser.add_argument("--path", type=Path, help="Vault path", default=".")


def parse_args():
    parser = argparse.ArgumentParser(prog="c")
    add_arguments(parser)
    return parser.parse_args()


def main():
    args = parse_args()

    repo = FileBasedRepository(args.path)
    feed_crawler = FeedCrawler(CrawlingStrategyFactory())
    feed_updater = FeedUpdater(repo)
    post_downloader = PostDownloader(DownloadingStrategyFactory())
    post_updater = PostUpdater(repo)
    post_summarizer = ClaudeHaikuSummarizer()

    coartintator = Coartintator(
        repo,
        feed_crawler,
        feed_updater,
        post_downloader,
        post_updater,
        post_summarizer,
    )

    coartintator.run(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
