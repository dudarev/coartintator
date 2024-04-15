"""
For a given YouTube channel, list all videos from the channel.
"""

import os

from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()  # Load environment variables from .env file


HANDLE = "EveryInc"
CHANNEL_ID = "UCjIMtrzxYc0lblGhmOgC_CA"  # Replace with the channel's ID

API_KEY = os.getenv("YOUTUBE_API_KEY")


class FeedCrawler:
    def __init__(self, api_key, channel_id):
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.channel_id = channel_id

    def crawl(self):
        request = self.youtube.search().list(
            part="snippet",
            channelId=self.channel_id,
            maxResults=50,  # Change if needed
            order="date",  # Get videos by date
        )
        response = request.execute()

        for item in response["items"]:
            if "videoId" in item["id"]:
                print(
                    f"Title: {item['snippet']['title']}, Video Id: {item['id']['videoId']}"
                )
            else:
                print(f"Title: {item['snippet']['title']}, but it's not a video.")


crawler = FeedCrawler(API_KEY, CHANNEL_ID)
crawler.crawl()
